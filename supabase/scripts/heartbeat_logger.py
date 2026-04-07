#!/usr/bin/env python3
"""
Heartbeat 結果寫入 Supabase
"""

import os
import json
import requests
import subprocess
from datetime import datetime

SUPABASE_URL = "https://sgmasjasaemzzvgqiocs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNnbWFzamFzYWVtenp2Z3Fpb2NzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTU0NjE5MiwiZXhwIjoyMDkxMTIyMTkyfQ.714sECDxD8KayHkt82WPm5zdkH2RY-u7X6d67O-hxRg"

# 本地備援檔案
LOCAL_FALLBACK_LOG = "/tmp/heartbeat_fallback.log"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def log_to_local_fallback(data: dict) -> bool:
    """寫入本地備援檔案（Supabase 失敗時使用）"""
    try:
        with open(LOCAL_FALLBACK_LOG, "a") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return True
    except Exception as e:
        print(f"⚠️  本地備援寫入失敗: {e}")
        return False

def log_task(task_type: str, task_name: str, status: str,
            payload: dict = None, result: dict = None,
            error_message: str = None, duration_ms: int = None,
            use_fallback: bool = True) -> dict:
    """記錄任務到 Supabase，失敗時寫入本地備援"""
    data = {
        "task_type": task_type,
        "task_name": task_name,
        "status": status,
        "payload": payload or {},
        "result": result or {}
    }
    if error_message:
        data["error_message"] = error_message
    if duration_ms:
        data["duration_ms"] = duration_ms
    if status in ["success", "failed", "cancelled"]:
        data["completed_at"] = datetime.now().isoformat()
    
    try:
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/task_logs",
            headers=HEADERS,
            json=data,
            timeout=5  # 5秒超時
        )
        if resp.status_code in [200, 201]:
            return {"success": True, "source": "supabase", "data": resp.json()}
        else:
            raise Exception(f"HTTP {resp.status_code}")
    except Exception as e:
        print(f"⚠️  Supabase 寫入失敗: {e}")
        if use_fallback:
            print(f"📝  改寫本地備援: {LOCAL_FALLBACK_LOG}")
            if log_to_local_fallback(data):
                return {"success": True, "source": "local_fallback", "data": data}
        return {"success": False, "source": "failed", "error": str(e)}

def sync_fallback_to_supabase():
    """將本地備援檔案同步到 Supabase"""
    if not os.path.exists(LOCAL_FALLBACK_LOG):
        return {"synced": 0, "failed": 0}
    
    synced = 0
    failed = 0
    lines = []
    
    with open(LOCAL_FALLBACK_LOG, "r") as f:
        lines = f.readlines()
    
    if not lines:
        return {"synced": 0, "failed": 0}
    
    print(f"🔄  发现 {len(lines)} 筆本地備援，開始同步...")
    
    with open(LOCAL_FALLBACK_LOG, "w") as f:
        for line in lines:
            try:
                data = json.loads(line.strip())
                result = log_task(
                    task_type=data.get("task_type", "heartbeat"),
                    task_name=data.get("task_name", "sync"),
                    status=data.get("status", "unknown"),
                    payload=data.get("payload", {}),
                    result=data.get("result", {}),
                    error_message=data.get("error_message"),
                    duration_ms=data.get("duration_ms"),
                    use_fallback=False  # 同步時不用再寫入備援
                )
                if result.get("success"):
                    synced += 1
                else:
                    failed += 1
                    f.write(line)  # 寫回失敗的
            except:
                failed += 1
                f.write(line)
    
    return {"synced": synced, "failed": failed}

