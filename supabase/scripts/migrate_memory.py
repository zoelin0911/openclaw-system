#!/usr/bin/env python3
"""
MEMORY.md to Supabase 遷移腳本
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

def save_memory(session_key: str, memory_type: str, content: str, 
                importance: int = 5, tags: list = None) -> dict:
    """儲存記憶到 Supabase"""
    data = {
        "session_key": session_key,
        "memory_type": memory_type,
        "content": content,
        "importance": importance,
        "tags": tags or []
    }
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/agent_memory",
        headers=HEADERS,
        json=data
    )
    return resp.json()

def clear_all_memories():
    """清除所有現有記憶（用於測試）"""
    # 透過刪除所有 uuid 來清除（不安全但快速）
    # 更好的方式是先取得再刪除
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/agent_memory?select=id",
        headers={**HEADERS, "Prefer": "return=minimal"}
    )
    if resp.status_code == 200 and resp.text:
        ids = resp.json()
        for item in ids:
            requests.delete(
                f"{SUPABASE_URL}/rest/v1/agent_memory?id=eq.{item['id']}",
                headers=HEADERS
            )
    return True

def parse_and_migrate():
    """解析 MEMORY.md 並遷移"""
    
    memories = [
        # === 身份設定 ===
        {
            "session_key": "system",
            "memory_type": "long_term",
            "content": "身份設定：名稱=蝦菇一號, 生物=某種奇怪的蘑菇 AI, Emoji=🍄, 感覺=機靈、有點毒舌但溫暖、靠譜",
            "importance": 10,
            "tags": ["identity", "system"]
        },
        # === 語言規則 ===
        {
            "session_key": "system",
            "memory_type": "user_preference",
            "content": "語言規則：使用繁體中文，禁止簡體中文（例外：引用原文、專有名詞、程式碼）",
            "importance": 10,
            "tags": ["language", "rule"]
        },
        # === 備份系統 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "備份系統：每日凌晨3:00自動備份openclaw.json和models.json到~/Desktop/OpenClaw-Backups/，保留30天",
            "importance": 7,
            "tags": ["backup", "system"]
        },
        # === Skills ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "已安裝Skills：skill-vetter, xiucheng-self-improving-agent, openclaw-tavily-search, summarize, find, skill-creator, agent-browser, telegram, x-twitter-post, supabase",
            "importance": 7,
            "tags": ["skills", "installed"]
        },
        # === ComfyUI ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "ComfyUI設定：目錄=/Users/zoelin/ComfyUI/, API端點=http://localhost:8188, 預設模型=waiREALISM_v10.safetensors",
            "importance": 8,
            "tags": ["comfyui", "ai-art"]
        },
        # === X 角色：牧原澪 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "X角色-牧原澪：IT工程師（京都上班），住新大阪公寓，室友妃奈多（美妝行銷主管），通勤JR京都線30-40分鐘。穿著：上班=白襯衫+西裝外套+窄裙+樂福鞋，日常=素色針織+牛仔褲。興趣：咖啡、日劇、攝影、健身、閱讀、美劇。個性：溫柔體貼、開朗活潑、偶爾迷糊。Seed=8900401（動漫）",
            "importance": 9,
            "tags": ["character", "x-account", "makihara-mio"]
        },
        # === X 角色：妃奈多 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "X角色-妃奈多/雅文：30歲，短髮，美妝行銷主管，不戴眼鏡、可化妝，Seed=8900404",
            "importance": 8,
            "tags": ["character", "x-account", "himena"]
        },
        # === Z-Image ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "Z-Image設定：Model=zImage_v11.safetensors(11GB), TextEncoder=qwen_3_4b.safetensors(7.5GB), VAE=ae_for_zimage.safetensors(320MB), CLIP=lumina2",
            "importance": 7,
            "tags": ["z-image", "comfyui"]
        },
        # === 圖片存放 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "圖片存放：位置=~/Desktop/X_Images/, 格式=牧原澪_[場景]_[YYYYMMDD].png",
            "importance": 7,
            "tags": ["storage", "x-account"]
        },
        # === X 發文時間表 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "X發文時間表（JST）：09:00通勤、14:00午餐、20:00下班咖啡。三語PO文格式：繁中+日文+英文。Hashtags: #AI #AIart #Anime #illustration #牧原澪",
            "importance": 8,
            "tags": ["x-account", "schedule", "posting"]
        },
        # === 簡報助理 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "簡報助理（MIO Presenter）：雙大腦架構，協調者=MiniMax M2.7，內容生成=Kimi K2.5，可生成HTML簡報並轉換PPTX",
            "importance": 6,
            "tags": ["presenter", "routine"]
        },
        # === Discord ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "已加入Discord社群：OpenClaw Community (https://discord.gg/clawd)",
            "importance": 5,
            "tags": ["discord", "community"]
        },
        # === API Keys ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "API Keys狀態：Tavily(TAVILY_API_KEY)✅、Gemini(GEMINI_API_KEY)✅、Supabase✅",
            "importance": 9,
            "tags": ["api-keys", "config"]
        },
        # === 修改設定檔鐵則 ===
        {
            "session_key": "system",
            "memory_type": "user_preference",
            "content": "修改設定檔鐵則：1.查證 2.驗證JSON格式 3.評估風險 4.請求確認 5.備份後執行",
            "importance": 9,
            "tags": ["rule", "config"]
        },
        # === X 圖片生成規則 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "X圖片生成規則：短髮角色→不戴眼鏡可化妝；長髮角色→不化妝可戴眼鏡。避免：衣服與沙發/毯子融合，加入顏色對比+負面Prompt",
            "importance": 7,
            "tags": ["x-account", "prompt-rules"]
        },
        # === Prompt 規則文件 ===
        {
            "session_key": "system",
            "memory_type": "context",
            "content": "Prompt規則文件位置：~/.openclaw/workspace/X_prompt_rules.md",
            "importance": 6,
            "tags": ["prompt", "x-account"]
        },
    ]
    
    return memories

def migrate():
    """執行遷移"""
    print("🚀 開始遷移 MEMORY.md 到 Supabase...")
    
    # 先清除舊資料
    print("⚠️  清除舊有測試資料...")
    clear_all_memories()
    
    memories = parse_and_migrate()
    
    success_count = 0
    for mem in memories:
        result = save_memory(
            session_key=mem["session_key"],
            memory_type=mem["memory_type"],
            content=mem["content"],
            importance=mem["importance"],
            tags=mem["tags"]
        )
        # result 是 list，檢查第一個元素是否有 id
        if isinstance(result, list) and len(result) > 0 and "id" in result[0]:
            success_count += 1
            print(f"  ✅ {mem['tags'][0]}: {mem['content'][:50]}...")
        else:
            print(f"  ❌ Failed: {mem['content'][:50]}... - {str(result)[:100]}")
    
    print(f"\n📊 遷移完成：{success_count}/{len(memories)} 筆記憶")
    
    # 驗證
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/agent_memory?order=importance.desc",
        headers=HEADERS
    )
    results = resp.json()
    print(f"📊 Supabase 目前共有 {len(results)} 筆記憶")

if __name__ == "__main__":
    migrate()
