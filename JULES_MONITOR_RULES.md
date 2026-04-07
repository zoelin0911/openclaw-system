# Jules 自動監控規則（2026-04-07）

## 觸發條件

當建立 Jules 任務後，自動設定監控 cron job。

## 監控流程

```
1. 建立 Jules Session
2. 立即建立 cron job 每 5 分鐘檢查狀態
3. 檢查狀態：
   - IN_PROGRESS：繼續監控
   - COMPLETED：發送到 Telegram，報告結果
   - FAILED：CANCELLED：發送錯誤報告
4. 自動刪除 cron job
```

## 指令

```bash
# 檢查 Jules Session 狀態
curl -s "https://jules.googleapis.com/v1alpha/sessions/{SESSION_ID}" \
  -H "x-goog-api-key: $JULES_API_KEY"

# 取得 Activities
curl -s "https://jules.googleapis.com/v1alpha/sessions/{SESSION_ID}/activities" \
  -H "x-goog-api-key: $JULES_API_KEY"
```

## 通知格式

```
🔄 Jules 任務監控
━━━━━━━━━━━━━━━━━━
狀態：IN_PROGRESS
標題：{TITLE}
時間：{UPDATE_TIME}

[繼續等待...]
```

```
✅ Jules 任務完成！
━━━━━━━━━━━━━━━━━━
標題：{TITLE}
URL：{URL}
```

```
❌ Jules 任務失敗
━━━━━━━━━━━━━━━━━━
標題：{TITLE}
原因：{ERROR}
```

## 自動化設定

每次建立 Jules 任務後，自動建立 cron job：
- 頻率：每 5 分鐘
- 依據：SESSION_ID 動態設定
- 結束條件：狀態非 IN_PROGRESS
