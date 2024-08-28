import io
import os
import requests
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json

from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET
)

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