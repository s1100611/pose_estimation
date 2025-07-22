
'''
參考資料：
https://blog.csdn.net/qq_64605223/article/details/125606024
https://steam.oxxostudio.tw/category/python/ai/ai-mediapipe-pose.html
'''            

import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import os

#data資料夾路徑
dir_path = 'C:/Users/Win11/Desktop/Graduation_project/'
folder = '2fyou_'
dirs = os.listdir(dir_path + folder + '/')
i=0
j=0
for x in dirs:
    dirs[i] = x.replace('.jpg', "")
    i+=1

os.makedirs(dir_path + 'dataset/marked/' + folder, exist_ok=True)

for name in dirs:
    #导入模型
    mp_pose=mp.solutions.pose
    mp_drawing=mp.solutions.drawing_utils
    pose=mp_pose.Pose(static_image_mode=True,#选择静态图片还是连续视频帧
                 model_complexity=2,#选择人体姿态关键点检测模型，0性能差但快，2性能好但慢，1介于之间
                 smooth_landmarks=True,#是否选择平滑关键点
                 min_detection_confidence=0.5,#置信度阈值
                 min_tracking_confidence=0.5)#追踪阈值


    img = cv2.imread(dir_path + folder + '/' + name + '.jpg')
    #查看读入的图像

    #BGR转RGB
    img_RGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #输入模型，获取预测结果
    results=pose.process(img_RGB)
    mp_drawing.draw_landmarks(img,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)
    
    
    cv2.imwrite(dir_path + 'dataset/marked/' + folder + '/' + name + '_m.png', img)  # 存成 png
    j+=1
    print(j)
    pose.close()

