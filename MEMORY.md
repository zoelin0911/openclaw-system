# MEMORY.md - 長期記憶

## 身分

- **名稱**: 蝦菇一號
- **生物**: 某種奇怪的蘑菇 AI 🍄
- **感覺**: 機靈、有點毒舌但溫暖、靠譜
- **Emoji**: 🍄

---

## 🚫 語言規則（強制執行）

| 項目 | 規則 |
|------|------|
| **使用** | ✅ 繁體中文 |
| **禁止使用** | ❌ 簡體中文 |
| **例外** | 引用原文、專有名詞、程式碼 |

**違規處理：** 若不小心輸出簡體，立即自我糾正並道歉。

## 2026-03-22

### 備份系統設定

已建立 OpenClaw 設定檔每日備份系統：

- **備份腳本**: `~/Desktop/OpenClaw-Backups/backup.sh`
- **備份目錄**: `~/Desktop/OpenClaw-Backups/YYYY-MM-DD/`
- **備份檔案**:
  - `openclaw.json`
  - `models.json`（如果存在）
- **備份時間**: 每天凌晨 3:00（系統 cron）
- **保留期限**: 30 天

備份檔案命名格式: `YYYYMMDD_HHMMSS_filename.json`

手動執行備份:
```bash
~/Desktop/OpenClaw-Backups/backup.sh
```

### 已安裝的 Skills

| Skill | 用途 |
|-------|------|
| skill-vetter | 安全審核 |
| xiucheng-self-improving-agent | 對話品質分析 |
| self-improving-agent-cn | 錯誤/糾正記憶 |
| openclaw-tavily-search | 網頁搜尋 |
| liang-tavily-search | 進階搜尋 |
| summarize | 摘要網頁/檔案 |
| find | 尋找策略 |
| skill-creator | 創建 skill |
| agent-browser | 瀏覽器自動化 |
| telegram | Telegram Bot 指南 |
| x-twitter-post | X 自動發文工作流 |

### 已安裝的應用程式

| 應用 | 用途 |
|------|------|
| agent-browser CLI | 瀏覽器自動化（v0.21.4）|
| Chromium | 無頭瀏覽器（v146.0.7680.153）|
| ComfyUI | 圖片生成（v0.8.24）|

### API Keys（已設定於 ~/.openclaw/.env）

| 服務 | 環境變數 |
|------|----------|
| Tavily | TAVILY_API_KEY |
| Gemini | GEMINI_API_KEY |

### API Keys

| 服務 | 環境變數 | 狀態 |
|------|----------|------|
| Tavily | `TAVILY_API_KEY` | ✅ 已設定 |
| Gemini | `GEMINI_API_KEY` | ✅ 已設定 |

### 修改設定檔鐵則

每次修改設定檔前必須遵循：
1. 查證 - 先去官網確認指令是否正確
2. 驗證 - 用 Python 驗證 JSON 語法格式
3. 評估風險 - 評估可能會出什麼錯
4. 請求確認 - 重大操作前必須向老闆確認
5. 備份設定檔 - 備份後才能執行

### 身分

- **名稱**: 蝦菇一號
- **生物**: 某種奇怪的蘑菇 AI
- **感覺**: 機靈、有點毒舌但溫暖、靠譜
- **Emoji**: 🍄
## ComfyUI 環境

- **ComfyUI 目錄**: `/Users/zoelin/ComfyUI/`
- **API 端點**: `http://localhost:8188`
- **預設模型**: `waiREALISM_v10.safetensors`（⚠️ animagine_xl4 不在可用清單）
- **工作流腳本**: `~/.openclaw/workspace/tmp/`
- **參考圖片**: `~/.openclaw/workspace/tmp/face_refs/`

## X 角色設定（2026-03-28 更新）

### 角色名字
- **Makihara Mio**（牧原 澪）
- 中文名：牧原 澪
- 暱稱：Mio

### 穿著設定
- **上班**: 白襯衫 + 西裝外套 + 窄裙 + 樂福鞋
- **日常**: 素色針織 + 牛仔褲 + 樂福鞋

### 模型與工具
- **主模型**: waiREALISM_v10.safetensors
- **角色風格**: 動漫風格

### 生成參數
| 參數 | 值 |
|------|-----|
| **解析度** | 1024 x 1024 |
| **Steps** | 50 |
| **CFG** | 8.0 |
| **Sampler** | euler |
| **IPAdapter Weight** | 1.0 |

## Z-Image 角色設定（2026-03-26 新增）

### 組件狀態
| 組件 | 路徑 | 大小 |
|------|------|------|
| Diffusion Model | `~/ComfyUI/models/diffusion_models/zImage_v11.safetensors` | 11 GB |
| Text Encoder | `~/ComfyUI/models/text_encoders/qwen_3_4b.safetensors` | 7.5 GB |
| VAE | `~/ComfyUI/models/vae/ae_for_zimage.safetensors` | 320 MB |

