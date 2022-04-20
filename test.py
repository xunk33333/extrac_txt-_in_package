import numpy as np
import csv
import re
from sklearn.cluster import KMeans
import pdfplumber


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
        x = list(readers)
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
        for wword in word:
            if check(wword['text']):
                continue
            elif wword['text'].__contains__('.'):
                row = list(wword.values())[0:6]
                write = csv.writer(f)
                write.writerow(row)

    name, information = dataset("output_csv/" + pdf.metadata['Title'] + ".csv")
    n_clusters = 11
    km = KMeans(n_clusters=n_clusters)
    label = km.fit_predict(information)
    Cluster = [[] for _ in range(n_clusters)]
    for i in range(len(name)):
        Cluster[label[i]].append(name[i])
    # for i in range(len(Cluster)):
    #     print(Cluster[i])
    with open("result_csv/" + pdf.metadata['Title'] + ".csv", 'w', newline='') as f:
        for cluster in Cluster:
            write = csv.writer(f)
            write.writerow(cluster)


if __name__ == '__main__':
    pass
