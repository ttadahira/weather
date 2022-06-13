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
    # htmlに渡す日付リストの作成
    date_list = []
    count = 0
    for line in data:
        if line[0] not in date_list:
            count += 1
            date_list.append(line[0])
            # 一番古い日付と一番新しい日付の取得
            get_date = line[0].split('/')
            date_time = datetime.date(int(get_date[0]), int(get_date[1]), int(get_date[2]))
            if count == 1:
                oldest_list = [date_time, get_date]
                latest_list = [date_time, get_date]
            else:
                # 一番古い日付
                if date_time < oldest_list[0]:
                    oldest_list = [date_time, get_date]
                # 一番新しい日付
                if date_time > latest_list[0]:
                    latest_list = [date_time, get_date]
    # 古い日付をグローバル化
    global oldest_year, oldest_month, oldest_day
    oldest_year = oldest_list[1][0]
    oldest_month = oldest_list[1][1]
    oldest_day= oldest_list[1][2]
    # 新しい日付をグローバル化
    global latest_year, latest_month, latest_day
    latest_year = latest_list[1][0]
    latest_month = latest_list[1][1]
    latest_day = latest_list[1][2]
    # htmlに渡す日付データの作成
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
    return render_template('calendar.html', region=region, city=city, chosen_date=chosen_date, chosen_year=chosen_year, chosen_month=chosen_month, chosen_day=chosen_day, data=data_str)


# 実行
if __name__ == "__main__":
    app.run()