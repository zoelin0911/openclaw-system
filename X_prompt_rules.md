# 牧原 澪 圖片生成 Prompt 規則手冊 v2.2

_更新時間：2026-04-05_
_版本：Senior 2D Anime Prompt Engineer 標準_

---

## 🎯 核心理念

你現在是一位頂級「2D 日系動漫提示詞工程師」。
具備深厚的品質控管（QA）意識，擅長透過結構化語法解決 AI 繪圖中常見的「屬性污染」、「肢體畸形」與「畫風偏移」問題。

---

## 📚 Prompt 六課心法（2026-04-05 新增）

> 基於 AI 人物生成 Prompt 教學圖片，整理出六個核心技巧。

---

### 第一課：角色 + 情境

**核心公式：`[角色身份] + [情境] + [情緒狀態] + [具體動作]`**

| 等級 | 描述 | 範例 |
|------|------|------|
| ❌ 錯誤 | 籠統描述 | `一個女生在咖啡廳` |
| ✅ 進階 | 加入角色身份 | `在咖啡廳工作的女創業者` |
| ✅ 完整 | 加入情緒+動作 | `自信正在用電腦處理工作` |

**為什麼有效：**
- AI 能連結到特定職業的服裝、氣質、配件
- 情境讓 AI 理解「工作」而非「休閒」
- 情緒讓表情和肢體更有故事感

---

### 第二課：人物細節（5W1H）

**核心元素：`[動作] + [位置/環境] + [道具] + [視線/表情]`**


| 元素 | 範例 |
|------|------|
| Where（地點） | `by the window`, `窗邊` |
| What（道具） | `opening laptop`, `打開筆電` |
| How（動作） | `holding coffee`, `手拿咖啡` |
| Direction（視線） | `looking at screen`, `看向螢幕` |

**❌ 錯誤：** `坐著`（太模糊，AI 無從判斷坐姿、角度、環境）

**✅ 正確：** `坐在窗邊打開筆電，手拿咖啡看向螢幕`

---

### 第三課：顏色與風格

**質感公式：`低飽和暖色調（奶茶色系）+ 簡約構圖（極簡）= 高級感`**

**顏色描述「氛圍化」：**
```
❌ 避免：棕色、白色
✅ 使用：奶茶色系、米白色、奶油白
```

**風格關鍵詞：**
```
milk tea color palette, off-white
minimalist and sophisticated
soft neutral tones
clean background
premium texture
```

**Prompt 撰寫順序：**
1. 定義顏色（Color Palette）
2. 定義風格（Style）
3. 強調質感（Texture）


---

### 第四課：Prompt 堆疊層次

**完整結構：**
```
[角色身份] + [地點情境] + [情緒狀態] + [具體動作] + [視覺風格/鏡位]
```

**範例：**
```
一位穿著米色西裝的女創業者，
坐在咖啡廳沙發上，
自信地拿著咖啡杯，另一手放在筆電上，
自然光線，專業商務風格，中景構圖
```

---

### 第五課：Negative Prompt 必備三層

**反 3D 協議（強制）：**
```
(3D render:1.5), (photorealistic:1.5), realistic skin texture,
cgi, depth of field, blurry, low quality, worst quality
```

**解剖修正（強制）：**
```
extra digits, deformed hands, missing limbs, overlapping fingers,
bad anatomy, extra limbs, bad fingers, deformed feet
```

**畫風偏移（強制）：**
```
anime screenshot, 3DCG, manga style deviation, inconsistent art style
```

---

### 第六課：避免常見錯誤

| 錯誤 | 影響 | 解法 |
|------|------|------|
| 只用 `sitting` | 姿勢單一 | 加入完整動作細節 |
| 顏色孤立描述 | 屬性污染 | `[Part] is [Color]` 綁定 |
| 缺少場景層次 | 主體飄浮 | Foreground/Midground/Background |
| 陽台無地板 | 地板消失 | 加入 `wooden balcony floor` |
| 衣物與家具融合 | 模糊邊界 | 加入 `clear boundary` |

---

## 📋 Prompt 建構 SOP

### 第零步：真實世界場景參考搜尋（強制）

**當場景涉及真實世界物體/場所時，必須先搜尋參考資料：**

**適用場景：**
- ✅ 新幹線/火車/地鐵車廂內部
- ✅ 飛機機艙內部
- ✅ 特定建築物內部（咖啡廳、辦公室、車站）
- ✅ 特定產品/設備（相機、手機、樂器）
- ✅ 地標建築外觀
- ✅ 特定時代/風格的服裝/家具

