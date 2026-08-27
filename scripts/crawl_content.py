#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCES_FILE = Path("scripts/sources.json")
DATA_DIR = Path("data")
WMDB_API = "https://api.wmdb.tv/api/v1/movie/search"

# 分类ID映射（大部分CMS站通用）
CATEGORY_MAP = {
    "movies": {"电影": 1},
    "tv": {"国产剧": 2, "港台剧": 3, "日韩剧": 4, "欧美剧": 5, "海外剧": 6},
    "variety": {"综艺": 7}
}

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

def fetch_rating(title):
    try:
        resp = requests.get(WMDB_API, params={"q": title, "limit": 1},
                           timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        data = resp.json()
        if data and len(data) > 0:
            return {
                "rating": data[0].get("doubanRating", ""),
                "poster": data[0].get("img", "")
            }
    except:
        pass
    return {}

def crawl_category(sources, category_type, target_count=50):
    all_movies = []
    
    for source in sources:
        api = source.get("api", "")
        name = source.get("name", "")
        if not api:
            continue
        
        cat_ids = CATEGORY_MAP.get(category_type, {})
        
        for cat_name, cat_id in cat_ids.items():
            movies, _ = fetch_from_source(api, category_id=cat_id, page=1, limit=30)
            for m in movies:
                m["source_name"] = name
                m["cat_name"] = cat_name
            all_movies.extend(movies)
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
        time.sleep(0.3)
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
    filepath.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
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
