from flask import Flask, render_template
# import sqlite3 

app = Flask(__name__)


# # SQLiteデータベースに接続
# conn = sqlite3.connect('your_database.db')
# cursor = conn.cursor()


# # データベースから座標を取得するエンドポイント
# @app.route('/get_coordinates', methods=['GET'])
# def get_coordinates():
#     conn = sqlite3.connect('your_database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT lng, lat FROM coordinates')
#     coordinates = cursor.fetchall()
#     conn.close()
#     return jsonify({'coordinates': coordinates})

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def index():
    return render_template('home.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html')

@app.route('/statistics')
def statistics_page():
    return render_template('statistics.html')

@app.route('/test')
def test_page():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)
