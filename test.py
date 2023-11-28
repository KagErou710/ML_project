# import geopy
import requests
import json

# # 位置情報の取得
# location = geopy.geocoders.Nominatim().geocode("現在の場所")

# # 緯度と経度を取得
# latitude = location.latitude
# longitude = location.longitude

# # 表示
# print("緯度：", latitude)
# print("経度：", longitude)



# OpenWeatherMap APIキーを設定します。
api_key = ""

# 現在地の緯度と経度を取得します。
latitude = 35.689487
longitude = 139.760883

# OpenWeatherMap APIにリクエストを送信します。
url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
response = requests.get(url)

# ステータスコードを確認します。
if response.status_code != 200:
    print("APIリクエストに失敗しました。")
    exit()

# 応答をJSONとしてデコードします。
data = json.loads(response.content)

# 降水量を取得します。
try:
    precipitation = data["rain"]["1h"]
    print("降水量：", precipitation, "mm")
except KeyError:
    print("降水量データはありません。")

# 他の天気情報を取得します。
pressure = data["main"]["pressure"]
temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]

# 天気を定義します。
weather_type = ""
if data["weather"][0]["description"] == "clear sky":
    weather_type = "晴れ"
elif data["weather"][0]["description"] == "snow":
    weather_type = "雪"
elif data["weather"][0]["description"] == "rain":
    weather_type = "雨"

# 情報を表示します。
print("現在の天気情報：")
print("圧力：", pressure, "cmHg")
print("温度：", temperature, "℃")
print("湿度：", humidity, "%")
print("風速：", wind_speed, "m/s")
print("天気：", weather_type)
# --------------------------------------------------------------------------------------
from datetime import datetime

def check_weekday_or_weekend():
    # 現在の日付を取得
    current_date = datetime.now()

    # 曜日を取得 (0: Monday, 1: Tuesday, ..., 6: Sunday)
    day_of_week = current_date.weekday()

    # 判別
    if day_of_week < 5:  # 0から4は平日
        return "Weekday"
    else:  # 5または6は週末
        return "Weekend"

# 実行して結果を表示
result = check_weekday_or_weekend()