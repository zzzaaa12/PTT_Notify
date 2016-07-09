PTT article notifier
===================
本專案由 Python 撰寫，主要功能如下：  
- 定時讀取PTT特定看板的 RSS feed  
- 過濾RSS內容的標題或作者  
- 將最新的過濾結果以mail寄到收件者信箱  

--------
**檔案說明**  
- ptt_title_parser.py: 主程式
- send_notify.py: 發送mail的code (信箱資料填在這邊)

**注意事項**  
- 本程式預設讀取間隔時間為五分鐘
- RSS產生的時間不一，所以文章與擷取資料的時間差可能會到10-15分鐘
