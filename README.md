# pose_estimation

### 1.資料集預處理


#### 資料夾樹狀圖如下

data pre-process folder
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

此python檔是一開始我們嘗試用來自動化登入Instagram，但是用久了發現會出現是不是本人的訊息，於是有第二個 1_ig_crawler.py 檔

#### 1_ig_crawler.py

上述方法失敗後我們找到一個叫 instaloader 的套件，透過這個套件爬取我們想要爬取帳號的照片

#### 1-1_clean_人員list.py

這個程式碼用來擷取出我們想要爬的攝影師粉絲樹有多少寫成一個excel檔

#### 2_select_jpg.py

這段程式碼用來篩選出照片排除影片，並儲存下來

#### 3_postestimanation.py

進行姿勢偵測，預測完成後儲存成png檔

#### 4_del.py



#### 4-1_check.py

#### 4-2_count.py


