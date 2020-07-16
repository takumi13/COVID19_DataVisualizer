
import numpy as np

import gen_graph
from create_dic_day import create_dic_day

'''
データソース
https://github.com/kaz-ogiwara/covid19/

東洋経済オンライン編集部の荻野和樹氏が公開している
GitHub (https://github.com/kaz-ogiwara/covid19/)
からCOVID-19の感染者やPCR検査数に関するデータソースをお借りして
簡易的なビジュアライザーを作成した
'''
filepath_japan = './data/prefectures.csv'

debug_flag = False  # Trueならば, グラフ化するデータソースなどをコンソールに出力する

#-----------------------------------------------------------
# 描画の準備
#-----------------------------------------------------------
dic_day_all, dic_day_tokyo = create_dic_day(filepath_japan, debug_flag)

#-----------------------------------------------------------
# 日付
#-----------------------------------------------------------
width = 0.25
days_array = np.array(dic_day_all.keys())
x1 = [i+1       for i in range(len(dic_day_all))]
x2 = [i+1+width for i in range(len(dic_day_all))]

days_label = []
for key in dic_day_all:
    days_label.append(key)

#-----------------------------------------------------------
# 全国の情報をarray化
#-----------------------------------------------------------
japan_plus  = []    # 全国の新規陽性者数
japan_all   = []    # 全国の新規検査人数
japan_ratio = []    # 全国のPCR検査新規陽性率
imgpath_japan_ratio = './img/japan_pcr_ratio.png'
imgpath_japan_num   = './img/japan_pcr_num.png'
imgpath_japan_all   = './img/japan_pcr_all.png'
title_japan_ratio   = 'Japan PCR plus_num and ratio'
title_japan_num     = 'Japan PCR plus_num and inspected_num'
title_japan_all     = 'Japan PCR plus_num and inspected_num and ratio'

for key in dic_day_all:
    japan_plus.append(dic_day_all[key][0])
    japan_all.append(dic_day_all[key][1])
    japan_ratio.append(dic_day_all[key][2])  

#-----------------------------------------------------------
# 東京の情報をarray化
#-----------------------------------------------------------
tokyo_plus  = []    # 東京の新規陽性者数
tokyo_all   = []    # 東京の新規検査人数
tokyo_ratio = []    # 東京のPCR検査新規陽性率
imgpath_tokyo_ratio = './img/tokyo_pcr_ratio.png'
imgpath_tokyo_num   = './img/tokyo_pcr_num.png'
imgpath_tokyo_all   = './img/tokyo_pcr_all.png'
title_tokyo_ratio   = 'Tokyo PCR plus_num and ratio'
title_tokyo_num     = 'Tokyo PCR plus_num and inspected_num'
title_tokyo_all     = 'Tokyo PCR plus_num and inspected_num and ratio'

for key in dic_day_tokyo:
    tokyo_plus.append(dic_day_tokyo[key][0])
    tokyo_all.append(dic_day_tokyo[key][1])
    tokyo_ratio.append(dic_day_tokyo[key][2])


#-----------------------------------------------------------
# 移動平均
# 新規検査人数が3~7日に1回の不定期でまとめて更新されるので
# 移動平均を考慮する
#-----------------------------------------------------------

#-----------------------------------------------------------
# 当日と前後3日間の計7日間の平均
#-----------------------------------------------------------
move_ave_n = 7
k = move_ave_n//2

days_label_ave = days_label[k:-k]
x1_ave = x1[k:-k]
x2_ave = x2[k:-k]
japan_plus_ave = japan_plus[k:-k]
tokyo_plus_ave = tokyo_plus[k:-k]

japan_all_ave = []
tokyo_all_ave = []
for i in range(k, len(tokyo_all)-k):
    japan_all_ave.append(sum(japan_all[i-k : i+k+1]) / move_ave_n)
    tokyo_all_ave.append(sum(tokyo_all[i-k : i+k+1]) / move_ave_n)

japan_ratio_ave = []
tokyo_ratio_ave = []
for i in range(len(japan_all_ave)):
    japan_ratio_ave.append(round(100 * japan_plus_ave[i] / japan_all_ave[i], 1))
    tokyo_ratio_ave.append(round(100 * tokyo_plus_ave[i] / tokyo_all_ave[i], 1))

if debug_flag==True:
    print('Tokyo')
    for i in range(len(japan_plus)):
        print('{} : '.format(days_label[i]) + '{:>3}'.format(tokyo_plus[i]) + ', {:4.1f}'.format(tokyo_all[i]) + ', {:.2f}%'.format(tokyo_ratio[i]))
    print('----------------------------------------------------------')

    print('Japan')
    for i in range(len(japan_plus)):
        print('{} : '.format(days_label[i]) + '{:>3}'.format(japan_plus[i]) + ', {:>5.1f}'.format(japan_all[i]) + ', {:.2f}%'.format(japan_ratio[i]))
    print('----------------------------------------------------------')

#-----------------------------------------------------------
# グラフ作成 (移動平均を考慮)
#-----------------------------------------------------------
gen_graph.create_img_nums(days_label_ave, x1_ave, x2_ave, japan_plus_ave, japan_all_ave, imgpath_japan_num, title_japan_num)
gen_graph.create_img_nums(days_label_ave, x1_ave, x2_ave, tokyo_plus_ave, tokyo_all_ave, imgpath_tokyo_num, title_tokyo_num)

gen_graph.create_img_num_ratio(days_label_ave, x1_ave, japan_ratio_ave, japan_plus_ave, imgpath_japan_ratio, title_japan_ratio)
gen_graph.create_img_num_ratio(days_label_ave, x1_ave, tokyo_ratio_ave, tokyo_plus_ave, imgpath_tokyo_ratio, title_tokyo_ratio)

gen_graph.create_img_all(days_label_ave, x1_ave, x2_ave, japan_plus_ave, japan_all_ave, japan_ratio_ave, imgpath_japan_all, title_japan_all)
gen_graph.create_img_all(days_label_ave, x1_ave, x2_ave, tokyo_plus_ave, tokyo_all_ave, tokyo_ratio_ave, imgpath_tokyo_all, title_tokyo_all)