def check_gateway_processes() -> dict:
    """檢查 Gateway 進程"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "openclaw"],
            capture_output=True, text=True
        )
        pids = result.stdout.strip().split("\n") if result.stdout.strip() else []
        return {
            "process_count": len(pids) if pids and pids[0] else 0,
            "pids": pids if pids and pids[0] else [],
            "healthy": len(pids) == 1 if pids and pids[0] else False
        }
    except Exception as e:
        return {"error": str(e), "process_count": -1, "healthy": False}

def check_gateway_port() -> dict:
    """檢查 Gateway 端口"""
    try:
        result = subprocess.run(
            ["lsof", "-i", ":18789"],
            capture_output=True, text=True
        )
        listening = "LISTEN" in result.stdout
        return {
            "port_listening": listening,
            "details": result.stdout[:200] if result.stdout else ""
        }
    except Exception as e:
        return {"error": str(e), "port_listening": False}

def check_memory() -> dict:
    """檢查記憶體使用"""
    try:
        result = subprocess.run(
            ["vm_stat"],
            capture_output=True, text=True
        )
        # macOS vm_stat output
        lines = result.stdout.strip().split("\n")
        free = 0
        active = 0
        for line in lines:
            if "Pages free" in line:
                free = int(line.split(":")[1].strip().replace(".", ""))
            if "Pages active" in line:
                active = int(line.split(":")[1].strip().replace(".", ""))
        
        page_size = 4096  # macOS page size
        free_mb = free * page_size / 1024 / 1024
        active_mb = active * page_size / 1024 / 1024
        total_used_mb = active_mb
        
        return {
            "free_mb": round(free_mb, 2),
            "active_mb": round(active_mb, 2),
            "total_used_mb": round(total_used_mb, 2),
            "status": "normal" if total_used_mb < 20480 else "warning" if total_used_mb < 25600 else "error"
        }
    except Exception as e:
        return {"error": str(e)}

def check_comfyui() -> dict:
    """檢查 ComfyUI 運行狀態"""
    try:
        resp = requests.get("http://localhost:8188/system_stats", timeout=3)
        if resp.status_code == 200:
            return {"running": True, "status_code": 200}
        return {"running": False, "status_code": resp.status_code}
    except:
        return {"running": False, "error": "Connection failed"}

def run_heartbeat() -> dict:
    """執行完整心跳檢查並寫入 Supabase"""
    start_time = datetime.utcnow()
    results = {
        "gateway_process": check_gateway_processes(),
        "gateway_port": check_gateway_port(),
        "memory": check_memory(),
        "comfyui": check_comfyui(),
        "timestamp": start_time.isoformat()
    }
    
    # 決定狀態
    all_healthy = (
        results["gateway_process"].get("healthy", False) and
        results["gateway_port"].get("port_listening", False) and
        results["memory"].get("status", "error") != "error" and
        results["comfyui"].get("running", False)
    )
    
    overall_status = "success" if all_healthy else "failed"
    
    # 寫入 Supabase
    log_data = {
        "task_type": "heartbeat",
        "task_name": "system_health_check",
        "status": overall_status,
        "payload": {
            "checks": {
                "gateway_process": results["gateway_process"],
                "gateway_port": results["gateway_port"],
                "memory": results["memory"],
                "comfyui": results["comfyui"]
            }
        },
        "result": {
            "all_healthy": all_healthy,
            "summary": {
                "gateway_process_healthy": results["gateway_process"].get("healthy", False),
                "gateway_port_listening": results["gateway_port"].get("port_listening", False),
                "memory_status": results["memory"].get("status", "unknown"),
                "comfyui_running": results["comfyui"].get("running", False)
            }
        }
    }
    
    end_time = datetime.utcnow()
    duration_ms = int((end_time - start_time).total_seconds() * 1000)
    log_data["duration_ms"] = duration_ms
    
    # 寫入 Supabase（失敗時自動寫入本地備援）
    result = log_task(
        task_type="heartbeat",
        task_name="system_health_check",
        status=overall_status,
        payload={"checks": results},
        result={
            "all_healthy": all_healthy,
            "summary": {
                "gateway_process_healthy": results["gateway_process"].get("healthy", False),
                "gateway_port_listening": results["gateway_port"].get("port_listening", False),
                "memory_status": results["memory"].get("status", "unknown"),
                "comfyui_running": results["comfyui"].get("running", False)
            }
        },
        duration_ms=duration_ms
    )
    
    return {
        "results": results,
        "log_result": result,
        "duration_ms": duration_ms
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "log-only":
            # 只寫入一個簡單的心跳記錄
            result = log_task(
                task_type="heartbeat",
                task_name="system_health_check",
                status="success",
                payload={"source": "cron"},
                result={"message": "Heartbeat completed"}
            )
            print(f"✅ Heartbeat logged ({result.get('source', 'unknown')})")
        elif sys.argv[1] == "sync-fallback":
            # 同步本地備援到 Supabase
            result = sync_fallback_to_supabase()
            print(f"✅ 同步完成: {result['synced']} 筆成功, {result['failed']} 筆失敗")
        elif sys.argv[1] == "check-fallback":
            # 檢查本地備援狀態
            if os.path.exists(LOCAL_FALLBACK_LOG):
                with open(LOCAL_FALLBACK_LOG, "r") as f:
                    lines = f.readlines()
                print(f"📝 本地備援有 {len(lines)} 筆待同步")
            else:
                print("✅ 沒有本地備援，Supabase 正常")
    else:
        # 完整檢查並記錄
        result = run_heartbeat()
        print(f"📊 Heartbeat Result:")
        print(f"   Gateway Process: {'✅' if result['results']['gateway_process'].get('healthy') else '❌'}")
        print(f"   Gateway Port: {'✅' if result['results']['gateway_port'].get('port_listening') else '❌'}")
        print(f"   Memory: {result['results']['memory'].get('status', 'unknown')}")
        print(f"   ComfyUI: {'✅' if result['results']['comfyui'].get('running') else '❌'}")
        print(f"   Duration: {result['duration_ms']}ms")
        print(f"   Logged: {result['log_result'].get('source', 'unknown')}")