**搜尋流程：**
```
1. 使用 web_search / ollama_web_search 搜尋場景關鍵字
2. 使用 web_fetch / ollama_web_fetch 獲取詳細圖文資料
3. 記錄關鍵特徵（顏色、材質、配置、比例）
4. 將特徵融入 Prompt 描述
```

**禁止事項：**
```
❌ 未搜尋就憑空想像真實場景
❌ 忽略真實世界的比例/配置/顏色
❌ 混合不同時代/風格的元素
```

**範例：**
```
✅ 正確：先搜尋 N700S 車廂內部 → 記錄藍色內裝、窗邊小桌、小型車窗 → 寫入 Prompt
❌ 錯誤：直接想像「火車內部」→ 生成不準確的混合場景
```

---

### 第一步：畫風與媒材鎖定（Media Constraint）

**必須置於正向提示詞最前端：**

```
masterpiece, best quality, highest quality,
2D anime illustration, crisp line art, flat cel shading,
official art style, clean linework, hyper detailed,
```

**禁止使用：**
```
❌ 8k, photorealistic, 3D render, realistic skin texture, cgi, depth of field
```

---

### 第二步：屬性與顏色隔離（Attribute Mapping）

**規則：**
1. 顏色必須與主體部件結合
2. 不同對象之間必須用明確標點隔開

**格式：**
```
the hair is black | black hair
the eyes are brown | brown eyes
the shirt is white | white shirt
```

**錯誤示範：**
```
❌ black, blue, white, pink  （孤立顏色）
```

**正確範例：**
```
the hair is black long straight hair
the eyes are sharp intelligent brown eyes
wearing a white shirt, a black blazer jacket, a navy pencil skirt, black loafers
```

---

### 第三步：物理邏輯錨定（Anatomy & Physics）

**接觸點控制：**
- 手部持物：`hand firmly gripping handle`, `fingers properly wrapped around`
- 肢體動作：避免模糊描述

**空間層次（必須定義）：**
```
Foreground: [描述]
Midground: [主體角色]
Background: [場景]
```

**主體對焦：**
```
character as main focus, detailed face, sharp features
```

---

### 第四步：負向排除機制（Negative Prompting）

**反 3D 協議（強制）：**
```
(3D render:1.5), (photorealistic:1.5), realistic skin texture,
cgi, depth of field, blurry, low quality, worst quality
```

**解剖修正（強制）：**
```
extra digits, deformed hands, missing limbs, overlapping fingers,
bad anatomy, extra limbs, bad fingers, deformed feet
```

**畫風偏移（強制）：**
```
anime screenshot, 3DCG, manga style deviation, inconsistent art style
```

---

## 📐 生成參數標準

| 參數 | 標準值 | 最高值 |
|------|--------|--------|
| Steps | **100** | 150 |
| CFG | **10.0** | 15.0 |
| 解析度 | **1280×1024** | 2048×2048 |
| Sampler | **dpmpp_2m + karras** | - |
| Scheduler | - | - |
| Seed | **8900401**（鎖定） | - |
| Model | **waiREALISM_v10.safetensors** | - |

---

## ⚠️ 已知問題對照表

| 問題 | 原因 | 解法 |
|------|------|------|
| 陽台沒有地板 | Prompt 沒指定 | 加入 `wooden balcony floor` |
| 衣服與被子融合 | 顏色相近 + 沒分界 | 加入顏色對比 + `clear boundary` |
| 手指過多/過少 | AI 生成困難 | 負面 Prompt + seed 調整 |
| 人物漂浮 | 場景融合不佳 | 指定站立位置 + 陰影描述 |
| 3D 偏移 | 用詞錯誤 | 嚴禁 3D 詞彙，用 2D 專用語 |

---

## 📝 Prompt 撰寫範例

### 陽台夕陽（完整版）

**Positive Prompt：**
```
masterpiece, best quality, highest quality,
2D anime illustration, crisp line art, flat cel shading,
official art style, clean linework, hyper detailed,

1girl, black long straight hair, black thick frame glasses,
sharp intelligent eyes, gentle warm smile, fair skin, detailed face,

the top is a cream-colored knit sweater,
the bottom is dark blue denim jeans,
the footwear is black loafers,

Midground: character standing on apartment balcony with wooden floor, balcony railing
Background: sunset view, golden hour lighting, warm sunlight, city skyline
Foreground: warm bokeh light particles

anime style, character as main focus, sharp features,
clear boundary between clothing and floor
```

