from flask import Flask, render_template, request
import sqlite3 
import requests
import json
from datetime import datetime

app = Flask(__name__)

# def predict_accidents():
#     conn = sqlite3.connect('ml_db.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT a_lng, a_lat, severity FROM Accidents')
#     coordinates = cursor.fetchall()
#     conn.close()
#     return coordinates

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def index():
    return render_template('home.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html', predicts = None)

@app.route('/statistics')
def statistics_page():
    return render_template('statistics.html')

@app.route('/test')
def test_page():
    return render_template('test.html')

@app.route('/predict', methods=['POST'])
def get_predict():
    if request.method == 'POST':
        lng = request.form['longitude']
        lat = request.form['latitude']
        crossing = convertNum(request.form['crossing'])
        signal = convertNum(request.form['Traffic_Signal'])
        stop = convertNum(request.form['Stop'])
        junction = convertNum(request.form['Junction'])
        sunriseset = convertNum(request.form['Sunrise_Sunset'])
        weather = request.form['Weather']

        isClear, isCloud, isSnowy, israiny = convertWeather(weather)
        

        # data = prediction(user_input)
        print(lng)
        print(lat)
        print(crossing)
        print(signal)
        print(stop)
        print(junction)
        print(sunriseset)
        print(isClear)
        print(isCloud)
        print(isSnowy)
        print(israiny)

        api_key = "76991990d4912e014dec46c9f8e4da4c"

        # 現在地の緯度と経度を取得します。

        # OpenWeatherMap APIにリクエストを送信します。
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}"
        response = requests.get(url)

        # ステータスコードを確認します。
        if response.status_code != 200:
            print("APIリクエストに失敗しました。")
            exit()

        # 応答をJSONとしてデコードします。
        data = json.loads(response.content)

        # 降水量を取得します。
        precipitation = getPrecipitation(data)

        # 他の天気情報を取得します。
        pressure = data["main"]["pressure"]*2.54
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]*3.6

        # 天気を定義します。
        # weather_type = ""
        # if data["weather"][0]["description"] == "clear sky":
        #     weather_type = "晴れ"
        # elif data["weather"][0]["description"] == "snow":
        #     weather_type = "雪"
        # elif data["weather"][0]["description"] == "rain":
        #     weather_type = "雨"

        # 情報を表示します。
        print("現在の天気情報：")
        print("圧力：", pressure, "cmHg")
        print("温度：", temperature, "℃")
        print("湿度：", humidity, "%")
        print("風速：", wind_speed, "m/s")
        print(precipitation)
        # print("天気：", weather_type)

        isWeekend = check_weekday_or_weekend()
        print(isWeekend)
        
        pred = [(lng, lat, 1)]
        return render_template('predict.html', predicts = pred)

def convertNum(input):
    if(input == 'Yes'):
        return 1
    elif(input == 'Sunrise'):
        return 0
    elif(input == 'Sunset'):
        return 1
    else:
        return 0
    
def convertWeather(input, isClear = 0, isCloud = 0, isSnowy = 0, israiny = 0):
    if(input == 'Clear'):
        isClear = 1
        isCloud = 0
        isSnowy = 0
        israiny = 0
    elif(input == 'Cloudy'):
        isClear = 0
        isCloud = 1
        isSnowy = 0
        israiny = 0
    elif(input == 'Snowy'):
        isClear = 0
        isCloud = 0
        isSnowy = 1
        israiny = 0
    else:
        isClear = 0
        isCloud = 0
        isSnowy = 0
        israiny = 1
    return isClear, isCloud, isSnowy, israiny

def check_weekday_or_weekend():
    # 現在の日付を取得
    current_date = datetime.now()

    # 曜日を取得 (0: Monday, 1: Tuesday, ..., 6: Sunday)
    day_of_week = current_date.weekday()

    # 判別
    if day_of_week < 5:  # 0から4は平日
        return 0
    else:  # 5または6は週末
        return 1
def getPrecipitation(data):
    precipitation = data["rain"]["1h"]
    if(precipitation != None):
        return precipitation
    else:
        return 0
   

def prediction(user_input):



    # mlflow code
    return(lng, lat, severity)



    
if __name__ == '__main__':
    app.run(debug=True)
