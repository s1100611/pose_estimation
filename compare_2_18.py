import json
import numpy as np
from scipy.spatial.distance import euclidean
import cv2
import os
import openai
import time



start_time = time.time()

# 資料夾路徑
json_folder = r"D:/dataset/marked_18/keypoints/"
image_folder = r"D:/dataset/marked_18/photos/"  # 確保這裡是存放對應圖片的資料夾
database_file = "database18.json"

# 讀取 JSON 檔案 (單張圖片)
def load_json_keypoints(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 檢查是否有偵測到人
    if "people" not in data or len(data["people"]) == 0:
        return None  # 沒有偵測到人

    # 取得 18 個關節點的 (x, y) 座標
    keypoints = data["people"][0]["pose_keypoints_2d"]
    xy_keypoints = [(keypoints[i], keypoints[i+1]) for i in range(0, len(keypoints), 3)]  # 每 3 個取 (x, y)
    
    return xy_keypoints  # 回傳 (x, y) 陣列，長度應為 18

# 轉換為 NumPy 向量
def keypoints_to_vector(keypoints):
    return np.array(keypoints).flatten()  # 轉換成 36 維向量 (18 × 2)

# 讀取資料庫
def load_json_database(database_file):
    with open(database_file, 'r') as f:
        return json.load(f)  # 回傳字典 { "image_001.jpg": [[x, y], [x, y], ...] }

# 找出最相似的照片
def find_most_similar_image(new_keypoints, database):
    new_vector = keypoints_to_vector(new_keypoints)  # 轉換為 NumPy 向量
    best_match = None
    min_distance = float('inf')

    for image_name, keypoints in database.items():
        db_vector = keypoints_to_vector(keypoints)  # 轉換資料庫內的向量
        distance = euclidean(new_vector, db_vector)  # 計算歐幾里得距離

        if distance < min_distance:  # 更新最小距離
            min_distance = distance
            best_match = image_name

    return best_match, min_distance

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

# 測試
file_path = "C:/Users/Win11/Desktop/Graduation_project/tests_18/path_to_output_folder_detected/6_keypoints.json"  # 你的新照片 JSON
database_path = "database18.json"  # 你的資料庫 JSON

# 讀取新圖片
new_keypoints = load_json_keypoints(file_path)
new_keypoints = normalize_keypoints(new_keypoints)  # 加入正規化步驟

if new_keypoints:
    print("成功解析關節點！")

    # 讀取資料庫
    database = load_json_database(database_path)

    # 找出最相似的圖片
    best_match, similarity = find_most_similar_image(new_keypoints, database)
    print(f"最相似的圖片: {best_match}, 相似度 (歐幾里得距離): {similarity}")
    if best_match:
        image_path = os.path.join(image_folder, best_match.replace("_keypoints.json", ".png"))  # 確保副檔名正確
        img = cv2.imread(image_path)

        if img is not None:
            # 在圖片上標記關節點
            for x, y in database[best_match]:
                if x > 0 and y > 0:  # 過濾無效點
                    cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)  # 綠色點
            
        else:
            print("找不到對應圖片，請確認圖片路徑是否正確！")
else:
    print("無法解析新圖片的關節點！")


from typing import Dict, Tuple
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont


landmark_names = [
        "NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER", "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
        "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT", "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW",
        "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY", "LEFT_INDEX", "RIGHT_INDEX",
        "LEFT_THUMB", "RIGHT_THUMB", "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE",
        "LEFT_HEEL", "RIGHT_HEEL", "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"
    ]

#18關節點要做的 33則去掉
reordered_indices = [0, 1, 12, 14, 16, 11, 13, 15, 24, 26, 28, 23, 25, 27, 5, 2, 8, 7]  


