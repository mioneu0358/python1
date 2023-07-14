from flask import Flask, render_template, request, redirect, url_for
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)


# Function to get Google OAuth credentials
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


# Function to load stored credentials
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


# Function to retrieve audio files from Google Drive
# Function to retrieve audio files from Google Drive
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

    # Create an empty dictionary to store the audio files by category
    audio_files = {}

    for file in files:
        # Extract the category from the file name (e.g., "Rain Sound 1.mp3" -> "Rain Sound")
        category = file['name'].split('.')[0]

        # Check if the category already exists in the audio_files dictionary
        if category in audio_files:
            # Append the new audio file to the existing category
            audio_files[category].append({
                'name': file['name'],
                'url': f"https://drive.google.com/uc?export=download&id={file['id']}"
            })
        else:
            # Create a new category with the audio file
            audio_files[category] = [{
                'name': file['name'],
                'url': f"https://drive.google.com/uc?export=download&id={file['id']}"
            }]

    return audio_files



# Function to retrieve the audio file URL from Google Drive
def get_audio_file_url(service, file_id):
    # Implement your logic to retrieve the audio file URL from Google Drive
    # Use the provided service object and file_id to make requests to the Google Drive API
    # Retrieve and return the URL of the audio file

    # Example code:
    response = service.files().get(fileId=file_id, fields='webViewLink').execute()
    file_url = response.get('webViewLink', '')
    return file_url


# Function to load the volume value from a database or file
def load_volume(category):
    # Implement your logic to load the volume value for the specified category
    # Load the volume value from a database or file
    # Return the volume value

    # Example code:
    # You can store the volume values in a database or file, and retrieve the corresponding value here
    pass


# Function to save the volume value to a database or file
def save_volume(category, volume):
    # Implement your logic to save the volume value for the specified category
    # Store the volume value in a database or file

    # Example code:
    # You can store the volume values in a database or file for each category
    pass


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
    audio_files = list(audio_files.values())
    for i in range(len(audio_files)):
        audio_files[i] = audio_files[i][0]
    # Render the audio files template and pass the audio files data
    category = ["Rain Sound", "Insects Sound", "Crackling Fire", "Piano Music", "Ocean Waves", "Wind Sounds"]
    return render_template('audio_files.html',categories =category, audio_files_data=audio_files)


@app.route('/play/<file_id>')
def play_audio(file_id):
    # Load credentials and create a service object
    credentials = load_credentials()  # Load stored credentials here
    service = build('drive', 'v3', credentials=credentials)

    # Retrieve the audio file URL from Google Drive
    file_url = get_audio_file_url(service, file_id)  # Implement the function to retrieve file URL

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
