#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path

SOURCES_FILE = Path("scripts/sources.json")
DATA_DIR = Path("data")
WMDB_API = "https://api.wmdb.tv/api/v1/movie/search"

DOUBAN_API = "https://caiji.dbzy5.com/api.php/provide/vod/at/json/"

MOVIE_CATS = [1, 6, 7, 8, 9, 10, 11, 12]
TV_CATS = [2, 13, 14, 15, 16, 21, 22, 23, 24]
VARIETY_CATS = [3, 25, 26, 27, 28]

ADULT_KEYWORDS = ["伦理", "福利", "制服诱惑", "丝袜", "诱惑", "AV", "色情", "成人", "SM", "援交", "大尺度"]

def fetch_from_douban(category_ids, target_count=50):
    all_items = []
    
    for cat_id in category_ids:
        for pg in range(1, 4):
            try:
                params = {"ac": "detail", "t": cat_id, "pg": pg, "limit": 30}
                resp = requests.get(DOUBAN_API, params=params, timeout=10,
                                  headers={"User-Agent": "Mozilla/5.0"})
                data = resp.json()
                items = data.get("list", [])
                
                for item in items:
                    name = item.get("vod_name", "")
                    score = item.get("vod_douban_score", "")
                    
                    if any(kw in name for kw in ADULT_KEYWORDS):
                        continue
                    
                    if score and score != "0.0" and float(score) >= 6.0:
                        all_items.append({
                            "vod_id": item.get("vod_id", 0),
                            "vod_name": name,
                            "vod_pic": item.get("vod_pic", ""),
                            "vod_year": item.get("vod_year", ""),
                            "vod_area": item.get("vod_area", ""),
                            "vod_remarks": f"{score}分",
                            "vod_class": item.get("type_name", ""),
                            "rating": score,
                            "source": "豆瓣资源"
                        })
                
                time.sleep(0.3)
                
                pagecount = data.get("pagecount", 1)
                if pg >= pagecount:
                    break
                    
            except Exception as e:
                print(f"    错误: 分类{cat_id} 第{pg}页 - {e}")
                break
    
    seen = set()
    unique = []
    for item in all_items:
        name = item["vod_name"]
        if name not in seen:
            seen.add(name)
            unique.append(item)
    
    unique.sort(key=lambda x: float(x.get("rating", "0") or "0"), reverse=True)
    
    return unique[:target_count]

def save_category(items, filename):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    filepath = DATA_DIR / filename
    wrapped = {
        "list": items,
        "page": 1,
        "pagecount": 1,
        "total": len(items)
    }
    filepath.write_text(json.dumps(wrapped, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  保存: {filename} ({len(items)} 部)")

def main():
    print("从豆瓣资源源爬取数据（按评分排序）\n")
    
    print("爬取电影...")
    movies = fetch_from_douban(MOVIE_CATS, 50)
    save_category(movies, "movies.json")
    
    print("\n爬取电视剧...")
    tv = fetch_from_douban(TV_CATS, 50)
    save_category(tv, "tv.json")
    
    print("\n爬取综艺...")
    variety = fetch_from_douban(VARIETY_CATS, 50)
    save_category(variety, "variety.json")
    
    print("\n全部完成!")
    print(f"  电影: {len(movies)} 部 (最高评分: {movies[0]['rating'] if movies else '无'})")
    print(f"  电视剧: {len(tv)} 部 (最高评分: {tv[0]['rating'] if tv else '无'})")
    print(f"  综艺: {len(variety)} 部 (最高评分: {variety[0]['rating'] if variety else '无'})")

if __name__ == "__main__":
    main()
