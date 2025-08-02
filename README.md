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


### 2.找出相近的照片

#### body_f_18.py
這段程式碼的主要作用是使用 MediaPipe 模型對資料夾內的圖片進行人體姿勢偵測，並輸出標註後的圖片與關節點座標（JSON 檔）
原本按照計劃書上的流程我們會先分群在進行預測，但是我們用了 ... 進行分群，由於我們資料集非常龐大，丟給模型分群效果不佳執行起來要好幾個天，
與前面程式碼不同的是這邊修正為只偵測18個關節點，因為我們找到的分群模型是用 openpose keypoints 的資料儲存格式，因此在分群前我們希望 mediapipe 預測完的關節點直接存成 openpose 18個關節點的格式，那為甚麼我們沒有直接用 openpose 進行預測，因為 openpose 對於系統要求比較高我們的電腦無法負荷，於是我們才採取上述做法。

主要流程說明：
初始化 Mediapipe Pose 模組：
設定模型複雜度、是否平滑關節點、最低偵測與追蹤可信度等參數。
設定資料夾路徑：
input_folder 是輸入圖片的資料夾
output_folder_detected 是輸出結果圖片與 JSON 的資料夾（若不存在會自動建立）
針對資料夾內所有圖片進行處理：

檢查圖片格式（jpg、jpeg、png）

讀取圖片，並轉換為 RGB 格式

傳入 MediaPipe Pose 模型進行姿勢偵測

如果有偵測到姿勢：

使用 MediaPipe 畫出關節點與連線

儲存畫過關節點的圖片（png 格式）

依照自訂的順序 reordered_indices 取出特定關節點

idx == 1 時會取左右肩膀平均作為"脖子"點

將每個關節的 (x, y, visibility) 存入列表

將關節資訊儲存為 JSON 檔，結構符合 COCO 格式 (pose_keypoints_2d)

若未偵測到姿勢：

在終端機輸出提示訊息

輸出結果包括：
已標註關節點的圖片（PNG 格式）

對應的關節座標資料 JSON 檔

這段程式特別適合用於建立姿勢資料集或作為動作分析的前處理步驟。