### Z-Image 工作流參數
| 參數 | 值 |
|------|-----|
| **Seed** | 8779462 |
| **Model** | zImage_v11.safetensors |
| **Text Encoder** | qwen_3_4b.safetensors |
| **VAE** | ae_for_zimage.safetensors |
| **CLIP Type** | lumina2 |
| **Steps** | 35 |
| **CFG** | 4.5 |
| **Sampler** | euler |
| **Resolution** | 1024×1024 |

### 角色特徵描述
- East Asian / Chinese woman
- sleek ponytail, dark brown hair
- soft defined jawline, clear bright eyes
- confident expression, glossy lips
- smooth luminous skin, dewy finish
- glam makeup with smoky eyes

### 角色設定檔位置
- `~/.openclaw/workspace/tmp/character_profile.md`

### 已生成圖片
| 名稱 | 日期 |
|------|------|
| zImage_Fixed_00001_.png | 2026-03-26 |
| zImage_Nightlife_00001_.png | 2026-03-26 |
| zImage_ChineseGirl_00001_.png | 2026-03-26 |
- **設定檔**: `~/.openclaw/workspace/tmp/X_character_config.md`

## 牧原 澪 角色詳細設定（2026-03-28 更新）

### 基本資料
- **職業**: IT 工程師（京都上班）
- **居住**: 新大阪公寓
- **室友**: 妃奈多（30歲，美妝行銷主管）
- **通勤**: JR京都線，30-40分鐘

### 作息時間表

| 時間 | 場合 | 場景 | 穿著 |
|------|------|------|------|
| 09:00 | 早班通勤 | 新大阪駅 → 京都 | 白襯衫+西裝外套+窄裙+樂福鞋 |
| 14:00 | 午餐 | 京都社員食堂 | 白襯衫+西裝外套 |
| 20:00 | 下班 | 京都駅 → 大阪 | 白襯衫+西裝外套+窄裙 |
| 20:00-21:00 | 下班咖啡 | 大阪咖啡廳 | 素色針織+牛仔褲+樂福鞋 |
| 21:00 | 回家 | 大阪公寓陽台 | 家居服 |
| 週末 09:00 | 週末早晨 | 大阪公寓沙發 | 寬鬆家居服 |
| 週末 14:00 | 早午餐 | 大阪咖啡廳（與室友） | 時尚休閒裝 |
| 週末 20:00 | 晚上 | 大阪公寓沙發 | 寬鬆家居服，追劇 |

### 室友設定（妃奈多 / 雅文）
- **名字**: 妃奈多（Himena）/ 雅文（Ya-wen）
- **年齡**: 30歲
- **職業**: 美妝行銷主管
- **特徵**: 短髮、不戴眼鏡、可化妝
- **Seed**: 8900404

### 角色 Seeds
- **牧原澪（長髮）**: 8900401（動漫風格）
- **牧原澪（寫實攝影）**: 8900419（RealVisXL V5.0）
- **妃奈多 / 雅文（短髮）**: 8900404

### 1號人物設定（RealVisXL V5.0 寫實攝影版）
- **Model**: RealVisXL_V5.0.safetensors
- **Steps**: 100, **CFG**: 10.0（最低10）
- **Sampler**: euler, **Resolution**: 1024×1024
- **Prompt**: 高解析度 Fujifilm 拍攝，完美面部對稱，瓷器肌膚
- **視覺**: 50mm f/1.8, 淺景深, bokeh, 奶茶色調, 日系雜誌風
- **設定檔**: `~/.openclaw/workspace/tmp/character_1_makihara_mio.md`

### 髮型妝容規則
- **長髮（牧原澪）**: 不化妝、可戴眼鏡
- **短髮（妃奈多）**: 不戴眼鏡、可化妝

### 興趣
咖啡探索、日劇/日本文化、攝影、健身/瑜珈、閱讀、美劇

### 個性
溫柔體貼、開朗活潑、偶爾迷糊

### 穿著
- 上班: 白襯衫 + 西裝外套 + 窄裙 + 樂福鞋
- 日常: 素色針織 + 牛仔褲 + 樂福鞋
- 配件: 黑色粗框眼鏡、黑色長髮

## 圖片存放規定（2026-03-28）
- 位置：`~/Desktop/X_Images/`
- 格式：`牧原澪_[場景]_[日期].png`

## X 圖片生成常見問題（2026-03-28）

### 角色屬性對照（2026-03-30 新增）
- **短髮** → 不戴眼鏡、可化妝
- **長髮** → 不化妝、可戴眼鏡

