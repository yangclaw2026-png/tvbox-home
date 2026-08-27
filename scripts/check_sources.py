#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path

SOURCES_FILE = Path("scripts/sources.json")
RESULTS_FILE = Path("data/check_results.json")

def check_source(source, timeout=8):
    api_url = source.get("api", "")
    name = source.get("name", "")
    
    if not api_url:
        return {"name": name, "status": "no_api", "type": source.get("type", "")}
    
    try:
        start = time.time()
        resp = requests.get(api_url, params={"ac": "detail", "pg": 1, "limit": 1},
                          timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        latency = round((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                if "list" in data or "class" in data:
                    return {"name": name, "status": "ok", "latency": latency, "type": source.get("type", "")}
            except:
                pass
        
        return {"name": name, "status": "error", "latency": latency, "type": source.get("type", "")}
    except requests.exceptions.Timeout:
        return {"name": name, "status": "timeout", "type": source.get("type", "")}
    except Exception as e:
        return {"name": name, "status": f"error: {str(e)[:30]}", "type": source.get("type", "")}

def main():
    sources_data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    all_sources = sources_data.get("cms_sources", []) + sources_data.get("pan_sources", [])
    
    results = []
    print(f"检测 {len(all_sources)} 个源...")
    
    for source in all_sources:
        result = check_source(source)
        icon = "✅" if result["status"] == "ok" else "❌"
        print(f"  {icon} {result['name']}: {result['status']}")
        results.append(result)
    
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    
    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"\n检测完成: {ok_count}/{len(results)} 个源可用")

if __name__ == "__main__":
    main()
