# 🔒 API Key 安全規則（2026-04-07 緊急制定）

## 核心原則

**API Key 只能存在 `.env` 檔案中，絕對不能寫在程式碼裡！**

---

## 錯誤示範（絕對禁止）

```python
# ❌ 錯誤！API Key 寫死在程式碼
API_KEY = "sk-1234567890abcdef"

# ❌ 錯誤！即使註釋也不可以
# API Key: sk-1234567890abcdef
```

## 正確做法

```python
# ✅ 正確：從環境變數讀取
import os
API_KEY = os.getenv("API_KEY")

# ✅ 正確：從 .env 檔案讀取
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
```

---

## 提交前檢查流程（強制執行）

### Step 1：檢查敏感關鍵字

```bash
# 在 git add 之前執行
grep -r "api_key\|API_KEY\|secret\|password\|token" --include="*.py" --include="*.js" --include="*.sh" .

# 如果有任何輸出，絕對不能 commit！
```

### Step 2：檢查 .gitignore

```bash
# 確認敏感檔案被排除
cat .gitignore | grep -E "\.env|\.key|*.pem"
```

### Step 3：使用 git diff 確認

```bash
# 提交前必ず看差異
git diff --cached
```

### Step 4：預設規則

```
任何包含以下關鍵字的檔案，絕對不能 git add：
- api_key, API_KEY
- secret, SECRET
- password, PASSWORD
- token, TOKEN
- key, KEY
- credential, CREDENTIAL
- "eyJ" (JWT token pattern)
- "sk-" (OpenAI key pattern)
- "ghp_" (GitHub token pattern)
```

---

## 腳本建立時的模板

建立任何需要 API 的腳本時，必須使用：

```python
#!/usr/bin/env python3
"""
Script description
"""
import os

# 從環境變數讀取 API Key
def get_api_key(key_name: str) -> str:
    """安全取得 API Key"""
    key = os.getenv(key_name)
    if not key:
        # 嘗試從 ~/.openclaw/.env 讀取
        env_file = os.path.expanduser("~/.openclaw/.env")
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith(f"{key_name}="):
                        return line.split("=", 1)[1].strip()
        raise ValueError(f"API Key {key_name} not found")
    return key

# 使用
API_KEY = get_api_key("API_KEY_NAME")
```

---

## 安全檢查清單

- [ ] API Key 從環境變數讀取，不是 hardcoded？
- [ ] 檔案在 .gitignore 中？
- [ ] `grep` 檢查沒有敏感關鍵字？
- [ ] `git diff` 確認變更內容？
- [ ] 測試環境變數是否正確讀取？

---

## 違規處理

如果發現 API Key 被上傳：
1. 立即刪除 Repo
2. 重新產生所有 API Key
3. 更新 .env
4. 從 local 移除並重建