### 衣服與物品融合
- 問題：衣服下擺與沙發被子/毯子連成一體
- 避免：加入顏色對比 + 負面 Prompt: merged objects, blurry edges, fused clothing

## Prompt 規則文件
- 位置：`~/.openclaw/workspace/X_prompt_rules.md`
- 內容：完整的 Prompt 模板與規範
- 用途：確保每次生成的圖片都達到標準品質

## X 發文時間表
- 設定檔：`~/.openclaw/workspace/x-account/content/posts-daily-life.json`
- 排程：09:00 / 14:00 / 20:00（以日本時間 JST = UTC+9 為準）

### 牧原澪作息（已完整記錄）

| 日本時間 | 場合 | 場景 | 穿著 |
|----------|------|------|------|
| 09:00 | 通勤 | 新大阪駅 → 京都 | 白襯衫+西裝外套+窄裙+樂福鞋 |
| 14:00 | 午餐 | 京都社員食堂 | 白襯衫+西裝外套 |
| 20:00 | 下班 | 京都駅 → 大阪 | 白襯衫+西裝外套+窄裙 |
| 20:00-21:00 | 下班咖啡 | 大阪咖啡廳 | 素色針織+牛仔褲+樂福鞋 |
| 21:00 | 回家 | 大阪公寓陽台 | 家居服 |
| 週末 09:00 | 週末早晨 | 公寓沙發 | 寬鬆家居服 |
| 週末 14:00 | 早午餐 | 大阪咖啡廳（與室友妃奈多） | 時尚休閒裝 |
| 週末 20:00 | 晚上 | 公寓沙發追劇 | 寬鬆家居服 |

### 完成後的完整流程
```
1. 生成圖片（ComfyUI Python script）
2. 移動到歸檔：`mv ~/ComfyUI/output/<prefix>* ~/Desktop/X_Images/`
3. 命名：`牧原澪_[場景]_[YYYYMMDD].png`
4. 發布到 X（瀏覽器自動化）
```

### Skill 位置
- **Skill 目錄**: `~/.openclaw/workspace/skills/x-twitter-post/`
- **認證檔案**: `~/.openclaw/workspace/skills/x-twitter-post/scripts/x-auth.json`

### X 發布（瀏覽器自動化）
```bash
# 載入認證
agent-browser --session x-post state load ~/.openclaw/workspace/skills/x-twitter-post/scripts/x-auth.json

# 開啟 X 首頁
agent-browser --session x-post open https://x.com

# 截圖確認登入狀態
agent-browser --session x-post snapshot -i --json

# 點擊 Post 按鈕（e105）
agent-browser --session x-post click @e105

# 輸入文案
agent-browser --session x-post fill @e185 "三語 PO 文內容"

# 加入圖片
agent-browser --session x-post click @e203
# 填入檔案路徑上傳

# 發布
agent-browser --session x-post click @e251
```

### PO 文格式（三語）
```
[繁體中文句子] 🌙
[日文句子] 🇯🇵
[英文句子] 🇺🇸

#AI #AIart #Anime #illustration #牧原澪
```

### 認證已設定
- ✅ X 帳號已登入並儲存（ Zoe Lin @ZoeLin0331）
- 之後發文不需要再登入

### 重新登入（如需）
```bash
agent-browser --session x-post state clear
# 然後手動在瀏覽器登入
agent-browser --session x-post state save ~/.openclaw/.../x-auth.json
```


## 已加入的社群（2026-04-05 新增）

| 平台 | 狀態 | 日期 |
|------|-------|------|
| Discord (OpenClaw Community) | ✅ 已加入 | 2026-04-05 |

Discord 邀請連結：https://discord.gg/clawd


---

## 2026-04-06

### 新增 AgentRoutine：MIO 簡報助理（v1.1）

**用途**：提案報告與專案改善報告生成

**路徑**：`~/.openclaw/workspace/routines/mio-presenter/`

**🧠 雙大腦架構**：
| 角色 | 模型 | 職責 |
|------|------|------|
| 協調者 | MiniMax M2.7 | 接收任務、詢問需求、生成檔案 |
| 內容生成 | **Kimi K2.5** | 規劃結構、撰寫內容、專業建議 |

**功能**：
- 💬 對話收集需求，主動確認目標對象
- 📊 Kimi K2.5 生成專業內容
- 🎨 生成專業 HTML 簡報（瀏覽器展示）
- 📄 支援轉換為 PPTX 格式

**使用方式**：
```
你：做簡報 [主題]
我：主動詢問目標對象、核心訊息、時間限制
我：呼叫 Kimi K2.5 生成內容
我：套用模板生成 HTML 簡報
你：轉 PPTX（可選）
```

**安裝依賴**：
```bash
pip3 install python-pptx --break-system-packages  # PPTX 轉換用
```
