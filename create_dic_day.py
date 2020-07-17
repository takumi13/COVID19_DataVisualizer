
import csv
import copy
from pprint import pprint
import math

def create_dic_day(filepath_japan, debug_flag):
    #-----------------------------------------------------------
    # csvファイルの読み込み. PCR検査数
    #-----------------------------------------------------------
    with open(filepath_japan, encoding='utf-8') as f:
        lines = f.readlines()

    #-----------------------------------------------------------
    # 都道府県の情報を消したリスト
    # ['月日', ある都道府県の累計陽性数, ある都道府県の累計検査数]
    # ['0401',                    120,                    2500]
    # data_japan : 全都道府県のデータ
    # data_tokyo : 東京のみのデータ
    #-----------------------------------------------------------
    lines = lines[1:]
    data_japan = []
    data_tokyo = []
    for line in lines:
        line = line.split(',')
        line = [line[0], line[1], line[2], line[3], line[5], line[6]]   # [2020, 5, 21, 東京, 60, 100]
        if line[5] == '""':
            line[5] = '0'
        line[1] = line[1].rjust(2, '0')
        line[2] = line[2].rjust(2, '0')
        if '東京' in line[3]:
            data_tokyo.append([line[1]+line[2], int(line[4]), int(line[5])])
        data_japan.append([line[1]+line[2], int(line[4]), int(line[5])])

    #-----------------------------------------------------------
    # 主に3月にPCR検査数が空白(直前で0に直している)の日が多数あるので
    # 概数を格納するために, 累計陽性数と累計PCR検査数に対して, 
    # ratio = 累計PCR検査数 / 累計陽性数
    # を計算し, 0 の部分には (陽性数は必ず存在するので) 陽性数に
    # ratioを乗じた値を格納している
    #-----------------------------------------------------------
    sum_plus = 0
    sum_japan  = 0

    today = data_tokyo[-1][0]
    print('today={}'.format(today))
    for i in range(len(data_japan)-1, len(data_japan)-48, -1):  # 47都道府県それぞれの, 累計感染者数・累計検査数にアクセスするためのfor文
        if data_japan[i][0] == today:                           # 念のためif文で制御
            sum_plus  += data_japan[i][1]                       # 各都道府県の累計感染者数
            sum_japan += data_japan[i][2]                       # 各都道府県の累計検査数

    ratio = sum_japan / sum_plus                                # 陽性率の逆数 (陽性者1人当たりのPCR検査数の平均)

    for d in data_japan:
        if d[2] == 0:                                           # もし, PCR検査数が0人の日があれば
            d[2] = math.floor(d[1] * ratio)                     # その日のPCR検査数を 陽性者数 × 陽性者1人当たりのPCR検査数の平均 とする

    for d in data_tokyo:
        if d[2] == 0:                                           # もし, PCR検査数が0人の日があれば
            d[2] = math.floor(d[1] * ratio)                     # その日のPCR検査数を 陽性者数 × 陽性者1人当たりのPCR検査数の平均 とする

    #-----------------------------------------------------------
    # 辞書型の定義
    # {'月日' : [累計陽性者数, 累計PCR検査数]}
    # d[0]には '月日' が入っているので, それを辞書のキーとして足し合わせる
    # ここでは, 該当する月日の47都道府県の陽性者数・PCR検査数をすべて足し合わせる
    #-----------------------------------------------------------
    dic_japan = {}
    dic_tokyo = {}

    for d in data_tokyo:                # 各月日における累計陽性者数, 累計PCR検査数の初期化
        dic_japan[d[0]] = [0, 0]
        dic_tokyo[d[0]] = [0, 0]

    for d in data_japan:                # 該当する月日をキーとして累計陽性者数, 累計PCR検査数
        dic_japan[d[0]][0] += d[1]
        dic_japan[d[0]][1] += d[2]

    for d in data_tokyo:
        dic_tokyo[d[0]][0] += d[1]
        dic_tokyo[d[0]][1] += d[2]

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
    # {'月日' : 新規陽性者数, 新規PCR検査数}
    # 0311はとばして0312から新規人数を格納するため, i>0とする
    # 陽性率は130行目にappendしている
    #-----------------------------------------------------------
    dic_day_japan   = {}
    dic_day_tokyo = {}

    i = 0
    for day in dic_japan:
        if i > 0:
            dic_day_japan[day] = [list_japan[i][1] - list_japan[i-1][1], list_japan[i][2] - list_japan[i-1][2]] # {'月日' : 新規陽性者数, 新規PCR検査数}
            dic_day_tokyo[day] = [list_tokyo[i][1] - list_tokyo[i-1][1], list_tokyo[i][2] - list_tokyo[i-1][2]] # {'月日' : 新規陽性者数, 新規PCR検査数}
            if dic_day_tokyo[day][1] == 0:
                dic_day_tokyo[day][1] = dic_day_tokyo[day][0]*10
        i += 1

    i = 0
    for day in dic_japan:
        if i > 0:
            if dic_day_tokyo[day][1] == 0:
                dic_day_tokyo[day][1] = dic_day_tokyo[day][0]*10
            if dic_day_japan[day][1] == 0:
                dic_day_japan[day][1] = dic_day_japan[day][0]*10
        i += 1

    if debug_flag==True:
        print('----------------------------------------------------------')
        print('sum_plus = {}'.format(sum_plus))
        print('sum_japan  = {}'.format(sum_japan))
        print('ratio = {}'.format(ratio))
        print('plus/pcr_num [%] = {}'.format(1.0/ratio))

    return dic_day_japan, dic_day_tokyo