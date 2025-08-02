
# pose_estimation

本專案旨在利用 **MediaPipe Pose** 偵測人體姿勢，並將關節點結果轉換為 **OpenPose 18 Keypoints JSON** 格式，以便後續使用 [POSE-ID-on](https://github.com/L9L4/POSE-ID-on) 進行**姿勢分群與比對**。  
我們同時包含一整套 **資料集蒐集與預處理流程**，方便快速建立可用於姿勢分析的資料集。

---

## 專案流程

本專案可分為兩大部分：

1. **資料集預處理**：從 Instagram 下載圖片、篩選出可用圖片並進行姿勢偵測  
2. **找出相近照片（分群與比對）**：利用 MediaPipe 偵測 + POSE-ID-on 分群與比對

---

## 1️⃣ 資料集預處理

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

## 2️⃣ 找出相近的照片

核心程式：**body_f_18.py**

### 功能說明

1. 使用 **MediaPipe Pose** 對資料夾內圖片進行人體姿勢偵測  
2. 將結果存為：
   - 標註後圖片（PNG）
   - 對應的 **OpenPose 18 Keypoints JSON**
3. 作為後續 **POSE-ID-on** 分群與比對的輸入

### 為什麼不用 OpenPose 直接預測？

- OpenPose 雖可直接產生 18 關節點，但系統需求高，現有電腦無法長時間運行  
- MediaPipe 運算輕量，因此採用 **MediaPipe 偵測 → 轉換為 OpenPose 格式** 的流程

### POSE-ID-on 模型特性

- 分群速度快：指定群數即可快速分類
- 比對速度受資料量影響大：
  - 4,000 張照片尚可
  - 超過 4,000 張比對需 20 天以上
- 先分群再比對的困難：
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
   - `output/annotated/xxx.png`：標註關節點圖片  
   - `output/keypoints/xxx.json`：對應 JSON 檔  

---

## OpenPose JSON 範例

```json
{
  "people": [
    {
      "pose_keypoints_2d": [
        123.4, 456.7, 0.9,
        120.1, 430.5, 0.8,
        ...
      ]
    }
  ]
}


相關連結
POSE-ID-on 論文: https://www.mdpi.com/2220-9964/10/4/257

POSE-ID-on GitHub: https://github.com/L9L4/POSE-ID-on






### 2.找出相近的照片

#### body_f_18.py
這段程式碼的主要作用是使用 MediaPipe 模型對資料夾內的圖片進行人體姿勢偵測，並輸出標註後的圖片與關節點座標（JSON 檔）
原本按照計劃書上的流程我們會先分群在進行預測，但是我們用了 POSE-ID-on 這個模型進行分群和比對，這個github有提供分群和比對兩種不同的程式碼
分群的速度可以很快，只要提供我們要分幾群就可以快速分類出，比對部分，由於我們資料集非常龐大，我們試過大概4000張照片，執行效果還可以，但是超過4000張訓練速度會變很慢，直接丟給模型分群效果不佳執行起來要二十幾天，我們有嘗試過先分群在進行比對，但是會遇到下述問題

1.假設現在有個未知照片要比對，要怎麼判斷他屬於哪一群?
2.找到他屬於哪一群要重新跟模型訓練，耗費很多時間

POSE-ID-on論文連結:https://www.mdpi.com/2220-9964/10/4/257
POSE-ID-on程式碼連結:https://github.com/L9L4/POSE-ID-on

與前面程式碼不同的是這邊修正為只偵測18個關節點，因為我們找到的分群模型是用 openpose keypoints 的資料儲存格式，因此在分群前我們希望 mediapipe 預測完的關節點直接存成 openpose 18 個關節點的格式，那為甚麼我們沒有直接用 openpose 進行預測，因為 openpose 對於系統要求比較高我們的電腦無法負荷，於是我們才採取上述做法。

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

