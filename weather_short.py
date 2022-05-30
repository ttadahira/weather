# coding: UTF-8
#コメント（折居）
from calendar import calendar
import os
from flask import Flask, render_template, request, redirect, url_for

# デバッグを有効
os.environ["FLASK_ENV"] = "development"

# データの取得
data = []
data_count = 0
with open('data/data.csv', 'r') as f:
    for line in f:
        data_count += 1
        if data_count >= 7:
            line = line.replace('\n', '')
            line = line.split(',')
            # 日付、天気、最高気温、最低気温のデータ
            new_line = [line[0], line[1], line[4], line[7]]
            data.append(new_line)

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
    # check_date.htmlを実行
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

@app.route('/select_region/<area>')
def select_area(area):
    area = str(area)
    return render_template(f'area/{area}.html', chosen_date=chosen_date)

@app.route('/pick_city/<city>')
def pick_city(city):
    return render_template('calender.html', city=city, chosen_date=chosen_date)


# 実行
if __name__ == "__main__":
    app.run()