import os
import io
import sys
import httplib2

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import auth


APPLICATION_NAME = 'Drive Encryption'

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = "/Users/tanmaykaushik/Desktop/TK-Cloud-Secure/client_secret.json"

authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)

# Function to list 10 files present in the Google Drive
def list_files() :
    
    # Call the Drive v3 API
    # pylint: disable=maybe-no-member
    results = service.files().list(
        pageSize= 10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', []) 

    if not items:
        print('No files found.')
    else:
        print('\n\nFiles on Google Drive:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

# Function that returns the file_ID of the required file
def get_file_id(request):
    file_ID = -1
    
    # pylint: disable=maybe-no-member
    results = service.files().list(
    pageSize = 1, fields="nextPageToken, files(id, name, kind, mimeType)",q=request).execute()
    items = results.get('files', [])
    
    # Check if File Found
        # If yes, return file_ID else -1
    if not items:
    	file_ID = -1
    else:
    	for item in items:
    		file_ID = item['id']
    return file_ID

# Function to download file from the Google Drive
def download_file(file_ID, filename) :
    
    # pylint: disable=maybe-no-member
    request = service.files().get_media(fileId=file_ID)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # Store the File in the Downloads Folder
    with io.open("Downloads/" + filename,'wb') as f:
        fh.seek(0)
        f.write(fh.read())


