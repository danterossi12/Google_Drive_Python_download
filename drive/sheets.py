# Download Google Drive API     *example of authorization designed for command-line application*

from __future__ import print_function
import io
from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Drive v3 API - (***need to create api credentials (OAuth 2.0 client IDs) for web application next***)
# Authorization flow
SCOPES = 'https://www.googleapis.com/auth/drive'  # full access!
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))


# Call Drive v3 API
results = service.files().list(
    pageSize=10, fields="*").execute()
items = results.get('files', [])  # returns google drive file info

if not items:
    print('No files found.')
else:
        request = service.files().export_media(fileId=items[0]['id'],  # request to download using file ID
                                               mimeType='text/csv')
        fh = io.FileIO(items[0]['name'], 'wb')  # write to file
        downloader = MediaIoBaseDownload(fh, request)  # download
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
print('finished downloading')

#  For multiple downloads
'''
 for x in range(len(items)):
        request = service.files().export_media(fileId=items[x]['id'],
                                               mimeType='text/csv')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            try: status, done = downloader.next_chunk()
            except: 'googleapiclient.errors.HttpError'
            print("Download %d%%." % int(status.progress() * 100))
print('finished downloading')
'''