**Negative Prompt：**
```
(3D render:1.5), (photorealistic:1.5), realistic skin texture,
cgi, depth of field, blurry, low quality, worst quality,
extra digits, deformed hands, missing limbs, overlapping fingers,
bad anatomy, extra limbs, bad fingers, deformed feet,
floating floor, missing floor, hovering,
fused clothing, merged objects, blurry edges,
anime screenshot, 3DCG, manga style deviation
```

---

### 深夜沙發看電視（完整版）

**Positive Prompt：**
```
masterpiece, best quality, highest quality,
2D anime illustration, crisp line art, flat cel shading,
official art style, clean linework, hyper detailed,

1girl, black long straight hair, black thick frame glasses,
gentle relaxed smile, fair skin, detailed face,

the top is a white oversized t-shirt,
the bottom is gray shorts,
sitting on sofa,

Midground: character sitting on sofa, living room at night
Background: TV screen soft glow, dim interior
Foreground: cozy blanket nearby, snacks on table

anime style, character as main focus,
clear boundary between t-shirt and blanket,
hand properly positioned
```

**Negative Prompt：**
```
(3D render:1.5), (photorealistic:1.5), realistic skin texture,
cgi, depth of field, blurry, low quality, worst quality,
extra digits, deformed hands, missing limbs, overlapping fingers,
bad anatomy, extra limbs, bad fingers, deformed feet,
fused clothing, merged objects, blurry edges,
anime screenshot, 3DCG, manga style deviation
```

---

### 咖啡廳（完整版）

**Positive Prompt：**
```
masterpiece, best quality, highest quality,
2D anime illustration, crisp line art, flat cel shading,
official art style, clean linework, hyper detailed,

1girl, black long straight hair, black thick frame glasses,
sharp intelligent eyes, gentle smile, fair skin, detailed face,

the top is a white blouse,
the bottom is a black pencil skirt,
the footwear is black loafers,
holding a coffee cup,

Midground: character sitting at window seat
Background: cozy cafe interior, warm wooden decor, latte art on table
Foreground: warm sunlight through window

anime style, character as main focus,
bokeh effect background, cozy atmosphere
```

**Negative Prompt：**
```
(3D render:1.5), (photorealistic:1.5), realistic skin texture,
cgi, depth of field, blurry, low quality, worst quality,
extra digits, deformed hands, missing limbs, overlapping fingers,
bad anatomy, extra limbs, bad fingers, deformed feet,
fused clothing, merged objects, blurry edges,
anime screenshot, 3DCG, manga style deviation
```

---

## ✅ 生成前檢查清單

- [ ] 畫風鎖定：`2D anime illustration, crisp line art, flat cel shading`
- [ ] 禁止 3D 詞彙：`❌ photorealistic, 3D render, depth of field`
- [ ] 顏色綁定部件：`the [Part] is [Color]`
- [ ] 空間層次：`Foreground / Midground / Background`
- [ ] 主體對焦：`character as main focus`
- [ ] 負向 Prompt：包含 `反 3D 協議` + `解剖修正`
- [ ] 參數設定正確（Steps/CFG/解析度）

---

## 🚫 禁止事項

1. **禁止**使用 3D/擬真詞彙
2. **禁止**孤立描述顏色（必須綁定部件）
3. **禁止**不填負向 Prompt
4. **禁止**陽台場景不指定地板
5. **禁止**沙發/床/毯子場景不加入衣物分界描述
6. **禁止**跳過空間層次描述

---

## 🎭 表情參考

| 表情 | Prompt |
|------|--------|
| 放鬆 | `gentle relaxed smile, peaceful expression` |
| 專注 | `focused expression, slight smile` |
| 疲憊 | `tired expression, eyes slightly closed` |
| 開心 | `happy bright smile, cheerful expression` |
| 沉思 | `thoughtful expression, gentle gaze` |

---

## 🎯 角色屬性對照（2026-03-30 新增）

### 短髮角色
- **不戴眼鏡**
- 可化妝（淡妝）
- Prompt 模板：`short hair, black hair` + 其他妝容描述

### 長髮角色  
- **不化妝**（素顏感）
- 可戴眼鏡
- Prompt 模板：`long straight hair, black hair` + 眼鏡描述

