
import csv
import copy
from pprint import pprint
import math

def create_dic_day(filepath):
    #-----------------------------------------------------------
    # csvファイルの読み込み. PCR検査数
    #-----------------------------------------------------------
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    #-----------------------------------------------------------
    # 都道府県の情報を消したリスト
    # ['月日', ある都道府県の累計陽性数, ある都道府県の累計検査数]
    # ['0401',                    120,                    2500]
    # data_japan : 全都道府県のデータ
    # data_tokyo : 東京のみのデータ
    #-----------------------------------------------------------
    lines = lines[1:]   # 1行目の行タイトルを削除
    data_japan = []     # 全都道府県のデータ
    data_tokyo = []     # 東京のみのデータ
    for line in lines:
        line = line.split(',')
        #      [     年,      月,      日, 都道府県, 累計感染者数, 累計PCR検査数]
        line = [line[0], line[1], line[2], line[3],      line[5],       line[6]]   # [2020, 5, 21, 東京, 60, 100]
        if line[5] == '""':                 # PCR検査数が未定義ならば
            line[5] = '0'                   # '0'を代入する(正規化処理)
        line[1] = line[1].rjust(2, '0')     # 月を'01'~'12'に正規化
        line[2] = line[2].rjust(2, '0')     # 日を'01'~'31'に正規化
        if '東京' in line[3]:
            data_tokyo.append([line[1]+line[2], int(line[4]), int(line[5])])
        #                 [月日,  ある都道府県の累計陽性者数, ある都道府県の累計検査数 ]
        data_japan.append([line[1]+line[2], int(line[4]), int(line[5])])

    #-----------------------------------------------------------
    # 辞書型の定義
    # {'月日' : [累計陽性者数, 累計PCR検査数]}
    # d[0]には '月日' が入っているので, それを辞書のキーとして足し合わせる
    # ここでは, 該当する月日の47都道府県の陽性者数・PCR検査数をすべて足し合わせる
    #-----------------------------------------------------------
    dic_japan = {}                      # 日本 {'月日' : [累計陽性者数, 累計PCR検査数]}
    dic_tokyo = {}                      # 東京 {'月日' : [累計陽性者数, 累計PCR検査数]}

    for d in data_tokyo:                # 各月日における累計陽性者数, 累計PCR検査数の初期化
        dic_japan[d[0]] = [0, 0]
        dic_tokyo[d[0]] = [0, 0]

    for d in data_japan:                # 該当する月日をキーとして累計陽性者数, 累計PCR検査数を計算
        dic_japan[d[0]][0] += d[1]      # d[0]県の累計陽性者数を加算
        dic_japan[d[0]][1] += d[2]      # d[0]県の累計PCR検査数を加算

    for d in data_tokyo:                # 該当する月日をキーとして累計陽性者数, 累計PCR検査数を計算
        dic_tokyo[d[0]][0] += d[1]      # d[0]県の累計陽性者数を加算
        dic_tokyo[d[0]][1] += d[2]      # d[0]県の累計PCR検査数を加算

    #-----------------------------------------------------------
    # リスト型の定義
    # ['月日', 累計陽性者数, 累計PCR検査数]
    # このあとの処理で扱いやすくするために辞書型をリスト型に変更する
    #-----------------------------------------------------------
    list_japan = []
    list_tokyo = []
    for day in dic_japan:
        list_japan.append([day, dic_japan[day][0], dic_japan[day][1]])
        list_tokyo.append([day, dic_tokyo[day][0], dic_tokyo[day][1]])

    #-----------------------------------------------------------
    # 辞書型の定義
    # {'月日' : [新規陽性者数, 新規PCR検査数]}
    # 0311はとばして0312から新規人数を格納するため, i>0とする
    #-----------------------------------------------------------
    dic_day_japan = {}   # 日本 {'月日' : [新規陽性者数, 新規PCR検査数]}
    dic_day_tokyo = {}   # 東京 {'月日' : [新規陽性者数, 新規PCR検査数]}

    for i, day in enumerate(dic_japan):
        if i > 0:
            dic_day_japan[day] = [list_japan[i][1] - list_japan[i-1][1], list_japan[i][2] - list_japan[i-1][2]] # {'月日' : 新規陽性者数, 新規PCR検査数}
            dic_day_tokyo[day] = [list_tokyo[i][1] - list_tokyo[i-1][1], list_tokyo[i][2] - list_tokyo[i-1][2]] # {'月日' : 新規陽性者数, 新規PCR検査数}

    return dic_day_japan, dic_day_tokyo