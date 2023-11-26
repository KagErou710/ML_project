from flask import Flask, render_template
import sqlite3 

# SQLiteデータベースに接続
conn = sqlite3.connect('ml_db.db')
cursor = conn.cursor()
# cursor.execute('CREATE TABLE Accidents(a_id INTEGER PRIMARY KEY, a_lat FLOAT NOT NULL, a_lng FLOAT NOT NULL,severity FLOAT NOT NULL);')
# cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (1, 13.75 , 100.53125, 20);')
# cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (2, 13.76 , 100.54, 30);')
# cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (3, 13.77 , 100.55, 40);')
# cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (4, 13.78 , 100.56, 50);')
# cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (5, 13.79 , 100.57, 60);')
cursor.execute('SELECT a_lng, a_lat FROM Accidents')
coordinates = cursor.fetchall()
conn.close()
for lng, lat in coordinates:
    print(f'Longitude: {lng}, Latitude: {lat}')

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def predict_accidents():
    # SQLiteデータベースに接続
    conn = sqlite3.connect('ml_db.db')
    cursor = conn.cursor()
    # cursor.execute('CREATE TABLE Accidents(a_id INTEGER PRIMARY KEY, a_lat FLOAT NOT NULL, a_lng FLOAT NOT NULL,severity FLOAT NOT NULL);')
    # cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (1, 13.75 , 100.53125, 20);')
    # cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (2, 13.76 , 100.54, 30);')
    # cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (3, 13.77 , 100.55, 40);')
    # cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (4, 13.78 , 100.56, 50);')
    # cursor.execute('INSERT INTO Accidents (a_id, a_lat, a_lng, severity) VALUES (5, 13.79 , 100.57, 60);')
    cursor.execute('SELECT a_lng, a_lat, severity FROM Accidents')
    coordinates = cursor.fetchall()
    conn.close()
    # for lng, lat in coordinates:
    #     print(f'Longitude: {lng}, Latitude: {lat}')

    return coordinates

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def index():
    return render_template('home.html')

@app.route('/predict')
def predict_page():
    data = predict_accidents()
    print(data)
    return render_template('predict.html', predicts = data)

@app.route('/statistics')
def statistics_page():
    return render_template('statistics.html')

@app.route('/test')
def test_page():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)
