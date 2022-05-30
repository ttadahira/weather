# coding: UTF-8
#ああああああああああああああああああああああああああああああああ
#いいいいいいいいいいいいいいいいいいいいいいいいいいいいいいいい
#うううううううううううううううううううううううううううううううう
#ええええええええええええええええええええええええええええええええ
import os
from flask import Flask, request

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
            # 日付データリスト
            date = line[0].split('/')
            # 日付、天気、最高気温、最低気温のデータ
            new_line = [date, line[1], line[4], line[7]]
            data.append(new_line)

app = Flask(__name__)

#　１ページ目
@app.route('/')
def sample():
    # 本文
    s = '<!DOCTYPE html>'
    s += '<html>'
    s += '<head><link href="/static/style.css" rel="stylesheet" type="text/css">'
    s += '<title>天気</title>'
    s += '</head>'
    s += '<body>'

    # カレンダー
    s += '<div class="wrapper">'
    s += '<h1 id="header"></h1>'
    s += '<div id="next-prev-button">'
    s += '<button id="prev" onclick="prev()">‹</button>'
    s += '<button id="next" onclick="next()">›</button>'
    s += '</div>'
    # 日にちをサーバーに渡す
    s += '<form method="POST" action="/">'
    s += '<div id="calendar"></div>'
    s += '</div>'

    # 画像表示はこんな感じの記述
    # s += '<img src="/static/japan.png">'

    # 以下、javascriptの記述
    # １文ずつで区切り文字「;」必要
    s += '<script type="text/javaScript">'
    s += 'const week = ["日", "月", "火", "水", "木", "金", "土"];'
    s += 'const today = new Date();'
    # 月末だとずれる可能性があるため、1日固定で取得
    s += 'var showDate = new Date(today.getFullYear(), today.getMonth(), 1);'
    # 初期表示(当日)
    s += 'window.onload = function () {'
    s += 'showProcess(today, calendar);'
    s += '};'
    # 前の月表示
    s += 'function prev(){'
    s += 'showDate.setMonth(showDate.getMonth() - 1);'
    s += 'showProcess(showDate);'
    s += '}'
    # 次の月表示
    s += 'function next(){'
    s += 'showDate.setMonth(showDate.getMonth() + 1);'
    s += 'showProcess(showDate);'
    s += '}'
    # カレンダー表示
    s += 'function showProcess(date) {'
    s += 'var year = date.getFullYear();'
    s += 'var month = date.getMonth();'
    s += 'document.querySelector("#header").innerHTML = year +"年 " + (month + 1) + "月";'
    s += 'var calendar = createProcess(year, month);'
    s += 'document.querySelector("#calendar").innerHTML = calendar;'
    s += '}'
    # 以下、カレンダー作成
    s += 'function createProcess(year, month) {'
    # 曜日
    s += 'var calendar = "<table><tr class=\'dayOfWeek\'>";'
    s += 'for (var i = 0; i < week.length; i++) {'
    s += 'calendar += "<th>" + week[i] + "</th>";'
    s += '}'
    s += 'calendar += "</tr>";'
    s += 'var count = 0;'
    s += 'var startDayOfWeek = new Date(year, month, 1).getDay();'
    s += 'var endDate = new Date(year, month + 1, 0).getDate();'
    s += 'var lastMonthEndDate = new Date(year, month, 0).getDate();'
    s += 'var row = Math.ceil((startDayOfWeek + endDate) / week.length);'
    # 1行ずつ設定
    s += 'for (var i = 0; i < row; i++) {'
    s += 'calendar += "<tr>";'
    # 1colum単位で設定
    s += 'for (var j = 0; j < week.length; j++) {'
    s += 'if (i == 0 && j < startDayOfWeek) {'
    # 1行目で1日まで先月の日付を設定
    s += 'calendar += "<td class=\'disabled\'>" + (lastMonthEndDate - startDayOfWeek + j + 1) + "</td>";'
    s += '} else if (count >= endDate) {'
    # 最終行で最終日以降、翌月の日付を設定
    s += 'count++;'
    s += 'calendar += "<td class=\'disabled\'>" + (count - endDate) + "</td>";'
    s += '} else {'
    # 当月の日付を曜日に照らし合わせて設定
    s += 'count++;'
    # 日付の条件設定
    s += 'if ('
    line_count = 0
    for line in data:
        line_count += 1
        if line_count == 1:
            s += '(year == {}'.format(line[0][0])
            s += '&& month + 1 == {}'.format(line[0][1])
            s += '&& count == {})'.format(line[0][2])
        else:
            s += '||(year == {}'.format(line[0][0])
            s += '&& month + 1 == {}'.format(line[0][1])
            s += '&& count == {})'.format(line[0][2])
    s += '){'
    s += 'var mo = month + 1;'
    s += 'var date = year + "," + mo + "," + count;'
    s += 'calendar += "<td>" + `<button type="submit" name="date" id="today" value=${date}>` + count + "</button></td>";'
    s += '} else {'
    s += 'calendar += "<td class=\'day\'>" + count + "</td>";'
    s += '}'
    s += '}'
    s += '}'
    s += 'calendar += "</tr>";'
    s += '}'
    s += 'return calendar;'
    s += '}'
    s += '</script>'

    s += '</body>'
    s += '</html>'
    return s

@app.route('/', methods = ["POST"])
def index():
    date = request.form['date']
    return date

if __name__ == "__main__":
    app.run()