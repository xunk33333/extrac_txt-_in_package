import os
import test

path = "data_pdf"
files = os.listdir(path)

for file_path in files:
    test.test_one(path+'/'+file_path)