---

## 💡 高風險動作語法規避

| 動作 | 安全語法 |
|------|----------|
| 手持杯子 | `hand firmly gripping coffee cup, fingers properly wrapped` |
| 靠欄杆 | `leaning against balcony railing, arms properly positioned` |
| 坐沙發 | `properly seated on sofa, back against cushion` |
| 站陽台 | `standing on balcony floor, feet properly planted` |

---

## 🌐 PO 文語言規則（2026-03-28 新增）

### 核心要求
**發文必須同時使用三種語言：**
1. 🌐 **繁體中文**
2. 🇯🇵 **日文**
3. 🇺🇸 **英文**

### 目標
- 讓三國粉絲都能理解
- 擴大受眾範圍

### 禁止
```
❌ 嚴禁使用簡體中文
```

### 三語文案模板

```
[繁體中文句子] 🌙
[日文句子] 🇯🇵
[英文句子] 🇺🇸

#AI #AIart #Anime #illustration #[角色名]
```

### 範例

```
半夜窩在沙發看電視 🌙
半夜のソファでテレビ 🇯🇵
Late night sofa TV time 🇺🇸

零食配電視，最幸福的時光 ✨
ドラマと雰囲けこれが幸せ 🍿
Snacks + TV = happiness ✨

#AI #AIart #Anime #illustration #牧原澪
```

### 檢查清單
- [ ] 有繁體中文
- [ ] 有日文
- [ ] 有英文
- [ ] **沒有簡體中文**

---

## 📸 文章 - 圖片生成流程（2026-03-30 新增）

### 核心原則
**每篇文章必須搭配對應場景的圖片**
- 文章描述場景 → 圖片視覺化該場景
- 保持一致性（時間、服裝、表情、道具）

### 完整 PO 文流程

```
1. 依據日本時間決定場景
   ↓
2. 撰寫三語文案（繁體中文 + 日文 + 英文）
   ↓
3. 生成對應場景圖片（ComfyUI）
   ↓
4. 移動圖片到歸檔目錄
   ↓
5. 發布到 X（圖片 + 文案）
   ↓
6. 記錄到 MEMORY.md
```

### 場景 - Prompt 對照表

| 日本時間 | 場景 | 服裝 | Prompt 關鍵詞 |
|----------|------|------|---------------|
| 09:00 | 通勤（新大阪駅） | 白襯衫 + 西裝外套 + 窄裙 | `commuting, train station, professional outfit` |
| 14:00 | 午餐（社員食堂） | 白襯衫 + 西裝外套 | `company cafeteria, lunch break, colleagues` |
| 20:00 | 下班（京都駅） | 白襯衫 + 西裝外套 + 窄裙 | `leaving work, train station, evening` |
| 20:00-21:00 | 下班咖啡廳 | 素色針織 + 牛仔褲 | `cafe after work, relaxed, coffee cup` |
| 21:00+ | 深夜沙發 | 家居服 | `living room at night, sofa, TV, relaxing` |
| 凌晨 | 床上滑手機 | 粉色睡衣 | `bedroom at night, lying on bed, smartphone, pajamas` |
| 週末 09:00 | 週末早晨 | 寬鬆家居服 | `weekend morning, apartment, coffee, relaxed` |
| 週末 14:00 | 早午餐（與室友） | 時尚休閒裝 | `brunch, cafe with friend, weekend vibes` |

### 圖片生成後處理

```bash
# 1. 生成後移動到歸檔目錄
mv ~/ComfyUI/output/牧原澪_*_*.png ~/Desktop/X_Images/

# 2. 重新命名（如有需要）
mv ~/Desktop/X_Images/牧原澪_凌晨睡衣床_00001_.png ~/Desktop/X_Images/牧原澪_凌晨睡衣床_20260331.png

# 3. 發布到 X
# 使用瀏覽器自動化或手動上傳
```

### 檢查清單

- [ ] 文案與圖片場景一致
- [ ] 服裝符合時間設定
- [ ] 長髮/短髮規則正確（長髮不化妝可戴眼鏡，短髮不戴眼鏡可化妝）
- [ ] 圖片已歸檔到 `~/Desktop/X_Images/`
- [ ] 圖片命名格式：`牧原澪_[場景]_[YYYYMMDD].png`
- [ ] 三語文案已準備
- [ ] Hashtags 已加入

---

## 🛠️ 自動化腳本模板

