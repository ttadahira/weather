#実行するとweather_data2.csvファイルが生成or上書きされる
import requests
import csv
from bs4 import BeautifulSoup

#place_codeA = [44] #都道府県コード 東京：44 茨城県：40
#place_codeB = [47662] #地域コード 東京：47662 つくば市：47646 水戸市：47629
#place_name = ["weather_data"] #ファイル名

place_codeA = [14, 21, 23, 31, 32, 33, 35, 34, 36, 54, 56, 55, 48, 41, 57, 42, 43, 40, 52, 51, 49, 45, 53, 50, 46, 68, 69, 61, 60, 67, 66, 63, 65, 64, 73, 72, 74, 71, 81, 82, 85, 83, 84, 86, 88, 87, 91]
place_codeB = [47412, 47423, 47430, 47575, 47582, 47584, 47588, 47590, 47595, 47604, 47605, 47607, 47610, 47615, 47616, 47624, 47626, 47629, 47632, 47636, 47638, 47648, 47651, 47656, 47670, 47741, 47746, 47759, 47761, 47765, 47768, 47770, 47777, 47780, 47887, 47891, 47893, 47895, 47762, 47807, 47813, 47815, 47817, 47819, 47827, 47830, 47936]
place_name = ["sapporo", "muroran", "hakodate", "aomori", "akita", "morioka", "yamagata", "sendai", "hukusima", "nigata", "kanazawa", "toyama", "nagano", "utsunomiya", "hukui", "maebashi", "kumagaya", "mito", "gihu", "nagoya", "kohu", "choushi", "tsu", "shizuoka", "yokohama", "matue", "tottori", "kyoto", "hikone", "hirosima", "okayama", "kobe", "wakayama", "nara", "matsuyama", "takamatsu", "kochi", "hukushima", "simonoseki", "hukuoka", "saga", "oita", "nagasaki", "kumamoto", "kagoshima", "miyazaki", "naha"]
ja_names = ["札幌", "室蘭", "函館", "青森", "秋田", "盛岡", "山形", "仙台", "福島", "新潟", "金沢", "富山", "長野", "宇都宮", "福井", "前橋", "熊谷", "水戸", "岐阜", "名古屋", "甲府", "銚子", "津", "静岡", "横浜", "松江", "鳥取", "京都", "彦根", "広島", "岡山", "神戸", "和歌山", "奈良", "松山", "高松", "高知", "徳島", "下関", "福岡", "佐賀", "大分", "長崎", "熊本", "鹿児島", "宮崎", "那覇"]

# 気象庁のURL
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=1&view=p1" #日ごと

#str to float
def str2float(str):
  try:
    return float(str)
  except:
    return 0.0

if __name__ == "__main__":
  #都市を網羅
  for place, ja_name in zip(place_name, ja_names):
    #最終的にデータを集めるリスト
    All_list = []
    row_list = ['年月日', '平均気温', '天気概況（昼）', '都市']
    print(place)
    print(ja_name)
    index = place_name.index(place)

    # for文で該当期間抽出
    for year in range(2022,2023):
      print(year)
      # その年の1月～12月の12回を網羅する
      for month in range(1,13):
        #2つの都市コードと年と月を当てはめる
        r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month))
        r.encoding = r.apparent_encoding

        # サイトごとスクレイピング
        soup = BeautifulSoup(r.text)
        # findAllで条件に一致するものをすべて抜き出す
        # trタグでclassがmtxになっているものを対象
        rows = soup.findAll('tr',class_='mtx')

        # 表の最初の1~4行目はカラム情報なのでスライス
        rows = rows[4:]

        # 1日〜最終日までの１行を取得
        for row in rows:
          # trのなかのtdをすべて抜き出す
          data = row.findAll('td')

          #データ取り出し
          rowData = [] #空
          rowData.append(str(year) + "/" + str(month) + "/" + str(data[0].string)) #年月日
          #文字列を数字(float)に変換
          rowData.append(str2float(data[7].string)) #最高気温
          rowData.append(str2float(data[8].string)) #最低気温
          rowData.append(data[19].string) #天気概況（昼）
          rowData.append(ja_name)

          #次の行にデータを追加
          All_list.append(rowData)

    #都市ごとにファイルを生成(csvファイル形式。名前は都市名)
    if place == "sapporo":
      with open('data/weather_data.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(row_list)
        writer.writerows(All_list)
    else:
      with open('data/weather_data.csv', 'a',encoding="utf_8_sig") as file: #文字化け防止
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(All_list)