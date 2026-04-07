#!/usr/bin/env python3
"""
ComfyUI 生成日誌系統
"""

import os
import json
import requests
from datetime import datetime

SUPABASE_URL = "https://sgmasjasaemzzvgqiocs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNnbWFzamFzYWVtenp2Z3Fpb2NzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTU0NjE5MiwiZXhwIjoyMDkxMTIyMTkyfQ.714sECDxD8KayHkt82WPm5zdkH2RY-u7X6d67O-hxRg"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

COMFYUI_API = "http://localhost:8188"

def log_task(task_type: str, task_name: str, status: str,
            payload: dict = None, result: dict = None,
            error_message: str = None, duration_ms: int = None) -> dict:
    """記錄任務到 Supabase"""
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
            timeout=5
        )
        return {"success": True, "source": "supabase", "data": resp.json()}
    except Exception as e:
        print(f"⚠️  Supabase 寫入失敗: {e}")
        return {"success": False, "source": "failed", "error": str(e)}

def check_comfyui_status():
    """檢查 ComfyUI 狀態"""
    try:
        resp = requests.get(f"{COMFYUI_API}/system_stats", timeout=3)
        if resp.status_code == 200:
            return {"running": True, "status": "ok"}
        return {"running": False, "status": f"HTTP {resp.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"running": False, "status": "not_running"}
    except Exception as e:
        return {"running": False, "status": str(e)}

def get_queue_status():
    """取得隊列狀態"""
    try:
        resp = requests.get(f"{COMFYUI_API}/queue", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "running": len(data.get("queue_running", [])),
                "pending": len(data.get("queue_pending", []))
            }
    except:
        pass
    return {"running": 0, "pending": 0}

def log_generation(prompt: str, model: str, seed: int, 
                   steps: int, cfg: float, resolution: str,
                   status: str, output_path: str = None,
                   error_message: str = None, duration_ms: int = None):
    """記錄一次生成任務"""
    return log_task(
        task_type="comfyui",
        task_name="image_generation",
        status=status,
        payload={
            "prompt": prompt[:500] if prompt else None,
            "model": model,
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "resolution": resolution
        },
        result={
            "output_path": output_path
        },
        error_message=error_message,
        duration_ms=duration_ms
    )

def get_generation_history(limit: int = 20):
    """取得生成歷史"""
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/task_logs?task_type=eq.comfyui&order=created_at.desc&limit={limit}",
            headers=HEADERS
        )
        return resp.json()
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_generation_stats():
    """取得生成統計"""
    history = get_generation_history(100)
    total = len(history)
    success = len([x for x in history if x["status"] == "success"])
    failed = len([x for x in history if x["status"] == "failed"])
    
    return {
        "total": total,
        "success": success,
        "failed": failed,
        "success_rate": f"{(success/total*100):.1f}%" if total > 0 else "N/A"
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("ComfyUI Generation Logger")
        print("Usage:")
        print("  comfyui_logger.py status           - Check ComfyUI status")
        print("  comfyui_logger.py history [limit] - Show generation history")
        print("  comfyui_logger.py stats            - Show statistics")
        print("  comfyui_logger.py log <json>       - Log a generation")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        status = check_comfyui_status()
        queue = get_queue_status()
        print(f"ComfyUI: {'✅ Running' if status['running'] else '❌ Not Running'}")
        print(f"Status: {status['status']}")
        print(f"Queue: {queue['running']} running, {queue['pending']} pending")
    
    elif cmd == "history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        history = get_generation_history(limit)
        print(f"\n📊 Generation History ({len(history)} records)")
        print("-" * 60)
        for item in history[:limit]:
            status_icon = "✅" if item["status"] == "success" else "❌"
            model = item["payload"].get("model", "unknown")
            time = item["created_at"][:19]
            print(f"{status_icon} {time} | {model} | {item['status']}")
    
    elif cmd == "stats":
        stats = get_generation_stats()
        print(f"\n📊 Generation Statistics")
        print("-" * 40)
        print(f"Total:   {stats['total']}")
        print(f"Success: {stats['success']} {stats['success_rate']}")
        print(f"Failed:  {stats['failed']}")
    
    elif cmd == "log":
        if len(sys.argv) < 3:
            print("Usage: comfyui_logger.py log <json_data>")
            sys.exit(1)
        try:
            data = json.loads(sys.argv[2])
            result = log_generation(**data)
            print(f"✅ Logged: {result}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON")
    
    else:
        print(f"Unknown command: {cmd}")
