#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path
from datetime import datetime

SOURCES_FILE = Path("scripts/sources.json")
OUTPUT_FILE = Path("tvbox.json")

FTY_CONFIG_URL = "https://gh-proxy.com/https://raw.githubusercontent.com/qist/tvbox/master/fty.json"

def generate():
    print("下载饭太硬配置...")
    req = urllib.request.Request(FTY_CONFIG_URL)
    with urllib.request.urlopen(req, timeout=30) as resp:
        config = json.loads(resp.read().decode("utf-8"))
    
    config["sites"][0]["name"] = "🐱八宝"
    
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    cms_sources = sources_data.get("cms_sources", [])
    
    for source in cms_sources:
        config["sites"].append({
            "key": f"cms_{source['name']}",
            "name": f"📺{source['name']}",
            "type": 1,
            "api": source["api"],
            "searchable": 1,
            "quickSearch": 1
        })
    
    config["_lastUpdate"] = datetime.now().isoformat()
    
    OUTPUT_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"配置生成完成:")
    print(f"  饭太硬源: {len(config['sites']) - len(cms_sources)} 个")
    print(f"  CMS源: {len(cms_sources)} 个")
    print(f"  输出: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
