import io
import os
import requests
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import json

load_dotenv()

# Load environment variables
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Scopes for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_drive_api():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token_file:
            creds = Credentials.from_authorized_user_info(json.load(token_file), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.json', 'w') as token_file:
                token_file.write(creds.to_json())
        else:
            raise Exception("No valid credentials available.")
    service = build('drive', 'v3', credentials=creds)
    return service

def download_file_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def upload_file_to_drive(service, file_io, file_name, mime_type='video/mp4', folder_id='1iXfvao610c3sKNPT0eA0GA53JsXdPFz9'):
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaIoBaseUpload(file_io, mimetype=mime_type, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    
    # Set permissions to "Anyone with the link"
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file.get('id'), body=permission).execute()
    
    # Retrieve the updated file metadata to get the webViewLink
    file = service.files().get(fileId=file.get('id'), fields='webViewLink').execute()
    
    return file.get('webViewLink')

def upload_creatomate_video_to_drive(service, file_io, file_name, mime_type='video/mp4', folder_id='1FTNKyWv21LJSXEF1D8aB98WchQBPgsUC'):
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaIoBaseUpload(file_io, mimetype=mime_type, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Set permissions to "Anyone with the link"
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file.get('id'), body=permission).execute()
    
    return file.get('id')

def retrieve_drive_file_info(service, file_id):
    file_info = service.files().get(fileId=file_id, fields='id, name, webViewLink, thumbnailLink').execute()
    return file_info

# def main():
#     service = authenticate_drive_api()
#     file_url = "https://instagram.fevn6-2.fna.fbcdn.net/o1/v/t16/f2/m69/An_uUGULuWLvZEpKgL1ZaKfKf-Y07S0Ngh-slMiChLoNq_NtZ8qJZJrn8HjxQlqEja07DIQBDWgBXnYZcZKIkMP-.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLmNsaXBzLmMyLjEwODAuYmFzZWxpbmUifQ&_nc_ht=instagram.fevn6-2.fna.fbcdn.net&_nc_cat=109&vs=1178828326453158_33892271&_nc_vs=HBksFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HREhRSHdkOFBkTVZzQTRJQUhzXzFjTTROUUU1YnBSMUFBQUYVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dNekN1aHBTVTdEOEJQMENBTTNiNFdGc29pVnlicV9FQUFBRhUCAsgBACgAGAAbABUAACbK1Lms9LngPxUCKAJDMywXQBqp%2B%2Bdsi0QYFmRhc2hfYmFzZWxpbmVfMTA4MHBfdjERAHX%2BBwA%3D&_nc_rid=9dfd66e9e0&ccb=9-4&oh=00_AYAH4KuM6DfzkzRPWF7sUXOAw9dFkN0oYuVILK2t3gIq4g&oe=667D25E5&_nc_sid=c024bc"
#     file_io = download_file_from_url(file_url)
#     file_name = "testing.mp4"
#     file_id = upload_file_to_drive(service, file_io, file_name)
#     file_info = retrieve_drive_file_info(service, file_id)
#     print(file_info)

# if __name__ == "__main__":
#     main()
