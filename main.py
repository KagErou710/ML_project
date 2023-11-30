from flask import Flask, render_template, request
import sqlite3 
import requests
import json
from datetime import datetime
import pickle
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html', predicts = None, data = None)

@app.route('/statistics')
def statistics_page():
    return render_template('statistics.html')

@app.route('/predict', methods=['POST'])
def get_predict():
    if request.method == 'POST':
        lng = request.form['longitude']
        lat = request.form['latitude']
        crossing = convertNum(request.form['crossing'])
        signal = convertNum(request.form['Traffic_Signal'])
        stop = convertNum(request.form['Stop'])
        junction = convertNum(request.form['Junction'])
        sunriseset = get_sunrise_sunset_status()
        Twilight = is_twilight()
        weather = request.form['Weather']
        visibility = request.form['visibility']
        isClear, isCloud, isSnowy, israiny = convertWeather(weather)

        api_key = "76991990d4912e014dec46c9f8e4da4c"

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}"
        response = requests.get(url)


        if response.status_code != 200:
            print("API request fail")
        
            data = json.loads(response.content)

            precipitation = getPrecipitation(data)
            pressure = data["main"]["pressure"]*2.54
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]*3.6

        else:
            precipitation = 100

            pressure = 40
            temperature = 15
            humidity = 75
            wind_speed = 14.4

        StartDec = is_december()
        StartJan = is_jan()
        StartH = get_hh() 

        isWeekend = check_weekday_or_weekend()
        pred = prediction(lng, lat, crossing, pressure, signal, temperature, StartDec, StartH, stop, humidity, StartJan, junction, isClear, wind_speed, visibility, Twilight, isCloud, sunriseset, isWeekend, precipitation, isSnowy, israiny)
        past_data = [(lng, lat, request.form['crossing'], pressure, request.form['Traffic_Signal'], temperature,request.form['Stop'], humidity, request.form['Junction'], wind_speed, request.form['visibility'], reverseNum(Twilight), reverseNum(sunriseset), precipitation, request.form['Weather'])]
        return render_template('predict.html', predicts = pred, data = past_data)

def convertNum(input):
    if(input == 'Yes'):
        return 1
    elif(input == 'Sunrise'):
        return 0
    elif(input == 'Sunset'):
        return 1
    else:
        return 0
    
def reverseNum(input):
    if(input == 1):
        return 'Yes'
    else:
        return 'No'
    
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
    current_date = datetime.now()
    day_of_week = current_date.weekday()

    if day_of_week < 5:
        return 0
    else:
        return 1
    
def getPrecipitation(data):
    try:
        precipitation = data["rain"]["1h"]
        if(precipitation != None):
            return precipitation
        else:
            return 0
    except:
        return 0


def is_december():
    current_month = datetime.now().month
    if(current_month == 12):
        output = 1
    else:
        output = 0
    return output 


def is_jan():
    current_month = datetime.now().month
    
    if(current_month == 1):
        output = 1
    else:
        output = 0
    return output


def get_hh():
    current_time = datetime.now().time()
    current_hour = current_time.hour
    return current_hour

def is_twilight():
    current_time = datetime.now().time()
    sunrise_time = datetime.strptime("17:00", "%H:%M").time()
    sunset_time = datetime.strptime("18:00", "%H:%M").time()
    if sunrise_time <= current_time < sunset_time:
        return 1
    else:
        return 0


def get_sunrise_sunset_status():
    current_time = datetime.now().time()
    sunrise_time = datetime.strptime("06:00", "%H:%M").time()
    sunset_time = datetime.strptime("18:00", "%H:%M").time()
    if sunrise_time <= current_time < sunset_time:
        return 1
    else:
        return 0


def prediction(Start_Lng, Start_Lat, Crossing, Pressure, Traffic_Signal, Temperature, Start_Month_December, Start_Hour, Stop, Humidity, Start_Month_January, Junction, Weather_Bin_Clear, Wind_Speed, Visibility, Civil_Twilight, Weather_Bin_Cloudy, Sunrise_Sunset, IsWeekend, Precipitation, Weather_Bin_Snowy, Weather_Bin_Rainy):
    with open('model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    input = pd.DataFrame({
        'Start_Lat': [Start_Lat],
        'Start_Lng': [Start_Lng],
        'Humidity(%)': [Humidity],
        'Crossing': [Crossing],
        'Junction': [Junction],
        'Stop': [Stop],
        'Traffic_Signal': [Traffic_Signal],
        'Sunrise_Sunset': [Sunrise_Sunset],
        'Civil_Twilight': [Civil_Twilight],
        'Start_Hour': [Start_Hour],
        'IsWeekend': [IsWeekend],
        'Temperature(C)': [Temperature],
        'Pressure(cm)': [Pressure],
        'Precipitation(cm)': [Precipitation],
        'Visibility(km)': [Visibility],
        'Wind_Speed(kmph)': [Wind_Speed],
        'Weather_Bin_Clear': [Weather_Bin_Clear],
        'Weather_Bin_Cloudy': [Weather_Bin_Cloudy],
        'Weather_Bin_Snowy': [Weather_Bin_Snowy],
        'Weather_Bin_Rainy': [Weather_Bin_Rainy],
        'Start_Month_December': [Start_Month_December],
        'Start_Month_January': [Start_Month_January]        
    })


    prediction = loaded_model.predict(input)
    print("output : ", prediction)
    print("data type : ", type(prediction))
    temp_list = prediction.tolist()
    severity = temp_list[0]
    prediction = [(Start_Lng, Start_Lat, severity)]


#     conn = sqlite3.connect('ml_db.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#     INSERT INTO AccidentData (Start_Lng, Start_Lat, Crossing, Pressure, Traffic_Signal, Temperature, Start_Month_December, Start_Hour, Stop, Humidity, Start_Month_January, Junction, Weather_Bin_Clear, Wind_Speed, Visibility, Civil_Twilight, Weather_Bin_Cloudy, Sunrise_Sunset, IsWeekend, Precipitation, Weather_Bin_Snowy, Weather_Bin_Rainy, Severity)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# ''', (Start_Lng, Start_Lat, Crossing, Pressure, Traffic_Signal, Temperature, Start_Month_December, Start_Hour, Stop, Humidity, Start_Month_January, Junction, Weather_Bin_Clear, Wind_Speed, Visibility, Civil_Twilight, Weather_Bin_Cloudy, Sunrise_Sunset, IsWeekend, Precipitation, Weather_Bin_Snowy, Weather_Bin_Rainy, severity))
    
#     conn.commit()
#     conn.close()



    return prediction


if __name__ == '__main__':
    app.run(debug=True, port=8080)
