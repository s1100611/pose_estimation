# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 01:04:28 2024

@author: shama
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import json

# 初始化 Mediapipe 的姿勢偵測模組
mp_pose=mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
pose=mp_pose.Pose(static_image_mode=True,#選擇圖片或是影片
                model_complexity=2,#選擇人體姿態關節點檢測模型，0性能差但快，2性能好但慢，1介於之間
                smooth_landmarks=True,#是否選擇平滑關節點
                min_detection_confidence=0.85,#系統判定姿勢偵測成功的最低可信度分數，範圍是[0,1]
                min_tracking_confidence=0.85)#系統判定姿勢追蹤成功的最低可信度分數


'''
# 初始化 Mediapipe 的背景分割模組
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
'''



# 定義輸入和輸出資料夾
input_folder = r"C:/Users/Win11/Desktop/Graduation_project/tests_18"
output_folder_detected = os.path.join(input_folder, 'path_to_output_folder_detected')


os.makedirs(output_folder_detected, exist_ok=True)



# 關節點名稱
landmark_names = [
    "NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER", "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
    "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT", "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW",
    "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY", "LEFT_INDEX", "RIGHT_INDEX",
    "LEFT_THUMB", "RIGHT_THUMB", "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE",
    "LEFT_HEEL", "RIGHT_HEEL", "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"
]

reordered_indices = [0, 1, 12, 14, 16, 11, 13, 15, 24, 26, 28, 23, 25, 27, 5, 2, 8, 7]  #根據需要自定義



for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Cannot read {filename}")
            continue
       
        #BGR轉RGB
        img_RGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        #輸入模型，獲取預測結果
        pose_results=pose.process(img_RGB)

        if pose_results.pose_landmarks:
            #繪製姿勢偵測結果
            mp_drawing.draw_landmarks(
                image, 
                pose_results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                #landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            #儲存結果圖片
            output_path = os.path.join(output_folder_detected, filename).replace('.jpg', '.png')
            cv2.imwrite(output_path, image)
            print(f"{filename} 偵測到姿勢")

            #重新排序並儲存關節點
            pose_keypoints_2d = []
            landmarks = pose_results.pose_landmarks.landmark

            for idx in reordered_indices:
                if idx == 1:
                    x = (landmarks[11].x + landmarks[12].x)/2
                    y = (landmarks[11].y + landmarks[12].y)/2
                    visibility = (landmarks[11].visibility + landmarks[12].visibility)/2
                else:
                    x, y, visibility = landmarks[idx].x, landmarks[idx].y, landmarks[idx].visibility
                pose_keypoints_2d.extend([x, y, visibility])

            landmarks_data = {
                'people': [{'pose_keypoints_2d': pose_keypoints_2d}]
            }

            json_path = output_path.replace('.jpg', '_keypoints.json').replace('.jpeg', '_keypoints.json').replace('.png', '_keypoints.json')
            with open(json_path, 'w') as f:
                json.dump(landmarks_data, f, indent=4)
        else:
            print(f"{filename} 沒有偵測到姿勢")
            continue