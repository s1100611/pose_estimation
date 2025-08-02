import os
import json
import numpy as np
from scipy.spatial.distance import euclidean

# 指定 JSON 檔案的資料夾路徑
json_folder = r"D:/dataset/marked_18/keypoints"
database_file = "database18.json"
#database_file = "database33.json"

# 讀取 JSON 並回傳 (x, y) 關節點座標
def load_json_keypoints(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 確保 JSON 有人像數據
    if "people" not in data or len(data["people"]) == 0:
        return None

    # 取得 18 個關節點的 (x, y) 座標
    keypoints = data["people"][0]["pose_keypoints_2d"]
    xy_keypoints = [(keypoints[i], keypoints[i + 1]) for i in range(0, len(keypoints), 3)]
    
    return np.array(xy_keypoints)  # 轉為 NumPy 陣列

# **骨架正規化函式**
def normalize_keypoints(keypoints):
    keypoints = np.array(keypoints)  # 轉 NumPy 陣列

    # 取得基準點
    neck = keypoints[1]   # 頸部
    midhip = keypoints[8] # 骨盆
    left_shoulder = keypoints[2]
    right_shoulder = keypoints[5]

    # **中心化骨架 (平移)**
    center = (neck + midhip) / 2  # 以 (頸部 + 骨盆) 中心點為基準
    keypoints -= center

    # **計算主要骨架長度 (例如肩寬)**
    shoulder_width = euclidean(left_shoulder, right_shoulder)

    if shoulder_width > 0:
        keypoints /= shoulder_width  # 讓骨架長度標準化為 1

    return keypoints.tolist()  # 轉回 list 存入 JSON

# 建立資料庫
database = {}

# 讀取資料夾內的所有 JSON 檔案
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):  # 確保是 JSON 檔案
        file_path = os.path.join(json_folder, filename)
        
        keypoints = load_json_keypoints(file_path)
        if keypoints is not None:
            normalized_keypoints = normalize_keypoints(keypoints)  # 加入正規化步驟
            database[filename] = normalized_keypoints  # 存入字典

# 存成 JSON 檔案
with open(database_file, 'w') as f:
    json.dump(database, f, indent=4)

print(f"向量資料庫建立完成，共 {len(database)} 張照片！")


