import os, time, sys
import pickle
import json
import pprint
import google.oauth2.credentials
 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

sys.path.append('./_libs')

from logger_setup import *
import lib_misc
pp = pprint.PrettyPrinter(indent=2) 

class GDrive_google_api:
    def __init__(self,conf_json, opt_verbose='OFF'):
        self.conf_json= conf_json
        self.opt_verbose= opt_verbose
        
        if (not os.path.isfile(self.conf_json))  :
            msg = 'Please check json file:{}  if exist!!! '
            logger.info(msg.format(self.conf_json) )
            sys.exit()
    
        with open(self.conf_json, encoding="utf-8") as f:
            json_data = json.load(f) 

        self.CLIENT_SECRETS_FILE = json_data["Client_Secrets_File"]#'client_secret_ubuntu.json' # 各自のclient_secret.jsonファイルへのパスを設定
        self.USER_CREDENTIALS_FILE = os.environ['USERNAME'] + '.credentials' #ユーザ毎の認証データ保存
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.API_SERVICE_NAME = 'drive'
        self.API_VERSION = 'v3'

    def get_authenticated_service(self):
        credentials = None
        if os.path.exists(self.USER_CREDENTIALS_FILE):  #保存したファイルがある場合はロード
            try:
                with open(self.USER_CREDENTIALS_FILE, 'rb') as fi:
                    credentials = pickle.load(fi)
 
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())  # 期限の更新を試みる
            except EOFError as e:
                pass
 
        if credentials is None or not credentials.valid:
            flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
            credentials = flow.run_local_server(port=0)#flow.run_console()
 
        with open(self.USER_CREDENTIALS_FILE, 'wb') as fo:  # 認証情報をファイルに保存
            pickle.dump(credentials, fo)
 
        #return build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)
        self.service= build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)

        return self.service

    def list_drive_files(self, **kwargs):
        results = self.service.files().list(**kwargs).execute()
        
        if self.opt_verbose.lower() == 'on':
            for key, value in kwargs.items():
             msg = "\n key: {} \n value: {}".format(key, value)
             logger.info(msg)   
        
        return results

    def get_drive_folder_id(self, folder_path):
        """指定パスフォルダのfileIdを取得"""
        parent_id = 'root'
        for name in folder_path:
            res = self.list_drive_files(q=f"'{parent_id}' in parents and "
                                   "mimeType = 'application/vnd.google-apps.folder' and "
                                   f"name = '{name}'")
            if 'files' not in res or len(res['files']) < 1:
                return None
            parent_id = res['files'][0]['id']
 
        return parent_id    
 
    def get_drive_file(self, **kwargs):
        results = self.service.files().get(**kwargs).execute()
        return results
 
    def get_drive_file_info(self, path):
        """指定パスのファイル情報を取得"""
        parent_id = 'root'
        path_depth = len(path)
        info = None
        for depth, name in enumerate(path):
            if depth < (path_depth - 1):
                mimeType = "mimeType = 'application/vnd.google-apps.folder' and "
            else:
                mimeType = ""
            res = self.list_drive_files(
                                   q=f"'{parent_id}' in parents and "
                                   f"{mimeType} "
                                   f"name = '{name}'")
            if 'files' not in res or len(res['files']) < 1:
                return None
            info = res['files'][0]
            parent_id = res['files'][0]['id']
    
        return info
 
    def download_file(self, file_info, output_dir):
        """指定ファイルのダウンロード"""
        req = self.service.files().get_media(fileId=file_info['id'])
        with open(os.path.join(output_dir, file_info['name']), 'wb') as f:
            downloader = MediaIoBaseDownload(f, req)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {status.progress() * 100}%")
 
    def upload_file(self, local_file, remote_folder_id='root', mimetype='text/plain'):
        media = MediaFileUpload(local_file, mimetype=mimetype)
        file = self.service.files().create(body={'name': os.path.basename(local_file),
                                            'parents': [remote_folder_id]},
                                      media_body=media,
                                      fields='id').execute()
        print(f'File ID: {file.get("id")}')
 
    def drive_mkdir(self, name, parent_id):
        res = self.service.files().create(body={'name': name,
                                           'parents': [parent_id],
                                           'mimeType': 'application/vnd.google-apps.folder'}
                                     ).execute()

def get_all_files_on_drive(service, opt_verbose= 'OFF'):
    # すべてのファイルの一覧を取得 (全ページ)
    nextPageToken = None
    while True:
        result = service.list_drive_files( pageSize=100, pageToken=nextPageToken)
        msg = '\n nextPageToken: {}'.format(nextPageToken)
        logger.info(msg)
        msg = '\n result: {}'.format(result)
        logger.info(msg)

        if 'nextPageToken' not in result:
            break
        nextPageToken = result['nextPageToken']
'''
Using Google Colab how to drive.files().list more than 1000 files from google drive
https://stackoverflow.com/questions/74717409/using-google-colab-how-to-drive-files-list-more-than-1000-files-from-google-dr

    page_token = ""
    filelist = {}
    while True:
        response = drive_service.files().list(q=query,
                                    corpora='drive',
                                    supportsAllDrives='true',
                                    includeItemsFromAllDrives='true',
                                    driveId=data_drive_id,
                                    pageSize=1000,
                                    fields='nextPageToken, files(id, name, webViewLink)',
                                    pageToken=page_token).execute()

        page_token = response.get('nextPageToken', None)
        filelist.setdefault("files",[]).extend(response.get('files'))

        if (not page_token):
            break

    response = filelist
'''

