import os

# 指定要列出所有檔案的目錄
path = "C:/Users/Win11/Desktop/Graduation_project/only.grapher"

# 取得所有檔案與子目錄名稱
files = os.listdir(path)

for filename in files:
    if filename[-1] != 'g':
        os.remove(path+'/'+filename) 