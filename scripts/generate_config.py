#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

SOURCES_FILE = Path("scripts/sources.json")
OUTPUT_FILE = Path("tvbox.json")

BASE_URL = "https://gh-proxy.com/https://raw.githubusercontent.com/yangclaw2026-png/tvbox-home/main"
DRPY_RUNTIME = f"{BASE_URL}/lib/drpy2.min.js"  # hjdhnx版本,依赖已替换为gh-proxy绝对URL
SPIDER_JAR = "./jar/fan.txt"  # 播放器兼容的饭太硬 JAR 相对路径
JAR_CLOUD = {"Cloud-drive": "tvfan/Cloud-drive.txt"}

def js(name):
    return f"{BASE_URL}/js/{name}.js"

def generate():
    sites = [
        # === JAR 源（饭太硬）=== 首页优先
        {"key":"jar_八小喵","name":"🐱八小喵","type":3,"api":"csp_DouDouGuard","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"jar_我的云盘","name":"🗂我的云盘┃网盘","type":3,"api":"csp_MyDriveGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":JAR_CLOUD},
        {"key":"jar_玩偶哥哥","name":"👽玩偶哥哥┃4K网盘","type":3,"api":"csp_WoGGGuard","timeout":30,"searchable":1,"quickSearch":1,"changeable":1,"ext":JAR_CLOUD},
        {"key":"jar2_玩偶哥哥","name":"📦玩偶哥哥┃4K网盘备份","type":3,"api":"csp_WoGGGuard","timeout":30,"searchable":1,"quickSearch":1,"changeable":1,"ext":JAR_CLOUD},
        {"key":"jar_聚剧","name":"💡聚剧┃四盘","type":3,"api":"csp_SeedhubGuard","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"jar_多多","name":"🎯多多┃4K网盘","type":3,"api":"csp_PanWebShare","searchable":1,"quickSearch":1,"filterable":1,"changeable":1},
        {"key":"jar_光影","name":"🌞光影┃多线","type":3,"api":"csp_T4Guard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_原创","name":"👒原创┃多线","type":3,"api":"csp_YCyzGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_厂长","name":"📔厂长┃多线","type":3,"api":"csp_NewCzGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_海绵","name":"🐬海绵┃多线","type":3,"api":"csp_HmysGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_瓜子","name":"👀瓜子┃多线","type":3,"api":"csp_AppgzGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_比特","name":"🍄比特┃多线","type":3,"api":"csp_BttwooGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_糯米","name":"🍓糯米┃多线","type":3,"api":"csp_NmyswvGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_文采","name":"💮文采┃多线","type":3,"api":"csp_JpysGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_热播","name":"📺热播┃多线","type":3,"api":"csp_AppTTGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_视界","name":"🌸视界┃多线","type":3,"api":"csp_App99Guard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_播客","name":"🦊播客┃多线","type":3,"api":"csp_AppSxGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_奥特","name":"🏝奥特┃多线","type":3,"api":"csp_AueteGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_新6V","name":"🧲新6V┃磁力","type":3,"api":"csp_SixVGuard","searchable":1,"quickSearch":1,"changeable":0},
        {"key":"jar_咕咕","name":"🦉咕咕┃动漫","type":3,"api":"csp_AppSxGuard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_巴士","name":"🚌巴士┃动漫","type":3,"api":"csp_Dm84Guard","searchable":1,"quickSearch":1,"changeable":1},
        {"key":"jar_盘搜","name":"🎈盘搜┃四盘","type":3,"api":"csp_S_zpsGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":{"siteUrl":"http://107.173.211.148/"}},
        {"key":"jar_易搜","name":"🦋易搜┃四盘","type":3,"api":"csp_S_zpsGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":{"siteUrl":"https://so.252035.xyz/"}},
        {"key":"jar_盘她","name":"🐌盘她┃夸父","type":3,"api":"csp_YpanSoGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":JAR_CLOUD},
        {"key":"jar_盘他","name":"🐞盘他┃嘟嘟","type":3,"api":"csp_BpanSoGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":JAR_CLOUD},
        {"key":"jar_抠搜","name":"🍄抠抠┃搜搜","type":3,"api":"csp_KkSsGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":JAR_CLOUD},
        {"key":"jar_UC","name":"🌈优汐┃搜搜","type":3,"api":"csp_UuSsGuard","searchable":1,"quickSearch":1,"changeable":0,"ext":JAR_CLOUD},

        # === DRPY 源（官方源）===
        {"key":"drpy_360影视","name":"📺360影视┃官源","type":3,"api":DRPY_RUNTIME,"ext":js("360影视"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_腾云驾雾","name":"🐧腾讯视频┃官源","type":3,"api":DRPY_RUNTIME,"ext":js("腾云驾雾"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_百忙无果","name":"🥭芒果TV┃官源","type":3,"api":DRPY_RUNTIME,"ext":js("百忙无果"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_茶杯狐","name":"🦊茶杯狐┃聚合","type":3,"api":DRPY_RUNTIME,"ext":js("茶杯狐"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_voflix","name":"🌊voflix┃热播","type":3,"api":DRPY_RUNTIME,"ext":js("voflix"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"drpy_荐片","name":"🥝荐片┃主链路","type":3,"api":DRPY_RUNTIME,"ext":js("荐片_new"),"searchable":1,"quickSearch":1,"changeable":0},
        {"key":"jar_荐片_fan","name":"🥝荐片┃饭太硬备用","type":3,"api":"csp_JPJGuard","playerType":1,"searchable":1,"quickSearch":1,"changeable":0},

        # === CMS 源（搜索用）===
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
        # 播放器兼容单一 spider；饭太硬 JAR 已包含主站及荐片备用实现
        "spider": f"{SPIDER_JAR};md5;608d621640f5ed5ae8c78158ca61bff7",
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
                "name":"量子广告",
                "hosts":["vip.lz","hd.lz","v.cdnlz","*"],
                "regex":["18.5333","新葡京","xinpujing","澳门","娱乐城","8888","9999"],
                "script":[]
            },
            {
                "name":"暴风广告",
                "hosts":["bfzy","*"],
                "regex":["#EXT-X-DISCONTINUITY\\r*\\n*#EXTINF:3,[\\s\\S]*?#EXT-X-DISCONTINUITY","新葡京","xinpujing","澳门","娱乐城","8888","9999"],
                "script":[]
            },
            {
                "name":"非凡广告",
                "hosts":["vip.ffzy","hd.ffzy","*"],
                "regex":["25.1","新葡京","xinpujing","澳门","娱乐城"],
                "script":[]
            },
            {
                "name":"光速广告",
                "hosts":["guangsu","api.guangsu","*"],
                "regex":["#EXT-X-DISCONTINUITY\\r*\\n*#EXTINF:3,[\\s\\S]*?#EXT-X-DISCONTINUITY","新葡京","xinpujing","澳门","娱乐城"],
                "script":[]
            },
            {
                "name":"广告屏蔽",
                "hosts":["*"],
                "regex":[".*\\.ad\\..*",".*\\.ads\\..*",".*\\.广告\\..*","新葡京","澳门新葡京","xinpujing","澳门","娱乐城","博彩","赌场"],
                "script":[]
            }
        ],
        "ads":["static-mozai.4gtv.tv","s3t3d2y8.afcdn.net"],
        "lives": [
            # 主列表：保留用户提供的全部新闻频道及其备用地址
            {"name":"新闻直播┃主列表","type":0,"url":"https://angusyang66669999.github.io/TV/live.m3u?v=883","playerType":2},
            # 补充列表：公开 IPv4 频道，提供主列表之外的备用线路
            {"name":"新闻直播┃Hacks补充","type":0,"url":"https://live.hacks.tools/iptv/categories/news.m3u","playerType":2},
            {"name":"中文直播┃Hacks补充","type":0,"url":"https://live.hacks.tools/iptv/languages/zho.m3u","playerType":2},
            {"name":"新闻直播┃IPTV-org补充","type":0,"url":"https://iptv-org.github.io/iptv/categories/news.m3u","playerType":2},
            {"name":"中文直播┃IPTV-org补充","type":0,"url":"https://iptv-org.github.io/iptv/languages/zho.m3u","playerType":2}
            ,{"name":"台湾频道┃测试","type":0,"url":f"{BASE_URL}/live/taiwan-test.m3u","playerType":2}
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
