import os
from flask import request

def convert_image():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # 파일 저장 경로
    save_directory = 'convertimage'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    file.save(os.path.join(save_directory, 'convert.jpg'))

    return 'Image uploaded successfully'