#2018/09/26 Intial modlue related google drive
#2018/09/29 Add def list_folder(), def list_folder() 
#           def folder_browser() and def download()
#2018/10/06 Add checkFolderExistence()
#2018/10/12 Add class GoogleDrivebyFileID 
####################################################
import glob, os, re
import sys, time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#2018/11/16 https://github.com/ITCoders/SyncIt/blob/master/src/drive_sync.py
######################################################################
class GoogleCloudDrive:
    def __init__(self,str_localdir):
        self.str_localdir = str_localdir
        #done_paths = []
        self.done_paths = []
        #browsed = []
        self.browsed = []

    def checkfolderExistence(self):
        if not os.path.isdir(self.str_localdir):
            os.makedirs(self.str_localdir)

    def querylocalfiles(self,re_pattern):
        #os.chdir(self.str_localdir)
        #for file in glob.glob("*.{}".format(str_filetype)):
        list_filename = []
        for f in os.listdir(self.str_localdir):
            try:
                if re.search(re_pattern, f):
                    print("Search file: {} in {}".format(f,self.str_localdir))
                    list_filename.append(f)
            except FileNotFoundError as e:
                print(e)

        if len(list_filename) > 0:
            print('Total {} file(s) under {}.'.format(len(list_filename),self.str_localdir))
        elif len(list_filename) == 0:
            print('No {} like file(s) under {}.'.format(re_pattern,self.str_localdir))
        
        return list_filename  

    def purgelocalfiles(self, re_pattern):
        # Check image sudfloder is existing or not
        self.checkfolderExistence()
        
        #check existing files under specific folder
        rtu_list_filename = self.querylocalfiles(re_pattern)

        if len(rtu_list_filename) > 0:
            for f in os.listdir(self.str_localdir):
                if re.search(re_pattern, f):
                    os.remove(os.path.join(self.str_localdir, f))
                    print('Delete {}'.format(os.path.join(self.str_localdir, f)))
        else:
            print('No {} like files to be deleted.'.format(re_pattern))

        

    #"""
    #Google Drive Authentication
    #
    #Automating pydrive verification process
    #https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process/24542604#24542604
    #"""
    def GDriveAuth(self,str_dir_client_credentials):
        print('Google Authentication Started')
        #Google Drive authentication
        gauth = GoogleAuth()
        #gauth.LocalWebserverAuth()# Creates local webserver and auto handles authentication.
        #gauth.CommandLineAuth() #透過授權碼認證

        # Try to load saved client credentials
        gauth.LoadCredentialsFile(str_dir_client_credentials)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
            print('Google Authentication Save current credentials.')
            # Save the current credentials to a file
            gauth.SaveCredentialsFile('client_secrets.json')
        elif gauth.access_token_expired:
            print('Google Authentication Refresh current credentials.')
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        
        print('Google Authentication Completed!') 
        return gauth
    '''2018/11/18
    {'id': '1BDjWcTnzhMEvmoy78rgaf9ITxCNjxKhD', 'title': '20181111', 
    'list': [{'title': 'put_波段_6176_瑞儀.jpg', 'title1': 'https://drive.google.com/file/d/1whTz5SroTzWtEsAVYl5SUzX6YhJSt7uY/view?usp=drivesdk','modifiedDate': '2018-11-17T08:25:05.280Z'}, 
    {'title': 'put_波段_5225_東科-KY.jpg', 'title1': 'https://drive.google.com/file/d/1VgKYtWMUzkCzmNTOwVG1NqLTSop0vckT/view?usp=drivesdk','modifiedDate': '2018-11-17T08:24:59.769Z'}, 
    {'title': 'put_景氣_5522_遠雄.jpg', 'title1': 'https://drive.google.com/file/d/1-iYIJQ451Bj8X79QOsv12RzwCnmHdo1u/view?usp=drivesdk','modifiedDate': '2018-11-17T08:24:54.776Z'}, 
    {'title': 'put_景氣_2617_台航.jpg', 'title1': 'https://drive.google.com/file/d/1QYCIUzR0kDwpogC4U8WW8KCu1PykyKXZ/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_景氣_2542_興富發.jpg', 'title1': 'https://drive.google.com/file/d/1bosIkZs0n-bOJHINGOWzn3xRracMRxn6/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_景氣_2534_宏盛.jpg', 'title1': 'https://drive.google.com/file/d/1Db6Lp0DaZ4dDAKU1tVDl2tmxGLjDyXkk/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_景氣_2031_新光鋼.jpg', 'title1': 'https://drive.google.com/file/d/1QC18SMXtw9daUkQ8_2vCdmWF2NgmMI_S/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_景氣_2027_大成鋼.jpg', 'title1': 'https://drive.google.com/file/d/1YZVUdjilf-qyqI801fGd56-UNZbj40kx/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_景氣_1904_正隆.jpg', 'title1': 'https://drive.google.com/file/d/1oE_e17671dqaOlf1Gn0ofsPwdWcrqvWn/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_循環_9910_豐泰.jpg', 'title1': 'https://drive.google.com/file/d/1xx5Ot9rItQjhLOanm-J7AEbd1kyprRYF/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_循環_5015_華祺.jpg', 'title1': 'https://drive.google.com/file/d/1Wp2qNlpORdcat-SxTwLn7YbaYecCZ1aQ/view?usp=drivesdk','modifiedDate':...}, 
    {'title': 'put_循環_3090_日電貿.jpg', 'title1': 'https://drive.google.com/file/d/1GCo_kYHH2-2nAusnVyo0xpBXfCurpOCP/view?usp=drivesdk','modifiedDate':...},...}
    '''
    def listfolder(self,Gdrive,parent):
        filelist=[]
        file_list = Gdrive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
        
        for f in file_list:
            if f['mimeType']=='application/vnd.google-apps.folder': # if folder
                filelist.append({"id":f['id'],"title":f['title'],"list":self.listfolder(Gdrive,f['id'])})
            else:
                #2018/11/18 
                # filelist.append({"title":f['title'],"title1":f['alternateLink']})
                filelist.append({"title":f['title'],"title1":f['alternateLink'], "modifiedDate":f['modifiedDate']})
    
        return filelist

    #"""
    #Countdown to wait between events
    #"""
    def countdown(self,t):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '\r{:02d}:{:02d}'.format(mins, secs)
            sys.stdout.write(timeformat)
            sys.stdout.flush()
            time.sleep(1)
        t -= 1
    #"""
    #Uploads an image to Google Drive
    #"""
    def uploadtoGDrive(self,drive,parent,gd_folderName,uploadfilename):
        
        # makeup uploadfilename including local path
        str_dirfilename = os.path.join(self.str_localdir,uploadfilename)
        # Name of the folder where I'd like to upload images
        upload_folder = gd_folderName
        # Id of the folder where I'd like to upload images
        upload_folder_id = None

        # Check if folder exists. If not than create one with the given name
        # Check the files and folers in the parent foled
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
        for file_folder in file_list:
            #print(file_folder['title'],upload_folder)
            if file_folder['title'] == upload_folder:
        	    # Get the matching folder id
                upload_folder_id = file_folder['id']
                print('{} is uploaded to EXISTING folder: {}'.format(str_dirfilename, file_folder['title'])) 
                # We need to leave this if it's done
                break
            #else:
                # If there is no mathing folder, create a new one
            #    file_new_folder = drive.CreateFile({'title': upload_folder,
            #        "mimeType": "application/vnd.google-apps.folder"})
            #    file_new_folder.Upload() #Upload the folder to the drive
            #    print('New folder created: {}'.format(file_new_folder['title']))  
            #    upload_folder_id = file_new_folder['id'] #Get the folder id
            #    print('File is uploaded to the NEW folder: {}'.format(file_new_folder['title']))  
            #    break #We need to leave this if it's done

        # Create new file in the upload_folder

        file_image = drive.CreateFile({"parents":  [{"kind": "drive#fileLink","id": upload_folder_id}]})
        file_image.SetContentFile(str_dirfilename) #Set the content to the taken image
        file_image.Upload() # Upload it
    ##################################################    
    # from https://github.com/ITCoders/SyncIt/blob/master/src/drive_sync.py
    # """ function of getting id of a given filename """
    ##################################################
    def id_of_title(self,drive,title, parent_directory_id):

        foldered_list = drive.ListFile({
            'q': "'{}' in parents and trashed=false".format(parent_directory_id)
        }).GetList()

        #print(foldered_list)
        for file in foldered_list:
            #print(file)
            if file['title'] == title:
                return file['id']
        return None

    def create_folder(self,drive,folder_id, subfolder):
        new_folder = drive.CreateFile({
            'title': subfolder,
            'parents': [{'kind': 'drive#fileLink', 'id': folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        })
        new_folder.Upload()
        
        return new_folder
    ############################################################
    #""" function of downloading a specific folder from drive to local """
    ############################################################
    def download(self, drive, folder_id, destination_location):
        if not os.path.exists(destination_location):
             os.makedirs(destination_location)
        
        foldered_list = drive.ListFile({
            'q': "'{}' in parents and trashed=false".format(folder_id)
        }).GetList()     

        for item in foldered_list:
            item_path = os.path.join(destination_location, item['title'])

            if item['mimeType'] == 'application/vnd.google-apps.folder':
                download(item['id'], item_path)
                # print('title: {}, id: {}'.format(item['title'], item['size']))
            else:
                open(item_path, 'w+')  # <-- what does this line do?
                local_size = os.path.getsize(item_path)
                drive_size = item['fileSize']
                if local_size != drive_size:
                    file = drive.CreateFile({'id': item['id']})
                    file.GetContentFile(item_path)

    ##################################################    
    # """ function for uploading source location to designated id """
    ##################################################    
    def upload(self,drive,source_location, folder_id):
        for folder_name, subfolders, filenames in os.walk(source_location):

            if folder_name not in self.done_paths:
                for filename in filenames:
                    file_id = self.id_of_title(drive,filename, folder_id)
                    file_path = os.path.join(folder_name, filename)
                    
                    if file_id is not None:
                        file_drive = drive.CreateFile({'id': file_id})
                        drive_file_size = file_drive['fileSize']
                        local_file_size = os.path.getsize(file_path)
                        
                        if drive_file_size != str(local_file_size):
                            print('Updating exisiting {} to of Google Drive folder:{}.'.format(file_path,os.path.split(folder_name)[1]) )
                            file_drive.SetContentFile(file_path)
                            file_drive.Upload()
                            # else:
                             #     #blank
                    else:
                        new_file = drive.CreateFile({
                            'title': filename,
                            'parents': [{
                                'kind': 'drive#fileLink',
                                'id': folder_id
                            }]
                        })
                        print('Uploading new {} to of Google Drive folder:{}.'.format(file_path,os.path.split(folder_name)[1]) )
                        new_file.SetContentFile(file_path)
                        new_file.Upload()

            if subfolders:
                for subfolder in subfolders:
                    subfolder_id = self.id_of_title(drive,subfolder, folder_id)

                    if subfolder_id is None:
                        new_sub_folder = self.create_folder(drive,folder_id, subfolder)
                        subfolder_id = new_sub_folder['id']
                    
                    abs_path = os.path.join(folder_name, subfolder)
                    self.upload(drive,abs_path, subfolder_id)
                    self.done_paths.append(abs_path)

    ##################################################                    
    #""" function for creating a folder and upload into that """
    ##################################################    
    def upload_folder(self,drive, parent_id):
        source_location = self.str_localdir
        folder_name = os.path.split(source_location)[1]
        id_of_folder = self.id_of_title(drive,folder_name, parent_id)
        
        if id_of_folder is None:
            new_folder = drive.CreateFile({
                'title': folder_name,
                'parents': [{'kind': 'drive#fileLink', 'id': parent_id}],
                'mimeType': 'application/vnd.google-apps.folder'
            })
            new_folder.Upload()
            id_of_folder = new_folder['id']

        self.upload(drive,source_location, id_of_folder)
    ##################################################        
    #""" function for returning file tree structure from parentid """
    ##################################################    
    def list_folder(self,drive,parent):
        filelist = []
        file_list = drive.ListFile(
            {'q': "'%s' in parents and trashed=false" % parent}).GetList()        
        
        for f in file_list:
            if f['mimeType'] == 'application/vnd.google-apps.folder': # if folder
                filelist.append({
                    'id': f['id'],
                    'title': f['title'],
                    'list': self.list_folder(drive,f['id'])
                })
            else:
                filelist.append(f['title'])
        
        return filelist
    ##################################################               
    #""" function to get the current user's name and email address """
    ##################################################
    def get_username(self,drive_object):
        user_info = drive_object.GetAbout()['user']
        print('Logged in as: {displayName} ({emailAddress})\n'.format(**user_info))
        return user_info['displayName']

    ##################################################        
    #""" function for browsing into drive directory """
    ##################################################    
    def folder_browser(self,drive,folder_structure, folder_id):
        if not folder_structure:
            print('└── >>> Empty Folder <<<')
        else:
            total_items = len(folder_structure)
            for dex, item in enumerate(folder_structure, 1):
                print('{} {}'.format(
                    '└──' if dex == total_items else '├──',
                    item['title'] if isinstance(item, dict) else item))

        folder_name = input("\nEnter Name of Folder You Want to Use\n"
                            "Enter '/' to use current folder\n"
                            "Enter ':' to create New Folder and use that\n")

        if folder_name == '/':
            return folder_id
        elif folder_name == ':':
            new_folder_name = input('Enter Name of Folder You Want to Create\n')
            new_folder = self.create_folder(drive,folder_id,new_folder_name)
            folder_path = os.path.join(HOME_DIRECTORY, ROOT_FOLDER_NAME, USERNAME)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            return new_folder['id']
        else:
            folder_selected = folder_name
            for element in folder_structure:
                if isinstance(element, dict) \
                        and element['title'] == folder_selected:
                    struc = element['list']
                    self.browsed.append(folder_selected)
                    print('\n{}'.format(folder_selected))
                    return self.folder_browser(drive,struc, element['id'])    

#rajarsheem/GDrive.py(by FileID)
#https://gist.github.com/rajarsheem/1d9790f0e9846fb429d7
###################################
import io
from mimetypes import MimeTypes
from urllib.parse import urlparse

try:
	from googleapiclient.errors import HttpError
	
	import oauth2client
	from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
	from oauth2client import client
	from oauth2client import tools
except ImportError:
    print('goole-api-python-client is not installed. Try:')
    print('sudo pip install --upgrade google-api-python-client')
    sys.exit(1)
import sys

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'GDrive'

class GoogleDrivebyFileID:
    def __init__(self, str_downloadpath,flags):
        self.str_downloadpath = str_downloadpath
        self.flags = flags

    def get_credentials(self,credential_dir):
        #home_dir = os.path.expanduser('~')
        #credential_dir = os.path.join(home_dir, '.credentials')
        #credential_dir = os.getcwd()
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,CLIENT_SECRET_FILE)
                                       #'drive-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            # if flags:
            credentials = tools.run_flow(flow, store, self.flags)
            # else:  # Needed only for compatibility with Python 2.6
            #     credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        
        return credentials

    def upload(self, service, path, parent_id=None):
        mime = MimeTypes()
        
        file_metadata = {
            'name': os.path.basename(path),
            # 'mimeType' : 'application/vnd.google-apps.spreadsheet'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]

        media = MediaFileUpload(path,
                                mimetype=mime.guess_type(os.path.basename(path))[0],
                                resumable=True)
        try:
            file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        except HttpError:
            print('corrupted file')
            pass
        print(file.get('id'))

    def share(self,service,file_id, email):
        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(response.get('id'))
        
        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': email
        }
        
        batch.add(service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ))
        batch.execute()

    def listfiles(self,service):
        results = service.files().list(fields="nextPageToken, files(id, name,mimeType)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            print('Filename (File ID)')
            for item in items:
                #print('{0} ({1})'.format(item['name'].encode('utf-8'), item['id']))
                print('{0} ({1})'.format(item['name'], item['id']))
            print('Total=', len(items))

    def delete(self,service,fileid):
        service.files().delete(fileId=fileid).execute()

    def getfilename_byfileid(self,service,file_id):
        name = service.files().get(fileId=file_id).execute()['name']
        print('Check file:{} by file_id:{} on Google Drive.'.format(name,file_id))
        return name
    
    #Get filename by fileid from google drive
    #Chk current xls files under log folder.
    #########################################
    def check_xlsfile_MHunterblog_logfolder(self,service,fileid,dirnamelog):
        #get filename by fileid from google drive
        #########################################
        filename_fileid_file = self.getfilename_byfileid(service,fileid)

        #Chk current xls files under log folder.
        ######################################
        localgoogle_drive = GoogleCloudDrive(dirnamelog)
        #re_exp = r'\.xls$'
        re_exp = r'{}'.format(filename_fileid_file)
        list_xls_filename = localgoogle_drive.querylocalfiles(re_exp)

        return list_xls_filename,filename_fileid_file

    def ggdrive_fileid(self,html_doc,xpath_url_file):
        parsed = urlparse(html_doc.xpath(xpath_url_file)[0])# 1st item fo list
    
        #ParseResult(scheme='https', netloc='drive.google.com', path='/file/d/1YaK7owM9M37fnEeXTxoSW_N3JZU5K4Ba/view', params='', query='usp=sharing', fragment='')
        #/file/d/1YaK7owM9M37fnEeXTxoSW_N3JZU5K4Ba/view
        # get fileid by path parm
        fileid = parsed.path.split('/')[-2]
        return fileid

    def download(self,service,file_id):#, path=os.getcwd()
        request = service.files().get_media(fileId=file_id)
        name = service.files().get(fileId=file_id).execute()['name']
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            #print(int(status.progress() * 100))
            print('Download progess: {}%'.format(int(status.progress() * 100)))
        
        #f = open(path + '/' + name, 'wb')
        f = open(self.str_downloadpath + '/' + name, 'wb')
        f.write(fh.getvalue())
        #print('File downloaded at', path)
        print('{} downloaded at {}'.format(name,self.str_downloadpath))
        f.close()

    def createfolder(self, service,folder, recursive=False):
        if recursive:
            print('recursive ON')
            ids = {}
            for root, sub, files in os.walk(folder):
                par = os.path.dirname(root)

                file_metadata = {
                    'name': os.path.basename(root),
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                if par in ids.keys():
                    file_metadata['parents'] = [ids[par]]
                print(root)
                file = service.files().create(body=file_metadata,
                                              fields='id').execute()
                id = file.get('id')
                print(id)
                ids[root] = id
                for f in files:
                    print(root+'/'+f)
                    upload(root + '/' + f, id)
        else:
            print('recursive OFF')
            file_metadata = {
                    'name': os.path.basename(folder),
                    'mimeType': 'application/vnd.google-apps.folder'
                }
            file = service.files().create(body=file_metadata,
                                              fields='id').execute()
            print(file.get('id'))                            