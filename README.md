# PTT article notifier

## 簡介  

本專案由 Python 撰寫，主要功能如下：  
- 定時讀取PTT特定看板的 RSS feed  
- 過濾RSS內容的標題或作者  
- 將最新的過濾結果以mail寄到收件者信箱  

## 檔案說明  

- ptt_title_parser.py: 主程式
- send_notify.py: 發送mail的code  

## 使用方法  

1. 在 ptt_title_parser.py 的下列變數填寫設定：  
  - BOARD_LIST：填入監控的英文看板名稱  
  - KEYWORD_LIST：監控關鍵字，有符合關鍵字的會寄信通知(關鍵字非英文時請加上u，ex: u'鍵盤')  
  - SHOW_ALL_BOARD：填在這邊的看板，只要有新文章會直接寄信通知  

2. 在 send_notify.py 填寫mail寄件者與收件者資訊：  
  - FROM_ADDR：寄件者mail  
  - TO_ADDR：收件者mail  
  - SMTP_PASSWD：收件者mail帳號  

3. 直接執行 ptt_title_parser.py 即可  
  

## 注意事項  
- 本程式預設讀取間隔時間為五分鐘
- RSS產生的時間不一，所以文章與擷取資料的時間差可能會到10-15分鐘
