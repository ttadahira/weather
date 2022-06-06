# 「new_weather_data.csv」の作成に使ったプログラム
import re

# 天気の簡略化
weather = {'快晴':'晴れ','晴':'晴れ','曇':'曇り','薄曇':'曇り','霧雨':'雨','雨':'雨','霧':'小雨' \
           ,'大雨':'大雨','暴風雨':'大雨','みぞれ':'みぞれ','雪':'雪','あられ':'雪','大雪':'大雪' \
           ,'暴風雪':'大雪','ふぶき':'大雪','ひょう':'大雪','雷':'雷','大風':'風','地ふぶき':'風'}
# 天気概況リスト
tenki_list = ['快晴','晴','曇','薄雲','霧雨','雨','霧','大雨','暴風雨','みぞれ','雪','あられ' \
              ,'大雪','暴風雪','ふぶき','ひょう','雷','大風','地ふぶき']

data = []
with open('data/weather_data.csv', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.replace('\n', '')
        line = line.split(',')
        # 天気概況が「×」でないならデータ追加
        if line[3] != '×' and line[3] != '':
            # 日付、天気、最高気温、最低気温、地域のデータ
            data.append(line)

for line in data:
     # 簡略化を適応
    for key in weather:
        # 「時々」、「後」パターン
        for tenki in tenki_list:
            tokidoki = '^{0}時々{1}'.format(key, tenki)
            nochi = '^{0}後{1}'.format(key, tenki)
            if re.compile(tokidoki).search(line[3]):
                line[3] = weather[key] + 'ときどき' + weather[tenki]
            elif re.compile(nochi).search(line[3]):
                line[3] = weather[key] + 'のち' + weather[tenki]
        # それ以外のパターン
        match = re.search(r'ときどき|のち', line[3])
        if match == None:
            pattern = '^{}'.format(key)
            if re.compile(pattern).search(line[3]):
                line[3] = weather[key]
            
with open('data/new_weather_data.csv', 'w', encoding='utf-8') as f:
    for line in data:
        line = ','.join(line)
        f.write(line + '\n')