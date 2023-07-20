from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)

# Google OAuth 자격증명을 얻기 위한 함수
def get_credentials(google_id, password):
    # Implement your authentication logic here
    # You can use the provided Google ID and password to authenticate the user
    # and retrieve the necessary OAuth credentials

    # Example implementation:
    # 1. Validate the provided Google ID and password
    # 2. If authentication is successful, create an OAuth flow
    # 3. Run the flow to obtain credentials
    # 4. Return the credentials object if successful, otherwise return None

    # Example code:
    if google_id == 'aliuveu' and password == '75fa2vheo!':
        # Set up the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive'])
        credentials = flow.run_local_server(port=0)
        return credentials
    else:
        return None

# 저장된 자격증명을 불러오기 위한 함수
def load_credentials():
    # Implement your logic to load stored credentials
    # Load the stored credentials from a database or file

    # Example code:
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
            return credentials
    else:
        return None
def get_audio_file_url(service, file_id):
    try:
        # Make a request to the Drive API to get the file metadata
        file_metadata = service.files().get(fileId=file_id, fields='webViewLink').execute()
        file_url = file_metadata.get('webViewLink', '')
        return file_url
    except Exception as e:
        # Handle any potential errors that may occur while retrieving the file URL
        print(f"Error retrieving file URL: {e}")
        return None
# Google Drive에서 오디오 파일을 검색하는 함수
def get_audio_files(service):
    # Implement your logic to retrieve audio files from Google Drive
    # Use the provided service object to make requests to the Google Drive API
    # Retrieve and process the audio files data
    # Return a list of audio files

    # Example code:
    results = service.files().list(q="mimeType='audio/mpeg'",
                                   pageSize=10,
                                   fields='files(id, name)').execute()
    files = results.get('files', [])
    print("files",files)
    # Create an empty dictionary to store the audio files by category
    audio_files = []

    for file in files:
        # Extract the category from the file name (e.g., "Rain Sound 1.mp3" -> "Rain Sound")
        category = file['name'].split('.')[0]

        # Check if the category already exists in the audio_files dictionary
        audio_files.append({
            'name': file['name'],
            'url': f"https://drive.google.com/uc?export=download&id={file['id']}"
        })
    return audio_files
# Function to save the volume value to a database or file
def save_volume(category, volume):
    # Implement your logic to save the volume value for the specified category
    # Store the volume value in a database or file

    # Example code (using a dictionary to simulate a database):
    volume_data = {}
    if os.path.exists('volume_data.pickle'):
        with open('volume_data.pickle', 'rb') as data_file:
            volume_data = pickle.load(data_file)

    volume_data[category] = volume

    with open('volume_data.pickle', 'wb') as data_file:
        pickle.dump(volume_data, data_file)

# Function to load the volume value from a database or file
def load_volume(category):
    # Implement your logic to load the volume value for the specified category
    # Load the volume value from a database or file
    # Return the volume value

    # Example code (using a dictionary to simulate a database):
    volume_data = {}
    if os.path.exists('volume_data.pickle'):
        with open('volume_data.pickle', 'rb') as data_file:
            volume_data = pickle.load(data_file)

    return volume_data.get(category, '50')  # Return the default volume value '50' if not found in the database





@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def authenticate():
    # Get Google ID and password from the form
    google_id = request.form['google_id']
    password = request.form['password']

    # Authenticate user and store credentials
    credentials = get_credentials(google_id, password)

    if credentials:
        # Save credentials and redirect to the audio files page
        # (You can store the credentials in a database or file for later use)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
        return redirect(url_for('audio_files'))
    else:
        # Invalid credentials, redirect back to the login page with an error message
        return redirect(url_for('login'))


@app.route('/audio_files')
def audio_files():
    # Load credentials and create a service object
    credentials = load_credentials()  # Load stored credentials here
    service = build('drive', 'v3', credentials=credentials)

    # Retrieve audio files from Google Drive
    audio_files = get_audio_files(service)  # Implement the function to retrieve audio files
    # Render the audio files template and pass the audio files data
    category = ["Rain Sound", "Insects Sound", "Crackling Fire", "Piano Music", "Ocean Waves", "Wind Sounds"]
    print(category,audio_files)

    return render_template('audio_files.html',categories =category, audio_files_data=audio_files)

@app.route('/play/<file_id>')
def play_audio(file_id):
    # Load credentials and create a service object
    credentials = load_credentials()  # Load stored credentials here
    service = build('drive', 'v3', credentials=credentials)

    # Retrieve the audio file URL from Google Drive using the get_audio_file_url function
    file_url = get_audio_file_url(service, file_id)

    # Load the volume value from a database or file (if available)
    volume = load_volume(file_id)  # Implement the function to load volume value

    # Render the audio player template and pass the file URL and volume value
    return render_template('audio_player.html', file_url=file_url, volume=volume)

@app.route('/set_volume', methods=['POST'])
def set_volume():
    category = request.form['category']
    volume = request.form['volume']

    # Save the volume value for the specified category
    save_volume(category, volume)

    return redirect(url_for('audio_files'))
@app.route('/get_volume', methods=['POST'])
def get_volume():
    category = request.form['category_load']

    # Load the volume value for the specified category
    volume = load_volume(category)

    # Redirect to the audio player page and pass the loaded volume value as a parameter
    return redirect(url_for('play_audio', file_id='', volume=volume))


if __name__ == '__main__':
    app.run(debug=True)
