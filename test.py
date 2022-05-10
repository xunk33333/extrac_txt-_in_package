import numpy as np
import csv
import re
import pdfplumber
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN


def check(strr):
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, strr)
    if len(res):
        return True
    else:
        return False


def dataset(filepath):
    nname = []
    iinformation = []
    with open(filepath, 'r+') as f:
        readers = csv.reader(f, delimiter=",")
        x = list(readers)[1:]
        data = np.array(x)
        for line in data:
            nname.append(line[0])
            iinformation.append([np.double(line[i]) for i in range(1, len(line))])
        return nname, iinformation


def test_one(file_path):
    pdf = pdfplumber.open(file_path)
    page = pdf.pages[0]
    word = page.extract_words(y_tolerance=-1)

    with open("output_csv/" + pdf.metadata['Title'] + ".csv", 'w', newline='') as f:
        row = list(word[0].keys())[0:6]
        row.pop(3)
        write = csv.writer(f)
        write.writerow(row)
        for wword in word:
            if check(wword['text']):
                continue
            # row = list(wword.values())[0:6]
            # write = csv.writer(f)
            # write.writerow(row)
            elif wword['text'].__contains__('.'):
                row = list(wword.values())[0:6]
                row.pop(3)
                write = csv.writer(f)
                write.writerow(row)

    name, information = dataset("output_csv/" + pdf.metadata['Title'] + ".csv")

    X = StandardScaler().fit_transform(information)
    db = DBSCAN(eps=0.3,min_samples=3).fit(X)
    # print(name)
    # print(db.labels_)
    # print(db.core_sample_indices_)

    date = pd.read_csv("output_csv/" + pdf.metadata['Title'] + ".csv")
    # print(date)
    # print(db.labels_)
    date['label'] = db.labels_
    date.to_csv("output_csv/" + pdf.metadata['Title'] + ".csv",index=False)


if __name__ == '__main__':
    pass
