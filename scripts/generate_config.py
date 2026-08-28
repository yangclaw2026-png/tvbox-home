#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
SOURCES_FILE = Path("scripts/sources.json")

DRPY_RUNTIME = "./lib/drpy2.min.js"
SPIDER_URL = "./lib/pg.jar"

def load_category(filename):
    filepath = DATA_DIR / filename
    if filepath.exists():
        return json.loads(filepath.read_text(encoding="utf-8"))
    return []

def generate():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    cms_sources = sources_data.get("cms_sources", [])
    
    sites = [
        {"key":"drpy_js_豆瓣","name":"搜索 | 豆瓣[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/drpy.js","searchable":1,"quickSearch":0,"changeable":0},
        {"key":"drpy_js_荐片","name":"影视 | 荐片[js]","type":3,"api":DRPY_RUNTIME,"searchable":1,"quickSearch":1,"changeable":1,"ext":"./js/荐片.js", "timeout":30},
        {"key":"drpy_js_酷云77","name":"影视 | 酷云77[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/酷云77.js"},
        {"key":"drpy_js_快看","name":"影视 | 快看[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/快看.js"},
        {"key":"drpy_js_爱看","name":"影视 | 爱看[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/爱看.js"},
        {"key":"drpy_js_低端","name":"影视 | 低端[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/低端.js"},
        {"key":"drpy_js_南瓜影视","name":"影视 | 南瓜影视[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/南瓜影视.js"},
        {"key":"drpy_js_Auete","name":"影视 | Auete[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/Auete.js"},
        {"key":"drpy_js_cokemv","name":"影视 | cokemv[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/cokemv.js"},
        {"key":"drpy_js_LIBVIO","name":"影视 | LIBVIO[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/LIBVIO.js"},
        {"key":"drpy_js_voflix","name":"影视 | voflix[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/voflix.js"},
        {"key":"drpy_js_量子影视","name":"影视 | 量子影视[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/量子影视.js"},
        {"key":"drpy_js_369影视","name":"影视 | 369影视[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/369影视.js"},
        {"key":"drpy_js_AGE动漫","name":"动漫 | AGE动漫[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/AGE动漫.js"},
        {"key":"drpy_js_兔小贝","name":"少儿 | 兔小贝[js]","type":3,"api":DRPY_RUNTIME,"style":{"type":"rect","ratio":1.597},"changeable":0,"ext":"./js/兔小贝.js"},
        {"key":"drpy_js_A8音乐","name":"音频 | A8音乐[js]","type":3,"api":DRPY_RUNTIME,"ext":"./js/A8音乐.js"},
        {"key":"drpy_js_斗鱼直播","name":"直播 | 斗鱼[js]","type":3,"api":DRPY_RUNTIME,"style":{"type":"rect","ratio":1.597},"changeable":0,"ext":"./js/斗鱼直播.js"},
        {"key":"drpy_js_虎牙直播","name":"直播 | 虎牙[js]","type":3,"api":DRPY_RUNTIME,"style":{"type":"rect","ratio":1.597},"changeable":0,"ext":"./js/虎牙直播.js"},
        {"key":"drpy_js_好趣网","name":"电视 | 好趣网[js]","type":3,"api":DRPY_RUNTIME,"style":{"type":"rect","ratio":1.333},"changeable":0,"ext":"./js/好趣网.js"},
        {"key":"drpy_js_310直播","name":"体育 | 310直播[js]","type":3,"api":DRPY_RUNTIME,"changeable":0,"style":{"type":"rect","ratio":1},"ext":"./js/310直播.js"},
        {"key":"drpy_js_88看球","name":"体育 | 88看球[js]","type":3,"api":DRPY_RUNTIME,"changeable":0,"style":{"type":"rect","ratio":1},"ext":"./js/88看球.js"},
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
            {"name":"Json聚合","type":3,"url":"Demo"},
            {"name":"虾米","type":0,"url":"https://jx.xmflv.com/?url=","ext":{"flag":["qq","腾讯","qiyi","爱奇艺","youku","优酷","sohu","搜狐","letv","乐视","mgtv","芒果","imgo","bilibili","1905","xigua"]}},
            {"name":"PM","url":"https://www.playm3u8.cn/jiexi.php?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","qq","腾讯","youku","优酷","pptv","letv","乐视","bilibili","mgtv","芒果","sohu","xigua","fun","风行"],"header":{"User-Agent":"Mozilla/5.0"}},"header":{"User-Agent":"Mozilla/5.0"}},
            {"name":"m3u8","type":0,"url":"https://jx.m3u8.tv/jiexi/?url="},
            {"name":"8090","url":"https://www.8090.la/8090/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","qq","腾讯","youku","优酷","pptv","letv","乐视","bilibili","mgtv","芒果","sohu","xigua","fun","风行"],"header":{"User-Agent":"Mozilla/5.0"}},"header":{"User-Agent":"Mozilla/5.0"}},
            {"name":"看看","type":0,"url":"https://jx.m3u8.pw/?url="},
            {"name":"云解析","type":0,"url":"https://jx.yparse.com/index.php?url=","ext":{"header":{"user-agent":"Mozilla/5.0(Linux;Android13;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36"}}},
            {"name":"巧技","type":1,"url":"http://pan.qiaoji8.com/tvbox/neibu.php?url=","ext":{"flag":["qq","腾讯","qiyi","爱奇艺","youku","优酷","sohu","搜狐","letv","乐视","mgtv","芒果","bilibili","1905"],"header":{"User-Agent":"okhttp/4.9.1"}}},
            {"name":"巧技二","type":1,"url":"http://pan.qiaoji8.com/tvbox/gouzi.php?url=","ext":{"flag":["qq","腾讯","qiyi","爱奇艺","youku","优酷","sohu","搜狐","letv","乐视","mgtv","芒果","bilibili","1905","NetFilx"],"header":{"User-Agent":"okhttp/4.9.1"}}}
        ],
        "lives": [
            {"name":"国内直播","type":0,"url":"./list.txt","playerType":2,"epg":"http://epg.112114.xyz/?ch={name}&date={date}","logo":"https://epg.112114.xyz/logo/{name}.png"}
        ],
        "rules": [
            {"name":"磁力廣告","hosts":["magnet"],"regex":["更多","社區","直播","更新","社区","有趣","英皇体育","澳门皇冠赌场"]},
            {"name":"暴風","hosts":["bfzy"],"regex":["#EXT-X-DISCONTINUITY\\r*\\n*#EXTINF:3,[\\s\\S]*?#EXT-X-DISCONTINUITY"]},
            {"name":"量子","hosts":["vip.lz","hd.lz","v.cdnlz"],"regex":["18.5333"]},
            {"name":"非凡","hosts":["vip.ffzy","hd.ffzy"],"regex":["25.1"]}
        ],
        "_lastUpdate": datetime.now().isoformat(),
        "_stats": {
            "drpy_sources": 21,
            "cms_sources": len(cms_sources)
        }
    }
    
    config_file = OUTPUT_DIR / "tvbox.json"
    config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"配置生成完成:")
    print(f"  DRPY源: 21 个")
    print(f"  CMS源: {len(cms_sources)} 个")
    print(f"  输出: {config_file}")

if __name__ == "__main__":
    generate()
