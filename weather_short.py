# coding: UTF-8
#コメント（折居）
import os
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

app = Flask(__name__)

# トップページ
@app.route('/')
def top():
    #トップページに遷移するとdateを初期化する
    global chosen_date
    chosen_date = False
    return render_template('top.html')

# トップページ(ロゴからの遷移用)
@app.route('/', methods = ["POST"])
def return_top():
    #トップページに遷移するとdateを初期化する
    global chosen_date
    chosen_date = False
    return render_template('top.html')

# 日付選択ページ
@app.route('/select_date', methods = ["POST"])
def select_date():
    # htmlに渡す日付データの作成
    date_list = []
    for line in data:
        date_list.append(line[0])
    date = ",".join(date_list)
    # select_date.htmlを実行
    return render_template('select_date.html', date=date)

@app.route('/index', methods = ["POST"])
def index():
    # ユーザに選択された日付
    date = request.form['date']
    global chosen_date
    chosen_date = date
    return render_template('select_region.html', chosen_date=chosen_date)

@app.route('/select_region', methods = ["POST", "GET"])
def select_region():
    return render_template('select_region.html')

@app.route('/select_region/<area>', methods = ["POST", "GET"])
def select_area(area):
    area = str(area)
    return render_template(f'area/{area}.html', chosen_date=chosen_date)

# カレンダー表示ページ
@app.route('/pick_city/<city>')
def pick_city(city):
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
    return render_template('calendar.html', city=city, chosen_date=chosen_date, data=data_str)


# 実行
if __name__ == "__main__":
    app.run()