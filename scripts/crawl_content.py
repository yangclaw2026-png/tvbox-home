#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCES_FILE = Path("scripts/sources.json")
DATA_DIR = Path("data")
WMDB_API = "https://api.wmdb.tv/api/v1/movie/search"

MOVIE_KEYWORDS = ["电影", "剧情", "动作", "喜剧", "爱情", "科幻", "恐怖", "战争", "动画", "犯罪", "悬疑", "冒险", "奇幻"]
TV_KEYWORDS = ["国产剧", "港台剧", "日韩剧", "欧美剧", "海外剧", "连续剧", "电视剧", "剧集"]
VARIETY_KEYWORDS = ["综艺", "真人秀", "脱口秀", "选秀", "音乐", "访谈"]
ADULT_KEYWORDS = ["伦理", "福利", "制服诱惑", "丝袜", "诱惑", "AV", "色情", "成人", "SM", "援交", "大尺度", "夜撩", "春宵", "欲女", "偷情", "私密", "激情", "辣妹"]

def fetch_categories(api):
    try:
        resp = requests.get(api, params={"ac": "list"}, timeout=8,
                          headers={"User-Agent": "Mozilla/5.0"})
        data = resp.json()
        return data.get("class", [])
    except:
        return []

def match_category(cat_name, keywords):
    for kw in keywords:
        if kw in cat_name:
            return True
    return False

def is_adult_category(cat_name):
    for kw in ADULT_KEYWORDS:
        if kw in cat_name:
            return True
    return False

def fetch_from_source(api, category_id=None, page=1, limit=30):
    try:
        params = {"ac": "detail", "pg": page, "limit": limit}
        if category_id:
            params["t"] = category_id
        resp = requests.get(api, params=params, timeout=10,
                          headers={"User-Agent": "Mozilla/5.0"})
        data = resp.json()
        return data.get("list", []), data.get("pagecount", 1)
    except:
        return [], 1

def fetch_rating(title, retries=2):
    for attempt in range(retries):
        try:
            resp = requests.get(WMDB_API, params={"q": title, "limit": 1},
                               timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            result = resp.json()
            items = result.get("data", [])
            if items and len(items) > 0:
                item = items[0]
                poster = ""
                inner_data = item.get("data", [])
                if inner_data and len(inner_data) > 0:
                    poster = inner_data[0].get("poster", "")
                return {
                    "rating": item.get("doubanRating", ""),
                    "poster": poster
                }
        except:
            if attempt < retries - 1:
                time.sleep(1)
    return {}

def crawl_category(sources, category_type, target_count=50):
    all_movies = []
    
    if category_type == "movies":
        keywords = MOVIE_KEYWORDS
    elif category_type == "tv":
        keywords = TV_KEYWORDS
    else:
        keywords = VARIETY_KEYWORDS
    
    for source in sources:
        api = source.get("api", "")
        name = source.get("name", "")
        if not api:
            continue
        
        categories = fetch_categories(api)
        time.sleep(0.3)
        
        matched_cats = [c for c in categories 
                       if match_category(c.get("type_name", ""), keywords) 
                       and not is_adult_category(c.get("type_name", ""))]
        
        if not matched_cats:
            movies, _ = fetch_from_source(api, page=1, limit=50)
            movies = [m for m in movies if not is_adult_category(m.get("vod_name", ""))]
            for m in movies:
                m["source_name"] = name
                m["cat_name"] = "其他"
            all_movies.extend(movies)
        else:
            for cat in matched_cats[:3]:
                cat_id = cat.get("type_id")
                cat_name = cat.get("type_name", "")
                for pg in range(1, 4):
                    movies, page_count = fetch_from_source(api, category_id=cat_id, page=pg, limit=20)
                    movies = [m for m in movies if not is_adult_category(m.get("vod_name", ""))]
                    for m in movies:
                        m["source_name"] = name
                        m["cat_name"] = cat_name
                    all_movies.extend(movies)
                    if pg >= page_count:
                        break
                    time.sleep(0.3)
    
    seen = set()
    unique = []
    for m in all_movies:
        name = m.get("vod_name", "").strip()
        if name and name not in seen:
            seen.add(name)
            unique.append(m)
    
    unique.sort(key=lambda x: x.get("vod_time", "") or x.get("vod_year", ""), reverse=True)
    
    return unique[:target_count]

def enrich_with_rating(movies):
    enriched = []
    for i, m in enumerate(movies):
        name = m.get("vod_name", "")
        if name:
            info = fetch_rating(name)
            m["rating"] = info.get("rating", "")
            if info.get("poster"):
                m["vod_pic"] = info["poster"]
            if (i + 1) % 10 == 0:
                print(f"    评分进度: {i+1}/{len(movies)}")
        enriched.append(m)
        time.sleep(0.5)
    return enriched

def save_category(movies, filename):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output = []
    for m in movies:
        output.append({
            "vod_id": m.get("vod_id", 0),
            "vod_name": m.get("vod_name", ""),
            "vod_pic": m.get("vod_pic", ""),
            "vod_year": m.get("vod_year", ""),
            "vod_area": m.get("vod_area", ""),
            "vod_remarks": m.get("vod_remarks", ""),
            "vod_class": m.get("cat_name", ""),
            "rating": m.get("rating", ""),
            "source": m.get("source_name", "")
        })
    
    filepath = DATA_DIR / filename
    wrapped = {
        "list": output,
        "page": 1,
        "pagecount": 1,
        "total": len(output)
    }
    filepath.write_text(json.dumps(wrapped, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  保存: {filename} ({len(output)} 部)")

def main():
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    cms_sources = sources_data.get("cms_sources", [])
    
    available = []
    results_file = DATA_DIR / "check_results.json"
    if results_file.exists():
        results = json.loads(results_file.read_text(encoding="utf-8"))
        available_names = {r["name"] for r in results if r["status"] == "ok"}
        available = [s for s in cms_sources if s["name"] in available_names]
    else:
        available = cms_sources
    
    print(f"使用 {len(available)} 个可用源\n")
    
    print("爬取电影...")
    movies = crawl_category(available, "movies", 50)
    movies = enrich_with_rating(movies)
    save_category(movies, "movies.json")
    
    print("\n爬取电视剧...")
    tv = crawl_category(available, "tv", 50)
    tv = enrich_with_rating(tv)
    save_category(tv, "tv.json")
    
    print("\n爬取综艺...")
    variety = crawl_category(available, "variety", 50)
    variety = enrich_with_rating(variety)
    save_category(variety, "variety.json")
    
    print("\n全部完成!")

if __name__ == "__main__":
    main()
