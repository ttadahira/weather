# coding: UTF-8
#コメント（折居）
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for

# デバッグを有効
os.environ["FLASK_ENV"] = "development"

# データの取得
data = []
count = 0
with open('data/new_weather_data.csv', 'r', encoding='utf-8') as f:
    for line in f:
        count += 1
        if count >= 2:
            line = line.replace('\n', '')
            line = line.split(',')
            # 日付、最高気温、最低気温、天気、地域のデータ
            data.append(line)

# 一番古い日付と一番新しい日付の取得
count = 0
for line in data:
    count += 1
    get_date = line[0].split('/')
    date_time = datetime.date(int(get_date[0]), int(get_date[1]), int(get_date[2]))
    if count == 1:
        oldest_list = [date_time, get_date]
        latest_list = [date_time, get_date]
    else:
        # 一番古い日付の更新
        if date_time < oldest_list[0]:
            oldest_list = [date_time, get_date]
        # 一番新しい日付の更新
        if date_time > latest_list[0]:
            latest_list = [date_time, get_date]
# 古い日付
oldest_year = oldest_list[1][0]
oldest_month = oldest_list[1][1]
oldest_day= oldest_list[1][2]
# 新しい日付    
latest_year = latest_list[1][0]
latest_month = latest_list[1][1]
latest_day = latest_list[1][2]

#dateの初期値はFalse
chosen_date = False
chosen_year = False
chosen_month = False
chosen_day = False

app = Flask(__name__)

# トップページ
@app.route('/')
def top():
    #トップページに遷移するとdateを初期化する
    global chosen_date, chosen_year, chosen_month, chosen_day
    chosen_date = False
    chosen_year = False
    chosen_month = False
    chosen_day = False
    return render_template('top.html')

# トップページ(ロゴからの遷移用)
@app.route('/', methods = ["POST"])
def return_top():
    #トップページに遷移するとdateを初期化する
    global chosen_date, chosen_year, chosen_month, chosen_day
    chosen_date = False
    chosen_year = False
    chosen_month = False
    chosen_day = False
    return render_template('top.html')

# 日付選択ページ
@app.route('/select_date', methods = ["POST"])
def select_date():
    # htmlに渡す日付データの作成
    date_list = []
    for line in data:
        if line[0] not in date_list:
            date_list.append(line[0])
    date = ",".join(date_list)
    # select_date.htmlを実行
    return render_template('select_date.html', date=date, oldest_year=oldest_year, oldest_month=oldest_month, oldest_day=oldest_day ,latest_year=latest_year, latest_month=latest_month, latest_day=latest_day)

@app.route('/index', methods = ["POST"])
def index():
    # ユーザに選択された日付
    date = request.form['date']
    global chosen_date, chosen_year, chosen_month, chosen_day
    chosen_date = date.split('/')
    chosen_year = chosen_date[0]
    chosen_month = chosen_date[1]
    chosen_day = chosen_date[2]
    return render_template('select_region.html', chosen_year=chosen_year, chosen_month=chosen_month, chosen_day=chosen_day)

@app.route('/select_region', methods = ["POST", "GET"])
def select_region():
    return render_template('select_region.html')

@app.route('/select_region/<area>', methods = ["POST", "GET"])
def select_area(area):
    area = str(area)
    return render_template(f'area/{area}.html', chosen_year=chosen_year, chosen_month=chosen_month, chosen_day=chosen_day)

# カレンダー表示ページ
@app.route('/pick_city/<region>/<city>', methods = ["POST", "GET"])
def pick_city(region, city):
    count = 0
    data_str = ""
    for line in data:
        if line[4] == city:
            count += 1
            line_str = ','.join(line)
            if count == 1:
                data_str = data_str + line_str
            else:
                data_str = data_str + '\n' + line_str
    city_dict = {"札幌":"さっぽろ", "室蘭":"むろらん", "函館":"はこだて", "旭川":"あさひかわ", "釧路":"くしろ", "青森":"あおもり", "秋田":"あきた", "盛岡":"もりおか", "山形":"やまがた", "仙台":"せんだい", \
                 "福島":"ふくしま", "新潟":"にいがた", "金沢":"かなざわ", "富山":"とやま", "長野":"ながの", "宇都宮":"うつのみや", "福井":"ふくい", "前橋":"まえばし", "熊谷":"くまがや", "水戸":"みと", \
                 "岐阜":"ぎふ", "名古屋":"なごや", "甲府":"こうふ", "銚子":"ちょうし", "津":"つ", "静岡":"しずおか", "東京":"とうきょう", "横浜":"よこはま", "松江":"まつえ", "鳥取":"とっとり", "京都":"きょうと", \
                 "彦根":"ひこね", "広島":"ひろしま", "岡山":"おかやま", "神戸":"こうべ", "大阪":"おおさか", "和歌山":"わかやま", "奈良":"なら", "松山":"まつやま", "高松":"まつやま", "高知":"こうち", "徳島":"とくしま", \
                 "下関":"しものせき", "福岡":"ふくおか", "佐賀":"さが", "大分":"おおいた", "長崎":"ながさき", "熊本":"くまもと", "鹿児島":"かごしま", "宮崎":"みやざき", "那覇":"なは"}
    city_ruby = city_dict[city]
    return render_template('calendar.html', region=region, city=city, city_ruby=city_ruby, chosen_date=chosen_date, chosen_year=chosen_year, chosen_month=chosen_month, chosen_day=chosen_day, oldest_year=oldest_year, oldest_month=oldest_month, oldest_day=oldest_day ,latest_year=latest_year, latest_month=latest_month, latest_day=latest_day, data=data_str)


# 実行
if __name__ == "__main__":
    app.run()