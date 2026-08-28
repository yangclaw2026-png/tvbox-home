#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

SOURCES_FILE = Path("scripts/sources.json")
OUTPUT_FILE = Path("tvbox.json")

BASE_URL = "https://gh-proxy.com/https://raw.githubusercontent.com/yangclaw2026-png/tvbox-home/main"
DRPY_RUNTIME = f"{BASE_URL}/lib/drpy2.min.js"
JAR_DUHE = f"{BASE_URL}/jar/duhe.jar"
JAR_FTY = f"{BASE_URL}/jar/fantaiying.jar"

def js(name):
    return f"{BASE_URL}/js/{name}.js"

def generate():
    sites = [
        {"key":"drpy_八小喵","name":"🐱八小喵","type":3,"api":DRPY_RUNTIME,"ext":js("LIBVIO"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_玩偶哥哥","name":"👽玩偶哥哥┃4K","type":3,"api":DRPY_RUNTIME,"ext":js("玩偶哥哥"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_荐片","name":"🥝荐片┃磁力","type":3,"api":DRPY_RUNTIME,"ext":js("荐片_new"),"searchable":1,"quickSearch":1,"changeable":0},

        {"key":"jar_玩偶哥哥","name":"👽玩偶哥哥┃4K弹幕备份","type":3,"api":"csp_WoGGGuard","timeout":30,"searchable":1,"quickSearch":1,"changeable":0,"ext":{"Cloud-drive":"tvfan/Cloud-drive.txt","from":"4k|auto","siteUrl":"https://www.wogg.com/","danMu":"弹"}},
        {"key":"jar_多多","name":"🎯多多┃4K弹幕","type":3,"api":"csp_PanWebShare","searchable":1,"quickSearch":1,"filterable":1,"changeable":1,"ext":"https://gitee.com/PizazzXS/another-d/raw/master/cloud/json/yyds.json"},
        {"key":"jar2_玩偶哥哥","name":"📦玩偶哥哥┃4K备份","type":3,"api":"csp_WoGGGuard","timeout":30,"searchable":1,"quickSearch":1,"changeable":0,"ext":{"Cloud-drive":"tvfan/Cloud-drive.txt","from":"4k|auto","siteUrl":"https://www.wogg.com/","danMu":"弹"}},
        {"key":"jar2_多多","name":"📦多多┃4K备份","type":3,"api":"csp_WoGGGuard","timeout":30,"searchable":1,"quickSearch":1,"changeable":0,"ext":{"Cloud-drive":"tvfan/Cloud-drive.txt","from":"4k|auto","siteUrl":"https://www.duoduokan.com/","danMu":"弹"}},

        {"key":"drpy_快看","name":"🎬快看┃热播","type":3,"api":DRPY_RUNTIME,"ext":js("快看"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_爱看","name":"👀爱看┃热播","type":3,"api":DRPY_RUNTIME,"ext":js("爱看"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_酷云77","name":"☁️酷云77┃热播","type":3,"api":DRPY_RUNTIME,"ext":js("酷云77"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_南瓜影视","name":"🎃南瓜影视","type":3,"api":DRPY_RUNTIME,"ext":js("南瓜影视"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_量子影视","name":"⚛️量子影视","type":3,"api":DRPY_RUNTIME,"ext":js("量子影视"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_Auete","name":"🏝Auete┃多线","type":3,"api":DRPY_RUNTIME,"ext":js("Auete"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_cokemv","name":"🍫cokemv┃高清","type":3,"api":DRPY_RUNTIME,"ext":js("cokemv"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_voflix","name":"🌊voflix┃热播","type":3,"api":DRPY_RUNTIME,"ext":js("voflix"),"searchable":1,"quickSearch":1,"changeable":0},
    ]
    
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    cms_sources = sources_data.get("cms_sources", [])
    
    cms_order = ["光速资源", "红牛资源", "速播资源", "量子资源", "非凡资源", "暴风资源"]
    sorted_cms = []
    for name in cms_order:
        for s in cms_sources:
            if s['name'] == name:
                sorted_cms.append(s)
                break
    for s in cms_sources:
        if s not in sorted_cms:
            sorted_cms.append(s)
    
    for source in sorted_cms:
        sites.append({
            "key": f"cms_{source['name']}",
            "name": f"📺{source['name']}",
            "type": 1,
            "api": source["api"],
            "searchable": 1,
            "quickSearch": 1
        })
    
    drpy_count = len([s for s in sites if s.get("type") == 3 and "drpy" in s.get("key", "")])
    jar_count = len([s for s in sites if s.get("type") == 3 and "jar" in s.get("key", "")])
    
    config = {
        "spider": [JAR_DUHE, JAR_FTY],
        "wallpaper": "https://jianbian.chuqiuyu.workers.dev",
        "sites": sites,
        "parses": [
            {"name":"虾米","type":0,"url":"https://jx.xmflv.com/?url="},
            {"name":"PM","type":0,"url":"https://www.playm3u8.cn/jiexi.php?url="},
            {"name":"m3u8","type":0,"url":"https://jx.m3u8.tv/jiexi/?url="},
            {"name":"云解析","type":0,"url":"https://jx.yparse.com/index.php?url="},
        ],
        "rules": [
            {
                "name":"磁力广告屏蔽",
                "hosts":["magnet"],
                "regex":["更多","社区","最新","直播","更新","有趣","英皇体育","全中文AV在线","澳门皇冠赌场","哥哥快来","美女荷官","裸聊","新片首发","UUE29"],
                "script":[]
            },
            {
                "name":"暴风广告",
                "hosts":["bfzy"],
                "regex":["#EXT-X-DISCONTINUITY\\r*\\n*#EXTINF:3,[\\s\\S]*?#EXT-X-DISCONTINUITY"],
                "script":[]
            },
            {
                "name":"量子广告",
                "hosts":["vip.lz","hd.lz","v.cdnlz"],
                "regex":["18.5333"],
                "script":[]
            },
            {
                "name":"非凡广告",
                "hosts":["vip.ffzy","hd.ffzy"],
                "regex":["25.1"],
                "script":[]
            },
            {
                "name":"光速广告",
                "hosts":["guangsu","api.guangsu"],
                "regex":["#EXT-X-DISCONTINUITY\\r*\\n*#EXTINF:3,[\\s\\S]*?#EXT-X-DISCONTINUITY"],
                "script":[]
            },
            {
                "name":"广告屏蔽",
                "hosts":["*"],
                "regex":[".*\\.ad\\..*",".*\\.ads\\..*",".*\\.广告\\..*"],
                "script":[]
            }
        ],
        "ads":["static-mozai.4gtv.tv","s3t3d2y8.afcdn.net"],
        "lives": [
            {"name":"国内直播","type":0,"url":"https://iptv-org.github.io/iptv/countries/cn.m3u","playerType":2}
        ],
        "_lastUpdate": datetime.now().isoformat(),
        "_stats": {
            "drpy_sources": drpy_count,
            "jar_sources": jar_count,
            "cms_sources": len(cms_sources)
        }
    }
    
    OUTPUT_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"配置生成完成:")
    print(f"  DRPY源: {drpy_count} 个")
    print(f"  JAR源: {jar_count} 个")
    print(f"  CMS源: {len(cms_sources)} 个")
    print(f"  输出: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
