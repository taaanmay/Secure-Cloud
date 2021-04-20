# pylint: disable=unused-variable
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
        print('\n\nFiles on Google Drive: \n')
        count = 1
        for item in items:
            print(u'({0}){1}'.format(count,item['name']))
            count = count + 1
    
    print("\n")

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


# Function to Upload file to Google Drive
def upload_file(filename, path):
   
    mimetype = file_type(filename)
    
    file_metadata = {'name': filename}
    media = MediaFileUpload(path, mimetype=mimetype)
    
    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    
    print("File Uploaded on Google Drive")

# Function to get the file extenstion
def file_type(filename):

    mime_types = dict(
        txt='text/plain',
        htm='text/html',
        html='text/html',
        php='text/html',
        css='text/css',
        js='application/javascript',
        json='application/json',
        xml='application/xml',
        swf='application/x-shockwave-flash',
        flv='video/x-flv',

        # images
        png='image/png',
        jpe='image/jpeg',
        jpeg='image/jpeg',
        jpg='image/jpeg',
        gif='image/gif',
        bmp='image/bmp',
        ico='image/vnd.microsoft.icon',
        tiff='image/tiff',
        tif='image/tiff',
        svg='image/svg+xml',
        svgz='image/svg+xml',

        # archives
        zip='application/zip',
        rar='application/x-rar-compressed',
        exe='application/x-msdownload',
        msi='application/x-msdownload',
        cab='application/vnd.ms-cab-compressed',

        # audio/video
        mp3='audio/mpeg',
        ogg='audio/ogg',
        qt='video/quicktime',
        mov='video/quicktime',

        # adobe
        pdf='application/pdf',
        psd='image/vnd.adobe.photoshop',
        ai='application/postscript',
        eps='application/postscript',
        ps='application/postscript',

        # ms office
        doc='application/msword',
        rtf='application/rtf',
        xls='application/vnd.ms-excel',
        ppt='application/vnd.ms-powerpoint',

        # open office
        odt='application/vnd.oasis.opendocument.text',
        ods='application/vnd.oasis.opendocument.spreadsheet',
    )

    file_extenstion = os.path.splitext(filename)[1][1:].lower()
    if file_extenstion in mime_types:
        return mime_types[file_extenstion]
    else:
        return 'application/octet-stream'

