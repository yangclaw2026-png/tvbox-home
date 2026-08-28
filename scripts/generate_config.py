#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
SOURCES_FILE = Path("scripts/sources.json")

GITHUB_USER = "yangclaw2026-png"
GITHUB_REPO = "tvbox-home"
GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main"

SPIDER_URL = f"https://ghproxy.cn/https://raw.githubusercontent.com/gaotianliuyun/gao/master/lib/spider.jar"

DRPY_RUNTIME = "https://raw.githubusercontent.com/hjdhnx/drpy-node/main/js/drpy2.min.js"

def load_category(filename):
    filepath = DATA_DIR / filename
    if filepath.exists():
        return json.loads(filepath.read_text(encoding="utf-8"))
    return []

def generate():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    movies = load_category("movies.json")
    tv = load_category("tv.json")
    variety = load_category("variety.json")
    
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    cms_sources = sources_data.get("cms_sources", [])
    
    sites = [
        {
            "key": "drpy_js_ranking",
            "name": "📊 豆瓣榜单",
            "type": 3,
            "api": DRPY_RUNTIME,
            "ext": f"{GITHUB_RAW}/js/ranking.js",
            "searchable": 1,
            "quickSearch": 1
        }
    ]
    
    for i, source in enumerate(cms_sources):
        js_file = source.get("js_file", f"{source['name']}.js")
        sites.append({
            "key": f"drpy_js_{source['name']}",
            "name": f"🔍 {source['name']}",
            "type": 3,
            "api": DRPY_RUNTIME,
            "ext": f"{GITHUB_RAW}/js/{js_file}",
            "searchable": 1,
            "quickSearch": 1
        })
    
    config = {
        "spider": SPIDER_URL,
        "sites": sites,
        "parses": [
            {"name": "解析聚合", "type": 3, "url": "Web"},
            {"name": "全能解析1", "type": 1, "url": "https://jx.777jiexi.com/player/?url=", "ext": {"flag": ["qq", "mgtv", "qiyi", "youku"]}},
            {"name": "全能解析2", "type": 1, "url": "https://jx.jsonplayer.com/player/?url=", "ext": {"flag": ["qq", "mgtv", "qiyi", "youku"]}}
        ],
        "lives": [
            {
                "name": "国内直播",
                "type": 0,
                "url": "https://iptv-org.github.io/iptv/countries/cn.m3u",
                "playerType": 1
            }
        ],
        "_lastUpdate": datetime.now().isoformat(),
        "_stats": {
            "movies": len(movies),
            "tv": len(tv),
            "variety": len(variety),
            "sources": len(cms_sources) + 1
        }
    }
    
    config_file = OUTPUT_DIR / "tvbox.json"
    config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"配置生成完成:")
    print(f"  排行榜: DRPY type 3 源")
    print(f"  CMS源: {len(cms_sources)} 个 DRPY type 3 源")
    print(f"  输出: {config_file}")

if __name__ == "__main__":
    generate()
