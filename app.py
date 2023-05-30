from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS #다른 출처끼리의 자원 공유
import cv2
import os
import numpy as np
import subprocess
import gptcrawling as gc
import convertimage as cv

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output', methods=['GET'])
def send_image():
    image_path = 'convertimage/convert.jpg'
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/convertimage',methods=['POST'])
def cv_image_save():
    cv.convert_image()


@app.route('/gpt_recommend', methods=['POST'])
def execute_gpt_crawling():
    data = request.get_json()
    gender = data['gender']
    temperature = data['temperature']
    weather = data['weather']
    
    recommendations = gc.perform_crawling(gender, temperature, weather)

    return jsonify(recommendations)
    
@app.route('/process_image', methods=['POST'])
def process_image():
    if request.method == 'POST':
        # 이미지 파일 받기
        image = request.files['image']

        # 이미지를 OpenCV로 처리
        image_data = image.read()
        nparr = np.frombuffer(image_data, np.uint8)
        cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 처리된 결과 이미지를 저장
        save_path = './clothesimage'  # 저장할 디렉토리 경로
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        filename = 'postimage.jpg'  # 저장할 파일 이름
        file_path = os.path.join(save_path, filename)
        cv2.imwrite(file_path, cv_image)

        # 처리된 결과 이미지의 파일 경로를 반환
        return file_path
    else:
        return 'Method Not Allowed', 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
