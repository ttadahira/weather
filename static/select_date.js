const week = ['日', '月', '火', '水', '木', '金', '土']
const week_ruby = ['にち', 'げつ', 'か', 'すい', 'もく', 'きん', 'ど']
// htmlに渡された日付データを引用
var str = document.getElementById('date').textContent;
const date_list = str.split(',')
// 一番新しい日付の取得
for (var i = 0; i < date_list.length; i++) {
    var newdate_element = date_list[i].split('/');
    if (i === 0) {
        var newdate = new Date(newdate_element[0], newdate_element[1] - 1, newdate_element[2]);
        var latest = date_list[i]
    } else {
        if (newdate < new Date(newdate_element[0], newdate_element[1] - 1, newdate_element[2])) {
            var newdate = new Date(newdate_element[0], newdate_element[1] - 1, newdate_element[2]); 
            var latest = date_list[i]
        }
    }
}
// 一番古い日付の取得
for (var i = 0; i < date_list.length; i++) {
    var olddate_element = date_list[i].split('/');
    if (i === 0) {
        var olddate = new Date(olddate_element[0], olddate_element[1] - 1, olddate_element[2]);
        var oldest = date_list[i]
    } else {
        if (olddate > new Date(olddate_element[0], olddate_element[1] - 1, olddate_element[2])) {
            var olddate = new Date(olddate_element[0], olddate_element[1] - 1, olddate_element[2]); 
            var oldest = date_list[i]
        }
    }
}
// 月末だとずれる可能性があるため、1日固定で取得
var showDate = new Date(newdate.getFullYear(), newdate.getMonth(), 1);

// 初期表示
window.onload = function () {
    showProcess(newdate, calendar);
};
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
                calendar += '<td class="disabled">' + (lastMonthEndDate - startDayOfWeek + j + 1) + '</td>';
            } else if (count >= endDate) {
                // 最終行で最終日以降、翌月の日付を設定
                count++;
                calendar += '<td class="disabled">' + (count - endDate) + '</td>';
            } else {
                // 当月の日付を曜日に照らし合わせて設定
                count++;
                var mo = month + 1
                var date = year + "/" + mo + "/" + count;
                if (date_list.indexOf(date) > -1) { 
                    if (date === latest) {
                        calendar += '<td>' + `<button type="submit" name="date" id="latest1" value=${date}>` + count + '</button></td>';
                    } else if (date === oldest) {
                        calendar += '<td>' + `<button type="submit" name="date" id="oldest1" value=${date}>` + count + '</button></td>';
                    } else {
                        calendar += '<td>' + `<button type="submit" name="date" id="selectable" value=${date}>` + count + '</button></td>';
                    }
                } else {
                    calendar += '<td class="day">' + count + '</td>';
                }
            }
        }
        calendar += '</tr>';
    }
    return calendar;
}