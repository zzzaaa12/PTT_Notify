# PTT Notify

## 簡介  

本專案由 Python 撰寫，主要功能如下：  
- 定時讀取PTT特定看板的 RSS feed  
- 過濾RSS內容的標題或作者  
- 將最新的過濾結果以mail寄到收件者信箱  

## 檔案說明  

- ptt_notify.py：主程式  
- setting.py：主設定檔  
- send_notify.py: 發送mail的程式碼與設定檔  

## 使用方法  

1. 在 setting.py 的下列變數填寫設定：
- AUTO_UPDATE_SECS：自動更新時間  
- BOARD_LIST：填入偵測的英文看板名稱  
- SHOW_ALL_BOARD：偵測所有文章的看板  
- KEYWORD_LIST：偵測的標題關鍵字清單  
- AUTHOR_LIST：偵測的作者清單  

2. 在 send_notify.py 填寫mail寄件者與收件者資訊：
- FROM_ADDR：寄件者mail  
- TO_ADDR：收件者mail  
- SMTP_PASSWD：收件者mail帳號  

3. 直接執行 ptt_notify.py 即可
  

## 注意事項  
- 本程式預設讀取間隔時間為五分鐘
- 文章產生與擷取資料的時間差可能會到10-15分鐘
