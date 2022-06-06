const week = ['日', '月', '火', '水', '木', '金', '土']
const week_ruby = ['にち', 'げつ', 'か', 'すい', 'もく', 'きん', 'ど']
// 天気と画像データを結びつける
const icon = {'晴れ':'hare.png', '曇り':'kumori.png', '小雨':'kosame.png', '雨':'ame.png', '大雨':'ooame.png', 'みぞれ':'mizore.png', '雪':'yuki.png', '大雪':'ooyuki.png', '雷':'kaminari.png', '風':'kaze.png'}
// ユーザが選択した日付を基本の日付にする
var chosen_date = document.getElementById('date').textContent;
const chosen_element = chosen_date.split('/')
const chosen_day = new Date(chosen_element[0], chosen_element[1] - 1, chosen_element[2]);
// 渡された気象データを二次配列にする
var data_str = document.getElementById('data').textContent;
var data_list = data_str.split('\n')
for (var i = 0; i < data_list.length; i++) {
    data_list[i] = data_list[i].split(',');
}
// 一番新しい日付の取得
for (var i = 0; i < data_list.length; i++) {
    var newdate_element = data_list[i][0].split('/');
    if (i === 0) {
        var newdate = new Date(newdate_element[0], newdate_element[1] - 1, newdate_element[2]);
        var latest = data_list[i][0]
    } else {
        if (newdate < new Date(newdate_element[0], newdate_element[1] - 1, newdate_element[2])) {
            var newdate = new Date(newdate_element[0], newdate_element[1] - 1, newdate_element[2]); 
            var latest = data_list[i][0]
        }
    }
}
// 一番古い日付の取得
for (var i = 0; i < data_list.length; i++) {
    var olddate_element = data_list[i][0].split('/');
    if (i === 0) {
        var olddate = new Date(olddate_element[0], olddate_element[1] - 1, olddate_element[2]);
        var oldest = data_list[i][0]
    } else {
        if (olddate > new Date(olddate_element[0], olddate_element[1] - 1, olddate_element[2])) {
            var olddate = new Date(olddate_element[0], olddate_element[1] - 1, olddate_element[2]); 
            var oldest = data_list[i][0]
        }
    }
}
// 月末だとずれる可能性があるため、1日固定で取得
if (chosen_date === 'False') {
    var showDate = new Date(newdate.getFullYear(), newdate.getMonth(), 1);
} else {
    var showDate = new Date(chosen_day.getFullYear(), chosen_day.getMonth(), 1);
}

// 初期表示
if (chosen_date === 'False') {
    window.onload = function () {
        showProcess(newdate, calendar);
    };
} else {
    window.onload = function () {
        showProcess(chosen_day, calendar);
    };
}

// 正規表現
function re_tenki(data, icon){
    for (var i = 0; i < data.length; i++) {
        for (var key in icon) {
            var pattern = `^${key}`
            if (data[i][1].search(pattern) >= 0) {
                data_list[i].push(icon[key]);
            }
        }
    }
}

// 前の月表示
function prev(){
    showDate.setMonth(showDate.getMonth() - 1);
    showProcess(showDate);
}

// 次の月表示
function next(){
    showDate.setMonth(showDate.getMonth() + 1);
    showProcess(showDate);
}

// カレンダー表示
function showProcess(date) {
    var year = date.getFullYear();
    var month = date.getMonth();
    document.querySelector('#calendar-header').innerHTML = year + '<ruby>年<rt>ねん</rt></ruby> ' + (month + 1) + '<ruby>月<rt>がつ</rt></ruby>';

    var calendar = createProcess(year, month);
    document.querySelector('#calendar').innerHTML = calendar;
}

// カレンダー作成
function createProcess(year, month) {
    // 曜日
    var calendar = '<table><tr class="dayOfWeek">';
    for (var i = 0; i < week.length; i++) {
        calendar += '<th><ruby>' + week[i] + '<rt>' + week_ruby[i] + '</rt></ruby></th>';
    }
    calendar += '</tr>';

    var count = 0;
    var startDayOfWeek = new Date(year, month, 1).getDay();
    var endDate = new Date(year, month + 1, 0).getDate();
    var lastMonthEndDate = new Date(year, month, 0).getDate();
    var row = Math.ceil((startDayOfWeek + endDate) / week.length);

    // 1行ずつ設定
    for (var i = 0; i < row; i++) {
        calendar += '<tr>';
        // 1colum単位で設定
        for (var j = 0; j < week.length; j++) {
            if (i == 0 && j < startDayOfWeek) {
                // 1行目で1日まで先月の日付を設定
                calendar += '<td id="tenki" class="disabled">' + (lastMonthEndDate - startDayOfWeek + j + 1) + '</td>';
            } else if (count >= endDate) {
                // 最終行で最終日以降、翌月の日付を設定
                count++;
                calendar += '<td id="tenki" class="disabled">' + (count - endDate) + '</td>';
            } else {
                // 当月の日付を曜日に照らし合わせて設定
                count++;
                var mo = month + 1
                var date = year + "/" + mo + "/" + count;
                re_tenki(data_list, icon);
                var match = data_list.filter(e => e[0] === date);
                if (match.length !== 0
                ){
                    if (date === chosen_date){
                        calendar += '<td id="tenki">' + `<button type="submit" name="date" id="chosen" value=${date}>` + count + `<br><img src="/static/tenki/${match[0][5]}" height="60px" width="60px" />` + '</button>';
                        calendar += `<div class="mouseover">${date}<br>${match[0][1]}</div></td>`;
                    } else if (date === latest) {
                        calendar += '<td id="tenki">' + `<button type="submit" name="date" id="latest2" value=${date}>` + count + `<br><img src="/static/tenki/${match[0][5]}" height="60px" width="60px" />` + '</button>';
                        calendar += `<div class="mouseover">${date}<br>${match[0][1]}</div></td>`;
                    } else if (date === oldest) {
                        calendar += '<td id="tenki">' + `<button type="submit" name="date" id="oldest2" value=${date}>` + count + `<br><img src="/static/tenki/${match[0][5]}" height="60px" width="60px" />` + '</button>';
                        calendar += `<div class="mouseover">${date}<br>${match[0][1]}</div></td>`;
                    } else {
                        calendar += '<td id="tenki">' + `<button type="submit" name="date" id="icon" value=${date} ontouchstart="">` + count + `<br><img src="/static/tenki/${match[0][5]}" height="60px" width="60px" />` + '</button>';
                        calendar += `<div class="mouseover">${date}<br>${match[0][1]}</div></td>`;
                    }
                } else {
                    calendar += '<td id="tenki" class="day">' + count + '</td>';
                }
            }
        }
        calendar += '</tr>';
    }
    return calendar;
}