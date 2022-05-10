import os
import test

path = "data_pdf"
files = os.listdir(path)

for file_path in files:
    print('当前文件：'+file_path)
    test.test_one(path+'/'+file_path)
    print('yes：' + file_path)
