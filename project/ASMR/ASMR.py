from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow  # pip install google-auth-oauthlib
from googleapiclient.discovery import build  # pip install google-api-python-client
from google.auth.transport.requests import Request  # pip install google-auth

app = Flask(__name__)

VOLUME_FILE_PATH = "volume.txt"  # 볼륨값을 저장할 파일 이름

# Initial data for the categories
categories = {
    "Rain Sound": 1,
    "Insects Sound": 1,
    "Crackling Fire": 1,
    "Piano Music": 1,
    "Ocean Waves": 1,
    "Wind Sounds": 1,
}


# Google OAuth 자격증명을 얻기 위한 함수: 사용자가 확인 및 어플의 정보 사용범위 설정 및 권한부
def get_credentials(google_id, password):
    # 과정
    # 1. 제공된 구글 아이디와 비밀번호 확인
    # 2. 인증에 성공하면 OAuth 흐름 생성
    # 3. 흐름을 실행하여 자격 증명을 얻습니다.
    # 4. 성공하면 자격 증명 개체를 반환하고 그렇지 않으면 None을 반환합니다.

    if google_id == 'aliuveu' and password == '75fa2vheo!':
        # Set up the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive'])
        credentials = flow.run_local_server(port=0)
        return credentials
    else:
        return None


# 저장된 자격증명을 불러오기 위한 함수
def load_credentials():
    # 현재 경로에 token.pickle이 존재하면 불러와서 return
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
            return credentials
    else:
        return None


def get_audio_file_url(service, file_id):
    try:
        # file metadata(file의 속성정보)를 불러오기 위해 요청을 보낸다
        file_metadata = service.files().get(fileId=file_id, fields='webViewLink').execute()
        file_url = file_metadata.get('webViewLink', '')
        return file_url
    except Exception as e:
        print(f"Error retrieving file URL: {e}")
        return None


# Google Drive에서 오디오 파일을 검색하는 함수
def get_audio_files(service):
    # 요청
    results = service.files().list(q="mimeType='audio/mpeg'",
                                   pageSize=10,
                                   fields='files(id, name)').execute()
    files = results.get('files', [])
    audio_files = []  # 요청한 오디오 파일들의 이름과 경로를 담을 변수

    for file in files:
        # Rain Sound.mp3" -> "Rain Sound"
        category = file['name'].split('.')[0]
        audio_files.append({
            'name': file['name'],
            'url': f"https://drive.google.com/uc?export=download&id={file['id']}"
        })
    return audio_files  # [{'name': "Rain Sound",'url': "https://drive.google.com/uc?export=download&id=파일id}, ...]


audio_files = []


def update_volume_file():
    # w모드는 새로 쓰기를 의미
    with open(VOLUME_FILE_PATH, "w") as f:
        for key, value in categories.items():
            f.write(f"{key}:{value}\n")


def load_volume_file():
    # volume.txt가 존재하면 해당 파일 읽어 오기기
    if os.path.exists(VOLUME_FILE_PATH):
        with open(VOLUME_FILE_PATH, "r") as f:
            for line in f:
                key, value = line.strip().split(":")
                categories[key] = float(value)

# 로그인 메인 페이지
@app.route('/')
def login():
    return render_template('login.html')

# 로그인 버튼 클릭시 실행 할 내용
@app.route('/login', methods=['POST'])
def authenticate():
    # log_in 창 에서 입력한 아이디와 비밀번호를 통해 credential을 가져오고
    google_id = request.form['google_id']
    password = request.form['password']

    # 인증 및 자격증명 저장
    credentials = get_credentials(google_id, password)

    if credentials:
        # 오디오 파일 페이지로 리디렉션 + token 저장
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
        return redirect(url_for('faudio_files'))
    else:
        return redirect(url_for('login'))


@app.route('/audio_files')
def faudio_files():
    credentials = load_credentials()
    service = build('drive', 'v3', credentials=credentials)

    # 오디오 파일 검색 및 audio_files에 저장
    audio_files = get_audio_files(service)
    category = ["Rain Sound", "Insects Sound", "Crackling Fire", "Piano Music", "Ocean Waves", "Wind Sounds"]
    print('fdsa', category, audio_files)
    # 저장된 오디오 파일과 카테고리 를 렌더링과 동시에 전달
    return render_template('audio_files.html', categories=categories, audio_files_data=audio_files)

# 해당 카테고리의 볼륨값을 불러와서 volume.txt에 저장
@app.route('/set_volume', methods=['POST'])
def set_volume():
    if request.method == "POST":
        req = eval(request.data.decode('utf-8'))
        key = req["category"]
        val = req["volume"]
        categories[key] = val
        update_volume_file()
    return render_template('audio_files.html', categories=categories, audio_files_data=audio_files)

# 불러온 볼륨값들을 카테고리별로 저장 후 보내기
@app.route('/get-data')
def load_volume():
    Volumes = {}
    if os.path.exists(VOLUME_FILE_PATH):
        with open(VOLUME_FILE_PATH, "r") as f:
            for line in f:
                key, value = line.strip().split(":")
                Volumes[key] = float(value)
    return jsonify(Volumes)



if __name__ == '__main__':
    app.run(debug=True)
