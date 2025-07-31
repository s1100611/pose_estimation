# pose_estimation

### 1.資料集預處理


#### 資料夾樹狀圖如下

**data pre-process** folder  
    |_ 0_ig_login.py  
    |_ 1_ig_crawler.py  
    |_ 1-1_clean_人員list.py  
    |_ 2_select_jpg.py  
    |_ 3_postestimanation.py  
    |_ 4_del.py  
    |_ 4-1_check.py  
    |_ 4-2_count.py  
    |_ cluster_keypoint.py  
    |_ instaloader.app  
    |_ instaloader.exe  
    |_ 粉絲數高攝影師名單.excel  

#### 0_ig_login.py

此python檔是一開始我們嘗試用來自動化登入Instagram，但是用久了發現會跳出現是不是本人的訊息，我們有嘗試用自動化但是解決不了，於是有第二個 1_ig_crawler.py 檔

#### 1_ig_crawler.py

上述方法失敗後我們找到一個叫 instaloader 的套件，透過這個套件爬取我們想要爬取帳號的照片

#### 1-1_clean_人員list.py

這段程式碼透過instaloader擷取出我們想要爬的攝影師帳號，自動化查詢該帳號粉絲數有多少並寫成一個excel檔

#### 2_select_jpg.py

這段程式碼將我們蒐集好的資料集，讀取資料集所有的檔名，利用檔名結尾的不同來篩選出照片排除影片，並儲存下來

#### 3_postestimanation.py

進行姿勢偵測，預測完成後儲存成png檔

#### 4_del.py

這段程式碼用來刪掉沒有辨識到的照片，由4-1和4-2程式碼合併而成

#### 4-1_check.py

這段程式碼用來檢查照片有沒有辨識到

#### 4-2_count.py

這段程式碼用來計算資料夾內照片數量，檢查有沒有刪對
