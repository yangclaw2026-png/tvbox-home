#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
SOURCES_FILE = Path("scripts/sources.json")

SPIDER_URL = "./lib/pg.jar"

DRPY_RUNTIME = "./lib/drpy2.min.js"

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
            "name": "搜索 | 豆瓣榜单[js]",
            "type": 3,
            "api": DRPY_RUNTIME,
            "ext": "./js/ranking.js",
            "searchable": 1,
            "quickSearch": 1
        }
    ]
    
    for source in cms_sources:
        sites.append({
            "key": f"cms_{source['name']}",
            "name": f"影视 | {source['name']}",
            "type": 1,
            "api": source["api"],
            "searchable": 1,
            "quickSearch": 1
        })
    
    config = {
        "spider": SPIDER_URL,
        "wallpaper": "https://jianbian.chuqiuyu.workers.dev",
        "sites": sites,
        "parses": [
            {"name": "Json聚合", "type": 3, "url": "Demo"},
            {"name": "虾米", "type": 0, "url": "https://jx.xmflv.com/?url="},
            {"name": "PM", "type": 0, "url": "https://www.playm3u8.cn/jiexi.php?url=", "ext": {"flag": ["qiyi", "imgo", "youku", "qq", "letv", "sohu", "bilibili", "mgtv"]}},
            {"name": "m3u8", "type": 0, "url": "https://jx.m3u8.tv/jiexi/?url="},
            {"name": "云解析", "type": 0, "url": "https://jx.yparse.com/index.php?url="},
            {"name": "巧技", "type": 1, "url": "http://pan.qiaoji8.com/tvbox/neibu.php?url=", "ext": {"flag": ["qq", "youku", "qiyi", "mgtv", "bilibili"]}}
        ],
        "lives": [
            {
                "name": "国内直播",
                "type": 0,
                "url": "https://iptv-org.github.io/iptv/countries/cn.m3u",
                "playerType": 2,
                "epg": "http://epg.112114.xyz/?ch={name}&date={date}",
                "logo": "https://epg.112114.xyz/logo/{name}.png"
            }
        ],
        "rules": [
            {"name": "磁力廣告", "hosts": ["magnet"], "regex": ["更多", "社區", "直播", "更新", "社区", "有趣", "英皇体育", "澳门皇冠赌场"]},
            {"name": "暴風", "hosts": ["bfzy"], "regex": ["#EXT-X-DISCONTINUITY\\r*\\n*#EXTINF:3,[\\s\\S]*?#EXT-X-DISCONTINUITY"]},
            {"name": "量子", "hosts": ["vip.lz", "hd.lz", "v.cdnlz"], "regex": ["18.5333"]},
            {"name": "非凡", "hosts": ["vip.ffzy", "hd.ffzy"], "regex": ["25.1"]}
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
    print(f"  CMS源: {len(cms_sources)} 个 type 1 源")
    print(f"  输出: {config_file}")

if __name__ == "__main__":
    generate()
