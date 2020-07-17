# COVID19_DataVisualizer

東洋経済オンライン編集部の荻野和樹氏が公開しているGitHub  
(https://github.com/kaz-ogiwara/covid19/)  
からCOVID-19の感染者やPCR検査数に関するデータソースを利用して,  
東京都における 新規感染者数(人)・新規PCR検査数(人)・陽性率(%) をグラフ化し,   
画像データとして保存するプログラム.  
データソースは適宜最新版を上記URLからcloneして使うことを推奨する.

```bash
git clone https://github.com/kaz-ogiwara/covid19.git
```
 
# 生成される画像
緑の棒線 : 新規PCR検査数  
青い棒線 : 新規感染者数  
赤い折れ線 : 陽性率(%) = 100*新規感染者数 / 新規PCR検査数  
![tokyo_pcr_all](https://user-images.githubusercontent.com/38643137/87735483-9d298f80-c810-11ea-9eaa-c87e30df1dd1.png)

# 動作環境
Windows10  
python 3.7.5  
 
# プログラムの使い方
 
```bash
git clone https://github.com/takumi13/COVID19_DataVisualizer.git
cd COVID19_DataVisualizer
python main.py
```

# 注意事項
PCR検査数は, 毎日正確な数がデータに反映されるわけではなく,   
何日か分をまとめてデータに反映させることが多いので,  
今回作成するグラフでは, PCR検査数を当日と前後3日間の計7日間の平均値として算出している.  
なお, 感染者数は毎日ほぼ正確な数がデータに反映されている (らしい) ので, 移動平均等は考慮していない.  