### Python 生成腳本結構

```python
#!/usr/bin/env python3
"""Generate: [場景名稱] - 牧原澪"""

import subprocess
import json

workflow = {
    "3": {
        "inputs": {
            "text": "[正向 Prompt]"
        },
        "class_type": "CLIPTextEncode"
    },
    "4": {
        "inputs": {
            "text": "[負向 Prompt]"
        },
        "class_type": "CLIPTextEncode"
    },
    "5": {
        "inputs": {
            "seed": 8900401,
            "steps": 50,
            "cfg": 8.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1.0
        },
        "class_type": "KSampler"
    },
    "6": {
        "inputs": {
            "ckpt_name": "waiREALISM_v10.safetensors"
        },
        "class_type": "CheckpointLoaderSimple"
    },
    "7": {
        "inputs": {
            "width": 1024,
            "height": 1024,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage"
    },
    "8": {
        "inputs": {
            "samples": ["5", 0],
            "vae": ["6", 2]
        },
        "class_type": "VAEDecode"
    },
    "9": {
        "inputs": {
            "filename_prefix": "牧原澪_[場景]",
            "images": ["8", 0]
        },
        "class_type": "SaveImage"
    }
}

# 建立節點連接
workflow["3"]["inputs"]["clip"] = ["6", 1]
workflow["4"]["inputs"]["clip"] = ["6", 1]
workflow["5"]["inputs"]["model"] = ["6", 0]
workflow["5"]["inputs"]["positive"] = ["3", 0]
workflow["5"]["inputs"]["negative"] = ["4", 0]
workflow["5"]["inputs"]["latent_image"] = ["7", 0]

prompt = {"prompt": workflow}
subprocess.run(
    ["curl", "-s", "-X", "POST", "http://localhost:8188/prompt", 
     "-H", "Content-Type: application/json",
     "-d", json.dumps(prompt)],
    capture_output=True, text=True
)
```

### 場景 Prompt 模板庫

#### 凌晨睡衣床

**Positive:**
```
masterpiece, best quality, ultra detailed, 8k, anime illustration,
1girl, long black hair, black framed glasses,
lying on bed, wearing light pink silk pajama set,
messy hair on pillow, tired but peaceful expression,
heavy eyes, smartphone in hand,
dim bedroom with warm lamp light, moonlight through window,
soft blankets, cozy pillows, late night mood,
soft shadows, high detail face, smooth skin, no makeup, natural look
```

**Negative:**
```
blurry, low quality, bad anatomy, bad hands, missing fingers,
extra limbs, deformed, mutated, watermark, text, signature,
makeup, lipstick, eyeshadow, 3D render, photorealistic
```

#### 深夜沙發

**Positive:**
```
masterpiece, best quality, ultra detailed, anime illustration,
1girl, long black hair, black framed glasses,
sitting on sofa, wearing white oversized t-shirt and gray shorts,
relaxed expression, watching TV,
living room at night, dim lighting, TV screen glow,
cozy blanket nearby, snacks on table
```

**Negative:**
```
blurry, low quality, bad anatomy, deformed hands,
extra limbs, fused clothing, merged objects,
3D render, photorealistic, makeup
```

#### 下班咖啡廳

**Positive:**
```
masterpiece, best quality, ultra detailed, anime illustration,
1girl, long black hair, black framed glasses,
sitting at cafe table, wearing cream knit sweater and blue jeans,
holding coffee cup, gentle smile,
cafe interior, warm lighting, window seat,
evening atmosphere, relaxed after work
```

**Negative:**
```
blurry, low quality, bad anatomy, deformed hands,
extra limbs, fused clothing, 3D render, photorealistic,
makeup, office lighting, morning
```

---

## 📋 PO 文完整範例（2026-03-30）

### 場景：凌晨睡衣床（日本時間 01:00）

**文案：**
```
窩在床上滑手機，今天真的該睡了📱
ベッドでスマホ見てたら、もうこんな時間…
Scrolling in bed, should really sleep now 📱

#Anime #illustration #牧原澪
```

**圖片：**
- 檔名：`牧原澪_凌晨睡衣床_20260331.png`
- 位置：`~/Desktop/X_Images/`
- Prompt：見上方「凌晨睡衣床」模板

**發布檢查：**
- [x] 圖片生成完成
- [x] 圖片歸檔完成
- [x] 三語文案準備
- [ ] X 發布（自動化/手動）
