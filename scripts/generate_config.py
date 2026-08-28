#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

SOURCES_FILE = Path("scripts/sources.json")
OUTPUT_FILE = Path("tvbox.json")

DRPY_RUNTIME = "./lib/drpy2.min.js"

def generate():
    sites = [
        {"key":"drpy_八小喵","name":"🐱八小喵","type":3,"api":DRPY_RUNTIME,"ext":"./js/LIBVIO.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_快看","name":"🎬快看┃热播","type":3,"api":DRPY_RUNTIME,"ext":"./js/快看.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_Auete","name":"🏝Auete┃多线","type":3,"api":DRPY_RUNTIME,"ext":"./js/Auete.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_cokemv","name":"🍫cokemv┃高清","type":3,"api":DRPY_RUNTIME,"ext":"./js/cokemv.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_voflix","name":"🌊voflix┃热播","type":3,"api":DRPY_RUNTIME,"ext":"./js/voflix.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_爱看","name":"👀爱看┃热播","type":3,"api":DRPY_RUNTIME,"ext":"./js/爱看.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_酷云77","name":"☁️酷云77┃热播","type":3,"api":DRPY_RUNTIME,"ext":"./js/酷云77.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_南瓜影视","name":"🎃南瓜影视","type":3,"api":DRPY_RUNTIME,"ext":"./js/南瓜影视.js","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_量子影视","name":"⚛️量子影视","type":3,"api":DRPY_RUNTIME,"ext":"./js/量子影视.js","searchable":1,"quickSearch":1,"changeable":0},
    ]
    
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    cms_sources = sources_data.get("cms_sources", [])
    
    for source in cms_sources:
        sites.append({
            "key": f"cms_{source['name']}",
            "name": f"📺{source['name']}",
            "type": 1,
            "api": source["api"],
            "searchable": 1,
            "quickSearch": 1
        })
    
    config = {
        "spider": DRPY_RUNTIME,
        "wallpaper": "https://jianbian.chuqiuyu.workers.dev",
        "sites": sites,
        "parses": [
            {"name":"虾米","type":0,"url":"https://jx.xmflv.com/?url="},
            {"name":"PM","type":0,"url":"https://www.playm3u8.cn/jiexi.php?url="},
            {"name":"m3u8","type":0,"url":"https://jx.m3u8.tv/jiexi/?url="},
            {"name":"云解析","type":0,"url":"https://jx.yparse.com/index.php?url="},
        ],
        "lives": [
            {"name":"国内直播","type":0,"url":"https://iptv-org.github.io/iptv/countries/cn.m3u","playerType":2}
        ],
        "_lastUpdate": datetime.now().isoformat(),
        "_stats": {
            "drpy_sources": len(sites) - len(cms_sources),
            "cms_sources": len(cms_sources)
        }
    }
    
    OUTPUT_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"配置生成完成:")
    print(f"  DRPY源: {len(sites) - len(cms_sources)} 个")
    print(f"  CMS源: {len(cms_sources)} 个")
    print(f"  输出: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
