import os
import pickle
from pprint import pprint
import google.oauth2.credentials
 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

CLIENT_SECRETS_FILE = 'client_secret_ubuntu.json' # 各自のclient_secret.jsonファイルへのパスを設定
USER_CREDENTIALS_FILE = os.environ['USERNAME'] + '.credentials' #ユーザ毎の認証データ保存
SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
 
'''
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
'''

def list_drive_files(service, **kwargs):
  results = service.files().list(**kwargs).execute()
  pprint.pprint(results)
 
def get_authenticated_service():
    credentials = None
    if os.path.exists(USER_CREDENTIALS_FILE):  #保存したファイルがある場合はロード
        try:
            with open(USER_CREDENTIALS_FILE, 'rb') as fi:
                credentials = pickle.load(fi)
 
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())  # 期限の更新を試みる
        except EOFError as e:
            pass
 
    if credentials is None or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
 
    with open(USER_CREDENTIALS_FILE, 'wb') as fo:  # 認証情報をファイルに保存
        pickle.dump(credentials, fo)
 
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_drive_files(service, **kwargs):
    results = service.files().list(**kwargs).execute()
    return results
 
# すべてのファイルの一覧を取得 (1ページ分)

def get_drive_folder_id(service, folder_path):
    """指定パスフォルダのfileIdを取得"""
    parent_id = 'root'
    for name in folder_path:
        res = list_drive_files(service,
                               q=f"'{parent_id}' in parents and "
                               "mimeType = 'application/vnd.google-apps.folder' and "
                               f"name = '{name}'")
        if 'files' not in res or len(res['files']) < 1:
            return None
        parent_id = res['files'][0]['id']
 
    return parent_id    
 
def get_drive_file(service, **kwargs):
    results = service.files().get(**kwargs).execute()
    return results
 
def get_drive_file_info(service, path):
    """指定パスのファイル情報を取得"""
    parent_id = 'root'
    path_depth = len(path)
    info = None
    for depth, name in enumerate(path):
        if depth < (path_depth - 1):
            mimeType = "mimeType = 'application/vnd.google-apps.folder' and "
        else:
            mimeType = ""
        res = list_drive_files(service,
                               q=f"'{parent_id}' in parents and "
                               f"{mimeType} "
                               f"name = '{name}'")
        if 'files' not in res or len(res['files']) < 1:
            return None
        info = res['files'][0]
        parent_id = res['files'][0]['id']
 
    return info
 
def download_file(service, file_info, output_dir):
    """指定ファイルのダウンロード"""
    req = service.files().get_media(fileId=file_info['id'])
    with open(os.path.join(output_dir, file_info['name']), 'wb') as f:
        downloader = MediaIoBaseDownload(f, req)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {status.progress() * 100}%")
 
def upload_file(service, local_file, remote_folder_id='root', mimetype='text/plain'):
    media = MediaFileUpload(local_file, mimetype=mimetype)
    file = service.files().create(body={'name': os.path.basename(local_file),
                                        'parents': [remote_folder_id]},
                                  media_body=media,
                                  fields='id').execute()
    print(f'File ID: {file.get("id")}')
 
def drive_mkdir(service, name, parent_id):
    res = service.files().create(body={'name': name,
                                       'parents': [parent_id],
                                       'mimeType': 'application/vnd.google-apps.folder'}
                                 ).execute()
 
if __name__ == '__main__':

    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    list_drive_files(service)

    #result = list_drive_files(service, pageSize=50)

    # マイドライブ(トップフォルダ)にあるファイル一覧の取得
    result = list_drive_files(service, q="'root' in parents")

    # 指定のフォルダにあるファイル一覧を取得
    folder_id = get_drive_folder_id(service, ['tmp'])
    result = list_drive_files(service, fields='*', q=f"'{folder_id}' in parents")

    # 作成日時を取得
    result = get_drive_file(service, fields='name,createdTime',
                          fileId='1voasdfjlsIJTvasABdfJPIasfda2V5h4jEhcn0oPkQ')

    # 指定パスのファイルをダウンロード
    file_info = get_drive_file_info(service, ['tmp', 'hoge.txt'])
    download_file(service, file_info, '.')
                        
    # 指定フォルダにファイルをアップロード
    upload_folder_id = get_drive_folder_id(service, ['tmp'])
    upload_file(service, './hoge.txt', upload_folder_id)

    # フォルダの作成
    parent_folder_id = get_drive_folder_id(service, ['tmp'])
    drive_mkdir(service, 'hoge', parent_folder_id)

