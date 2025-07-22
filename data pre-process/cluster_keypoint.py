import os
import json
import shutil

# 建立好所有資料夾
input_folder = r"C:/Users/Win11/Desktop/temp/selected/all4/keypoints"
output_folder_detected = os.path.join(input_folder, 'selected')
output_folder_all2 = os.path.join(output_folder_detected, 'all3')
output_folder_all4 = os.path.join(output_folder_detected, 'all4')
output_all2_keypoints = os.path.join(output_folder_all2, 'keypoints')
output_all2_photos = os.path.join(output_folder_all2, 'photos')
output_all4_keypoints =os.path.join(output_folder_all4, 'keypoints')
output_all4_photos =os.path.join(output_folder_all4, 'photos')

image_path = 'C:/Users/Win11/Desktop/temp/selected/all4/photos'


os.makedirs(output_folder_detected, exist_ok=True)
os.makedirs(output_folder_all2, exist_ok=True)
os.makedirs(output_folder_all4, exist_ok=True)
os.makedirs(output_all2_keypoints, exist_ok=True)
os.makedirs(output_all2_photos, exist_ok=True)
os.makedirs(output_all4_keypoints, exist_ok=True)
os.makedirs(output_all4_photos, exist_ok=True)

# 設定新的工作路徑
os.chdir("C:/Users/Win11/Desktop/temp/selected/all4/keypoints")

# 確認是否成功切換
print("切換後的工作目錄:", os.getcwd())


for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.json')):
        with open(filename) as w:
            data = json.load(w)
            coordinate = data['people'][0]['pose_keypoints_2d']
            temp=0

            for i in range(2,54,3):
                if coordinate[i] < 0.5 :
                    temp +=1 

            if temp > 1:
                key_out = os.path.join(input_folder, filename)
                shutil.copy(key_out , output_all2_keypoints)
                image_out_path = os.path.join(image_path, filename).replace('_keypoints.json', '.png')
                shutil.copy(image_out_path , output_all2_photos)
                print(filename + "  all1")
            else:
                key_out = os.path.join(input_folder, filename)
                shutil.copy(key_out , output_all4_keypoints)
                image_out_path = os.path.join(image_path, filename).replace('_keypoints.json', '.png')
                shutil.copy(image_out_path , output_all4_photos)
                print(filename + "  all2")
    

    




'''
    
'''