def get_all_files_under_specific_folder_id(service, list_folders, page_Size=1000, opt_verbose= 'OFF'):
    list_files_info= []
    # 指定のフォルダにあるファイル一覧を取得
    folder_id = service.get_drive_folder_id(list_folders)
    msg = 'folder_id: {}'.format(folder_id)
    logger.info(msg)

    nextPageToken = None
    while True:
        result = service.list_drive_files( pageSize=page_Size, pageToken=nextPageToken, \
                                           fields='nextPageToken, files(id, name)', q=f"'{folder_id}' in parents")
        if opt_verbose.lower() == 'on':
            msg = '\n nextPageToken: {}'.format(nextPageToken)
            logger.info(msg)
            
            for key, list_values in result.items():
                for dict_values in list_values:
                    for key, value in dict_values.items():
                        msg = "\n key: {}; \n value: {}".format(key, value)
                        logger.info(msg)

        list_files_info.append(result)
        if 'nextPageToken' not in result:
            break
        nextPageToken = result['nextPageToken']

    return list_files_info

def get_files_under_specific_folder_id(service, list_folders, opt_verbose= 'OFF'):
    # 指定のフォルダにあるファイル一覧を取得
    folder_id = service.get_drive_folder_id(list_folders)
    msg = 'folder_id: {}'.format(folder_id)
    logger.info(msg)

    result = service.list_drive_files( fields='*', q=f"'{folder_id}' in parents")

    msg = 'result: {}'.format( result)
    logger.info(msg)   

if __name__ == '__main__':

    logger_set(strdirname)
    
    # Get present ti    me
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))         

    if len(sys.argv) != 2:
        msg = 'Please input config json file!!! '
        logger.info(msg)
        sys.exit()

    json_file= sys.argv[1]

    opt_verbose='ON'

    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    local_GDrive_google_api= GDrive_google_api(json_file, opt_verbose)
    local_GDrive_google_api.get_authenticated_service()
    #list_drive_files(service)

    # すべてのファイルの一覧を取得 (1ページ分)
    #result = local_GDrive_google_api.list_drive_files(pageSize=50)
    
    # マイドライブ(トップフォルダ)にあるファイル一覧の取得
    #result = list_drive_files(service, q="'root' in parents")

    # 指定のフォルダにあるファイル一覧を取得
    #get_files_under_specific_folder_id(local_GDrive_google_api, ['food-11', 'food-11_testing'])
    list_all_files_infos= get_all_files_under_specific_folder_id(local_GDrive_google_api, ['food-11', 'food-11_testing'], opt_verbose='off')
    msg = '\n len of list_all_files_infos: {}'.format( len(list_all_files_infos))
    logger.info(msg)
    
    '''msg = '\n list_all_files_infos: \n {}'.format(list_all_files_infos)
    logger.info(msg)
    '''
    
    '''
    {'id': '1LKxQuVerYnILvOvRH2JPX2IzqUi8OhRQ', 'name': '0217.jpg'}
    {'id': '1BuHQot_ktH_m07ctD_8Q4ouYI6GKIkzi', 'name': '0216.jpg'}
    '''
    for dict_all_files_info in list_all_files_infos:
        for key, list_values in dict_all_files_info.items():
            #if key == 'id' or key == 'name':
            #    msg = "\n key: {} \n value: {}".format(key, value)
            #    logger.info(msg)   
            
            t_download = time.time()
            local_time = time.localtime(t_download)
            msg = 'Start Download Time is {}/{}/{} {}:{}:{}'
            logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                                local_time.tm_hour,local_time.tm_min,local_time.tm_sec))   

            for dict_values in list_values:
                msg = "\n'id':{}; 'name': {}".format(dict_values['id'], dict_values['name'])
                '''logger.info(msg)   
                '''
                # 作成日時を取得
                '''result = local_GDrive_google_api.get_drive_file(\
                                    fields='name,createdTime, webViewLink, imageMediaMetadata',
                                    fileId=dict_values['id'])
                msg = "\n result: {}".format( result)
                logger.info(msg)''' 

                # 指定パスのファイルをダウンロード
                file_info = local_GDrive_google_api.get_drive_file_info( ['food-11', 'food-11_testing', dict_values['name']])
                local_GDrive_google_api.download_file(file_info, './logs')

            time_consumption, h, m, s= lib_misc.format_time(time.time() - t_download)         
            msg = 'File Download Time Consumption: {} seconds.'.format( time_consumption)
            logger.info(msg)

    # すべてのファイルの一覧を取得 (全ページ)
    #get_all_files_on_drive(local_GDrive_google_api, opt_verbose= 'OFF')


    '''  
    # 指定フォルダにファイルをアップロード
    upload_folder_id = get_drive_folder_id(service, ['tmp'])
    upload_file(service, './hoge.txt', upload_folder_id)

    # フォルダの作成
    parent_folder_id = get_drive_folder_id(service, ['tmp'])
    drive_mkdir(service, 'hoge', parent_folder_id)
    '''
    time_consumption, h, m, s= lib_misc.format_time(time.time() - t0)         
    msg = 'Time Consumption: {} seconds.'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)