class PoseCompare:

    #改
    connect_skeleton = [
    [0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6],
    [0, 7], [7, 8], [8, 9], [7, 10], [10, 11], [11, 12],
    [8, 13], [13, 14], [14, 15]
    ]

    #改
    kpts_angle = {
    "right_shoulder": [2, 8, 10],
    "right_elbow": [2, 3, 4],
    "left_shoulder": [5, 11, 13],
    "left_elbow": [5, 6, 7],
    "right_hip": [8, 10, 12],
    "right_knee": [8, 10, 14],
    "left_hip": [11, 13, 15],
    "left_knee": [11, 13, 16]
    }


    def __init__(self):
        self.output_ref = None
        self.output_trgt = None
        self.angle_ref = None
        self.angle_trgt = None
        self.img_ref = None
        self.img_trgt = None
        self.landmark_names = landmark_names

    def load_json(self, json_path: str) -> Dict:
        """讀取 JSON 檔案並轉換成 keypoints 格式"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        keypoints = data["people"][0]["pose_keypoints_2d"]
        keypoints_2d = [[keypoints[i], keypoints[i + 1]] for i in range(0, len(keypoints), 3)]
        return {"keypoints": np.array(keypoints_2d)}

    def inference(self, json_path: str) -> Tuple[Dict, Dict]:
        """讀取 JSON 格式檔案，計算姿勢和關節角度"""
        output = self.load_json(json_path)
        angles = {}
        for k, v in self.kpts_angle.items():
            angles[k] = self.get_angle(output["keypoints"], v)
        return output, angles

    def get_angle(self, keypoints: np.ndarray, points: list) -> float:
        """計算給定關節點之間的角度"""
        p1, p2, p3 = points
        a = keypoints[p1]
        b = keypoints[p2]
        c = keypoints[p3]
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(cosine_angle))
        return round(angle, 2)

    def load_ref_image(self, img_path: str):
        """讀取參考圖像"""
        self.img_ref = Image.open(img_path)

    def load_trgt_image(self, img_path: str):
        """讀取目標圖像"""
        self.img_trgt = Image.open(img_path)

    def load_json_as_ref(self, json_path: str, img_path: str):
        """讀取並設置參考姿勢及其圖像"""
        self.output_ref, self.angle_ref = self.inference(json_path)
        self.load_ref_image(img_path)

    def load_json_as_trgt(self, json_path: str, img_path: str):
        """讀取並設置目標姿勢及其圖像"""
        self.output_trgt, self.angle_trgt = self.inference(json_path)
        self.load_trgt_image(img_path)

    def calculate_overall_direction(self) -> str:
        """計算整體方向差異並給出建議方向"""
        ref_center = np.mean(self.output_ref["keypoints"], axis=0)
        trgt_center = np.mean(self.output_trgt["keypoints"], axis=0)

        direction = ""
        if trgt_center[0] < ref_center[0]:
            direction += "Left"
        elif trgt_center[0] > ref_center[0]:
            direction += "Right"

        if trgt_center[1] < ref_center[1]:
            direction += " Up"
        elif trgt_center[1] > ref_center[1]:
            direction += " Down"

        return direction.strip()

    def draw_one(self, img: Image, trgt: str = "ref") -> Image:
        """在圖像上繪製姿勢骨架"""
        if trgt == "ref":
            kp = self.output_ref["keypoints"]
        else:
            kp = self.output_trgt["keypoints"]

        img = img.copy()
        img_draw = ImageDraw.Draw(img)

        # 繪製骨架
        for con in self.connect_skeleton:
            pt1, pt2 = con[0], con[1]
            start_x, start_y = kp[pt1][0], kp[pt1][1]
            end_x, end_y = kp[pt2][0], kp[pt2][1]
            img_draw.line([(start_x, start_y), (end_x, end_y)], fill="red", width=3)

        # 繪製關節點
        for i in range(len(kp)):
            x, y = kp[i]
            img_draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill="blue")

        return img

    def compare_angles(self, max_angle_diff: float = 20.0) -> Tuple[Dict, bool]:
        """比較參考和目標角度，並標記差異"""
        angle_diff = {}
        all_ok = True
        for key in self.angle_ref.keys():
            diff = self.angle_ref[key] - self.angle_trgt[key]
            angle_diff[key] = diff
            if abs(diff) > max_angle_diff:
                all_ok = False
        return angle_diff, all_ok

    def draw_compare(self, max_angle_diff: float = 20.0) -> Image:
        """並排顯示參考和目標的姿勢與圖像進行比較，同時列印角度資訊"""
        if self.img_ref is None or self.img_trgt is None:
            raise ValueError("請先載入參考和目標圖像。")


        # 計算角度差異
        angle_diff, all_ok = self.compare_angles(max_angle_diff)
        
        # 列印角度差異資訊
        print("\n角度差異：")
        b='假設你是一個專業攝影師，下面是拍照時模特兒與需要擺的姿勢的角度差異，請幫我用簡潔的文字敘述讓模特兒更好理解，例如:手再抬高一點!\n'+'角度差異:\n'
        for k, diff in angle_diff.items():
            status = "OK" if abs(diff) <= max_angle_diff else "NOT OK"
            print(f"{k}: {diff:.2f}度 ({status})")
            a=f"{k}: {diff:.2f}度 ({status})\n"
            b=b+a

        client = openai.OpenAI(api_key="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")  # 直接傳入 API Key

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": b}]
        )
        print('\n')
        print(completion.choices[0].message.content)

        # 繪製參考圖像上的姿勢
        img_ref = self.draw_one(self.img_ref, trgt="ref")
        # 繪製目標圖像上的姿勢
        img_trgt = self.draw_one(self.img_trgt, trgt="trgt")

        # 並排顯示參考和目標圖像
        total_width = img_ref.width + img_trgt.width
        max_height = max(img_ref.height, img_trgt.height)
        compare_img = Image.new("RGB", (total_width, max_height))

        # 放置參考圖像和目標圖像
        compare_img.paste(img_ref, (0, 0))
        compare_img.paste(img_trgt, (img_ref.width, 0))

        return compare_img

# 使用範例
pose_compare = PoseCompare()
pose_compare.load_json_as_ref(file_path,file_path.replace("_keypoints.json", ".png"))
pose_compare.load_json_as_trgt(os.path.join(json_folder, best_match), image_path)

# 顯示角度和方向差異
result_img = pose_compare.draw_compare(max_angle_diff=20)

end_time = time.time()
execution_time = end_time - start_time
print("程式執行時間：", execution_time, "秒")

result_img.show()
result_img.save('C:/Users/Win11/Desktop/Graduation_project/best_result/comparison_output18_11.png')  # 保存比較結果




'''
best_result= os.path.join('best_result')
os.makedirs(best_result,exist_ok=True)

cv2.imwrite()

'''


