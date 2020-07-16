
'''
[参考URL]
非IT企業に勤める中年サラリーマンのIT日記
http://pineplanter.moo.jp/non-it-salaryman/2018/03/23/python-2axis-graph/
'''

import matplotlib.pyplot as plt
import numpy as np

day_slice=7     # グラフに表示する日付の間隔

#-----------------------------------------------------------
# 陽性者数(棒グラフ)
# 陽性率(折れ線グラフ)
# の2つを表示
#-----------------------------------------------------------
def create_img_num_ratio(days_label, x, y_ratio, y_plus, imgpath, title):
    plt.clf()
    width = 1.0

    #第一軸(ax1)と第二軸(ax2)を作って関連付ける
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    #第一軸を折れ線グラフ、第二軸を棒グラフに
    ax1.plot(x, y_ratio, linewidth=width, color="red", linestyle="solid", marker="o", markersize=1, label='plus_ratio')
    ax2.bar(x, y_plus, width=width, edgecolor="black", linewidth=0.1, label='plus')
    
    #y軸の範囲 今回は第二軸のみとした
    ax1.set_ylim([0,100])
    
    #重ね順として折れ線グラフを前面に。
    #そうしないと棒グラフに折れ線が隠れてしまうので。
    ax1.set_zorder(2)
    ax2.set_zorder(1)
    
    #折れ線グラフの背景を透明に。
    #そうしないと重ね順が後ろに回った棒グラフが消えてしまう。
    ax1.patch.set_alpha(0)
    
    #凡例を表示（グラフ左上、ax2をax1のやや下に持っていく）
    ax1.legend(bbox_to_anchor=(0, 1)  , loc='upper left', borderaxespad=0.5, fontsize=10)
    ax2.legend(bbox_to_anchor=(0, 0.9), loc='upper left', borderaxespad=0.5, fontsize=10)
    
    #グリッド表示(ax2のみ)
    ax2.grid(True)
    
    #軸ラベルを表示
    plt.xticks(x[::day_slice], days_label[::day_slice], rotation='vertical', size='small')
    # plt.xticks(x, ['' for i in range(len(x))])
    fig.autofmt_xdate(rotation=45)
    ax1.set_ylabel('ratio[%]')
    ax2.set_ylabel('num')

    ax1.set_title(title)
    
    plt.savefig(imgpath)
    plt.close()

#-----------------------------------------------------------
# 陽性者数(棒グラフ)
# PCR検査数(棒グラフ)
# の2つを表示
#-----------------------------------------------------------
def create_img_nums(days_label, x1, x2, y_plus, y_all, imgpath, title):
    plt.clf()
    fig, ax = plt.subplots()
    width = x2[0] - x1[0]
    x3 = [0 for i in range(len(x1))]
    for i in range(len(x3)):
        x3[i] = x1[i] + width/2

    ax.bar(x1, y_plus, color='b', edgecolor="black", width=width, linewidth=0.1, label='plus'     , align="center")
    ax.bar(x2, y_all , color='g', edgecolor="black", width=width, linewidth=0.1, label='inspected', align="center")

    ax.legend(loc=2)

    plt.xticks(x3[::day_slice], days_label[::day_slice], rotation='vertical', size='small')
    fig.autofmt_xdate(rotation=45)
    plt.ylabel('num')

    ax.set_title(title)
    plt.savefig(imgpath)
    plt.close()

#-----------------------------------------------------------
# 陽性者数(棒グラフ)
# PCR検査数(棒グラフ)
# 陽性率(折れ線グラフ)
# 3つを表示
#-----------------------------------------------------------
def create_img_all(days_label, x1, x2, y_plus, y_all, y_ratio, imgpath, title):
    plt.clf()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    width = x2[0] - x1[0]
    x3 = [0 for i in range(len(x1))]
    for i in range(len(x3)):
        x3[i] = x1[i] + width/2

    ax1.set_ylim([0, 100])

    ax1.plot(x3, y_ratio, linewidth=width*3, color="red", linestyle="solid", marker="o", markersize=1, label='plus_ratio')
    ax2.bar(x1, y_plus, color='b', edgecolor="black", width=width, linewidth=0.1, label='plus'     , align="center")
    ax2.bar(x2, y_all , color='g', edgecolor="black", width=width, linewidth=0.1, label='inspected', align="center")

    #重ね順として折れ線グラフを前面に。
    #そうしないと棒グラフに折れ線が隠れてしまうので。
    ax1.set_zorder(2)
    ax2.set_zorder(1)
    
    #折れ線グラフの背景を透明に。
    #そうしないと重ね順が後ろに回った棒グラフが消えてしまう。
    ax1.patch.set_alpha(0)
    
    #凡例を表示（グラフ左上、ax2をax1のやや下に持っていく）
    ax1.legend(bbox_to_anchor=(0, 1)  , loc='upper left', borderaxespad=0.5, fontsize=10)
    ax2.legend(bbox_to_anchor=(0, 0.9), loc='upper left', borderaxespad=0.5, fontsize=10)
    
    #グリッド表示(ax2のみ)
    ax2.grid(True)

    plt.xticks(x3[::day_slice], days_label[::day_slice], rotation='vertical', size='small')
    fig.autofmt_xdate(rotation=45)
    ax1.set_ylabel('ratio[%]')
    ax2.set_ylabel('num')

    ax1.set_title(title)

    plt.savefig(imgpath)
    plt.close()