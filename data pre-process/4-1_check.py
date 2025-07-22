import os

# 指定要列出所有檔案的目錄
path1 = "C:/Users/Win11/Desktop/Graduation_project/dataset/marked"
path2 = "C:/Users/Win11/Desktop/Graduation_project/photos"

# 取得所有檔案與子目錄名稱
files1 = os.listdir(path1)
files2 = os.listdir(path2)

for filename in files1:
    filename = filename.replace("_m.png",'.jpg' )
    if filename not in files1:
        print(filename)