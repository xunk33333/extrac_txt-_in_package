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
    # print(pd.read_csv("output_csv/" + pdf.metadata['Title'] + ".csv"))

    # 读取数据文件
    df = pd.read_csv("output_csv/" + pdf.metadata['Title'] + ".csv")
    # print([100<each<140 for each in df['x0']])

    # 创建结果表
    result = pd.DataFrame()

    # 厚度
    position = [[each/page.width <3/11.5 for each in df['x0']],
            [1/2<each/page.height < 7.1/8.3 for each in df['doctop']],
            [each > -1 for each in df['label']]
            ]
    booll = [all(e) for e in zip(*position)]
    result['厚度'] = df[booll]['text'].to_numpy()
    df.drop(index=df[booll]['text'].index,inplace=True)

    # 外边长
    position = [[each/page.width <4.5/11.5 for each in df['x0']],
            [each/page.height <3.2/8.6 for each in df['doctop']]
            ]
    booll = [all(e) for e in zip(*position)]
    result = pd.concat([result,pd.DataFrame({'外边长':df[booll]['text'].to_numpy()})],axis=1)
    df.drop(index=df[booll]['text'].index,inplace=True)

    # EXPOSED_PAD宽度
    position = [[each/page.width >8/11.5 for each in df['x0']],
            [2.5/9.2< each/page.height <7/9.2 for each in df['doctop']],
                [each > -1 for each in df['label']]
            ]
    booll = [all(e) for e in zip(*position)]
    result = pd.concat([result,pd.DataFrame({'EXPOSED_PAD宽度':df[booll]['text'].to_numpy()})],axis=1)
    df.drop(index=df[booll]['text'].index,inplace=True)

    # 脚长度
    position = [[4/12.5< each/page.width <8/12 for each in df['x0']],
            [1/2< each/page.height <7/8.7 for each in df['doctop']],
                [each > -1 for each in df['label']]
            ]
    booll = [all(e) for e in zip(*position)]
    result = pd.concat([result,pd.DataFrame({'脚长度':df[booll]['text'].to_numpy()})],axis=1)
    df.drop(index=df[booll]['text'].index,inplace=True)

    # 脚宽度
    position = [[2/11.4< each/page.width <5.5/11.4 for each in df['x0']],
            [6/8.4< each/page.height  for each in df['doctop']],
                [each > -1 for each in df['label']]
            ]
    booll1 = [all(e) for e in zip(*position)]

    position = [[4.5/10.7< each/page.width <9/12 for each in df['x0']],
            [1.5/8.8< each/page.height <4/8.7 for each in df['doctop']],
                [each > -1 for each in df['label']]
            ]
    booll2 = [all(e) for e in zip(*position)]

    position = [booll1,
                booll2
            ]
    booll = [any(e) for e in zip(*position)]
    result = pd.concat([result,pd.DataFrame({'脚宽度':df[booll]['text'].to_numpy()})],axis=1)
    df.drop(index=df[booll]['text'].index,inplace=True)
    # print(df)

    # EXPOSED_PAD长度
    position = [[6.5/11.4< each/page.width <9.5/11.4 for each in df['x0']],
            [1/8< each/page.height <4/8.7 for each in df['doctop']],
                [each > -1 for each in df['label']]
            ]
    booll = [all(e) for e in zip(*position)]
    result = pd.concat([result,pd.DataFrame({'EXPOSED_PAD长度':df[booll]['text'].to_numpy()})],axis=1)
    df.drop(index=df[booll]['text'].index,inplace=True)

    if df.empty:
        pass
    else:
        #脚间距
        position = [
            [ each/page.height <4.5/8.4 for each in df['doctop']],
                [each == -1 for each in df['label']]
            ]
        booll = [all(e) for e in zip(*position)]
        result = pd.concat([result,pd.DataFrame({'脚间距':df[booll]['text'].to_numpy()})],axis=1)
        df.drop(index=df[booll]['text'].index,inplace=True)

    if df.empty:
        pass
    else:
         #拐角限制
        position = [[8/12< each/page.width for each in df['x0']],
            [ 4.5/8.4< each/page.height  for each in df['doctop']],
                [each == -1 for each in df['label']]
            ]
        booll = [all(e) for e in zip(*position)]
        result = pd.concat([result,pd.DataFrame({'拐角限制':df[booll]['text'].to_numpy()})],axis=1)
        df.drop(index=df[booll]['text'].index,inplace=True)

    if df.empty:
        pass
    else:# 剩余side view参数
        df = df.sort_values('doctop')
        position = [
            [5.5/8.7< each/page.height for each in df['doctop']],
                [each == -1 for each in df['label']]
            ]
        booll = [all(e) for e in zip(*position)]
        side_view = df[booll]['text']
        df.drop(index=df[booll]['text'].index,inplace=True)
        result = pd.concat([result,pd.DataFrame({'芯片底到pcb最大距离':side_view[0:1].to_numpy()})],axis=1)
        side_view.drop(index=side_view[0:1].index,inplace=True)
        result = pd.concat([result,pd.DataFrame({'芯片底到pcb标准距离':side_view[0:1].to_numpy()})],axis=1)
        side_view.drop(index=side_view[1:2].index,inplace=True)
        result = pd.concat([result,pd.DataFrame({'针脚到pcb距离':side_view.tail(1).to_numpy()})],axis=1)
        side_view.drop(index=side_view.tail(1).index,inplace=True)
        result = pd.concat([result,pd.DataFrame({'COPLANARITY':side_view.to_numpy()})],axis=1)
        result = pd.concat([result,pd.DataFrame({'未分类':df['text'].to_numpy()})],axis=1)



    result.to_csv("result_csv/" + pdf.metadata['Title'] + ".csv",index=False,encoding='utf-8-sig')


if __name__ == '__main__':
    pass
