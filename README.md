
# pose_estimation

## 專案流程

本專案可分為兩大部分：

1. **資料集預處理**：從 Instagram 下載圖片、篩選出可用圖片並進行姿勢偵測  
2. **找出相近照片（分群與比對）**：利用 MediaPipe 偵測 + POSE-ID-on 分群與比對

---

## 1️資料集預處理

### 資料夾結構
data pre-process/  
│── 0_ig_login.py  
│── 1_ig_crawler.py  
│── 1-1_clean_人員list.py  
│── 2_select_jpg.py  
│── 3_postestimanation.py  
│── 4_del.py  
│── 4-1_check.py  
│── 4-2_count.py  
│── cluster_keypoint.py  
│── instaloader.app  
│── instaloader.exe  
│── 粉絲數高攝影師名單.xlsx  

### 各檔案說明

| 檔案名稱 | 功能說明 |
|---------|---------|
| **0_ig_login.py** | 嘗試自動化登入 Instagram，但會遇到「是否本人」驗證，後續改用 Instaloader。 |
| **1_ig_crawler.py** | 使用 Instaloader 套件爬取指定帳號的照片。 |
| **1-1_clean_人員list.py** | 擷取攝影師帳號並查詢粉絲數，輸出 Excel。 |
| **2_select_jpg.py** | 篩選出純照片（排除影片），並將檔名存檔。 |
| **3_postestimanation.py** | 使用 MediaPipe 進行姿勢偵測，輸出標註圖片（PNG）。 |
| **4_del.py** | 刪除未偵測到姿勢的圖片，由 4-1 與 4-2 合併而成。 |
| **4-1_check.py** | 檢查哪些圖片未被成功偵測。 |
| **4-2_count.py** | 計算資料夾內圖片數量，確認刪除結果正確。 |
| **cluster_keypoint.py** | 分群與比對流程使用的工具程式。 |

---

## 2️找出相近的照片

核心程式：**body_f_18.py**

### 功能說明

1. 使用 **MediaPipe Pose** 對資料夾內圖片進行人體姿勢偵測  
2. 將結果存為：
   - 標註後圖片（PNG）
   - 對應的 **OpenPose 18 Keypoints JSON**
3. 作為後續 **POSE-ID-on** 分群與比對的輸入

### 為什麼不用 OpenPose 直接預測？

- MediaPipe 運算輕量，因此採用 **MediaPipe 偵測 → 轉換為 OpenPose 格式** 的流程
- 未來或許可以直接採用openpose

### POSE-ID-on 模型特性

- 分群速度快：指定群數即可快速分類
- 比對速度受資料量影響大

### 先分群再比對的困難：

  1. 新圖片要先判斷屬於哪一群
  2. 更新資料集需重新訓練模型，耗時巨大

---

## 程式主要流程

1. **初始化 MediaPipe Pose**  
   - 設定模型複雜度、平滑參數、偵測與追蹤可信度
2. **讀取資料夾內圖片**  
   - 支援 jpg / jpeg / png
3. **進行姿勢偵測**  
   - 若偵測成功：
     1. 繪製關節點與骨架連線
     2. 轉換為 OpenPose 18 Keypoints（包含 `(x, y, visibility)`）
     3. 輸出標註圖片與 JSON
   - 若偵測失敗：
     - 終端機輸出提示訊息
4. **輸出結果**  
   - `output/photos/xxx.png`：標註關節點圖片  
   - `output/keypoints/xxx.json`：對應 JSON 檔  

---

相關連結  
POSE-ID-on 論文: https://www.mdpi.com/2220-9964/10/4/257  
POSE-ID-on GitHub: https://github.com/L9L4/POSE-ID-on  

---

## 3️更改成向量方式儲存資料

由於我們改變了資料儲存方式，不再使用 **POSE-ID-on** 的模型，因此也另外實作了 **33 個關節點版本**，以便支援更多姿勢資訊的比對。

核心程式：**database.py**

### 程式主要流程

1. **讀取資料集內所有關節點**  
   - 掃描資料集內所有 JSON 檔  
   - 將每張圖片的關節點資訊讀取後，以向量方式儲存
2. **正規化處理**  
   - 對關節點向量進行正規化  
   - 使不同尺寸或比例的圖片產生的向量能在同一尺度下比較
3. **輸出結果**  
   - 將整個資料集的關節點資訊以單一 JSON 檔儲存  
   - 檔名：databaseXX.json

---

## 4比對姿勢

核心程式：**compare_2_18.py**
程式碼主要整併前面幾個使用過的部分

### 程式主要流程

1. **讀取要比較圖片的關節點**  
   - 讀取輸入圖片對應的 `_keypoints.json` 檔  
   - 提取 18 個關節點座標 `(x, y)`  
   - 若未偵測到人，則直接跳過

2. **正規化與向量化**  
   - 將關節點中心化（以頸部與骨盆中心為原點）  
   - 使用肩寬標準化骨架長度  
   - 轉換為 NumPy 向量（18 × 2 → 36 維）

3. **與資料庫比對找出最相似圖片**  
   - 掃描資料庫 `database18.json`  
   - 計算歐幾里得距離找出相似度最高的姿勢  
   - 回傳最相似圖片檔名與距離數值

4. **角度計算與分析**  
   - 根據預設關節組（如肩膀、手肘、膝蓋）計算夾角  
   - 與目標圖片比較角度差異  
   - 標記超過閾值（預設 ±20°）的關節

5. **圖像可視化與建議生成**  
   - 在兩張圖片上繪製骨架線與關節點  
   - 將參考與目標圖片並排輸出  
   - 使用 GPT 產生簡潔的文字建議，例如：
     ```
     左手再抬高一點，右腿向外展開！
     ```

6. **輸出結果**  
   - 標註後的對比圖片（PNG 格式）  
   - 角度差異與建議文字  
   - 範例輸出位置：
     1. 18個關節點 :`best_result/18/comparison_output18_11.png`
     2. 33個關節點 :`best_result/33/comparison_output33_11.png`

---











