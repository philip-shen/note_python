#import os.path
import shutil
import unittest
from io import BytesIO, StringIO
from os import path
from time import sleep

from webdav3_base_client_it import BaseClientTestCase
from webdav3.client import Client
from webdav3.exceptions import MethodNotSupported, OptionNotValid, RemoteResourceNotFound, WebDavException

import os, time, sys
import argparse
import json
import pathlib
import concurrent.futures

strabspath=os.path.abspath(sys.argv[0])
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelog=os.path.join(strdirname,"logs")

sys.path.append('./_libs')

from logger_setup import *
import lib_misc

class ClientTestCase(BaseClientTestCase):
    pulled_file = BaseClientTestCase.local_path_dir + os.sep + BaseClientTestCase.local_file

    def test_timeout_set(self):
        self.assertEqual(10, self.client.timeout)

    def test_list(self):
        self._prepare_for_downloading()
        file_list = self.client.list()
        self.assertIsNotNone(file_list, 'List of files should not be None')
        self.assertGreater(file_list.__len__(), 0, 'Expected that amount of files more then 0')

    def test_list_no_parent(self):
        self._prepare_for_downloading(inner_dir=True)
        file_list = self.client.list(self.remote_path_dir)
        for file_name in file_list:
            self.assertNotEqual(self.remote_path_dir, file_name, 'Result should not contain parent directory')

    def test_list_info(self):
        self._prepare_for_downloading()
        list_info = self.client.list(get_info=True)
        self.assertIsNotNone(list_info, 'List of files should not be None')
        self.assertTrue('created' in list_info[0].keys(), 'info should contain created')
        self.assertTrue('name' in list_info[0].keys(), 'info should contain name')
        self.assertTrue('modified' in list_info[0].keys(), 'info should contain modified')
        self.assertTrue('size' in list_info[0].keys(), 'info should contain size')
        self.assertTrue('etag' in list_info[0].keys(), 'info should contain etag')
        self.assertTrue('isdir' in list_info[0].keys(), 'info should contain isdir')
        self.assertTrue('path' in list_info[0].keys(), 'info should contain path')
        self.assertTrue('content_type' in list_info[0].keys(), 'info should contain content_type')

    def test_free(self):
        if 'localhost' in self.options['webdav_hostname']:
            with self.assertRaises(MethodNotSupported):
                self.client.free()
        else:
            self.assertNotEqual(self.client.free(), 0, 'Expected that free space on WebDAV server is more then 0 bytes')

    def test_check(self):
        self._prepare_for_downloading(inner_dir=True)
        self.assertTrue(self.client.check(), 'Expected that root directory is exist')
        self.assertTrue(self.client.check(self.remote_path_dir), 'Expected that the directory is exist')
        self.assertTrue(self.client.check(self.remote_inner_path_dir), 'Expected that the inner directory is exist')
        self.assertTrue(self.client.check(self.remote_path_file), 'Expected that the file is exist')
        self.assertTrue(self.client.check(self.remote_inner_path_file), 'Expected that the inner file is exist')

    def test_check_does_not_exist(self):
        self._prepare_for_downloading(inner_dir=True)
        self.assertFalse(self.client.check('wrong'), 'Expected that the directory is not exist')
        self.assertFalse(self.client.check(self.remote_path_dir + '/wrong'), 'Expected that the inner directory is not exist')
        self.assertFalse(self.client.check(self.remote_path_dir + '/wrong.txt'), 'Expected that the file is not exist')
        self.assertFalse(self.client.check(self.remote_inner_path_dir + '/wrong.txt'), 'Expected that the inner file is not exist')

    def test_check_another_client(self):
        self._prepare_for_uploading()
        client = Client(self.options)
        if self.client.check(self.remote_path_dir):
            self.client.clean(self.remote_path_dir)
        self.assertTrue(self.client.mkdir(self.remote_path_dir))
        self.assertTrue(self.client.check(self.remote_path_dir))

        self.client.upload_sync(remote_path=self.remote_path_file, local_path=self.local_path_dir)
        self.assertTrue(self.client.check(self.remote_path_file))

        self.assertTrue(client.check(self.remote_path_dir))
        self.assertTrue(client.check(self.remote_path_file))

    def test_mkdir(self):
        if self.client.check(self.remote_path_dir):
            self.client.clean(self.remote_path_dir)
        self.client.mkdir(self.remote_path_dir)
        self.assertTrue(self.client.check(self.remote_path_dir), 'Expected the directory is created.')

    def test_download_from(self):
        self._prepare_for_downloading()
        buff = BytesIO()
        self.clipathent.download_from(buff=buff, remote_path=self.remote_path_file)
        self.assertEqual(buff.getvalue(), b'test content for testing of webdav client')

    def test_download_from_compressed(self):
        self._prepare_dir_for_downloading(self.remote_path_dir, self.remote_compressed_path_file, local_file_path=self.local_compressed_file_path)
        buff = BytesIO()
        self.client.download_from(buff=buff, remote_path=self.remote_compressed_path_file)
        self.assertIn(b'test content for testing of webdav client', buff.getvalue())

    def test_download_from_dir(self):
        self._prepare_for_downloading()
        buff = BytesIO()
        with self.assertRaises(OptionNotValid):
            self.client.download_from(buff=buff, remote_path=self.remote_path_dir)

    def test_download_from_wrong_file(self):
        self._prepare_for_downloading()
        buff = BytesIO()
        with self.assertRaises(RemoteResourceNotFound):
            self.client.download_from(buff=buff, remote_path='wrong')

    def test_download_directory_wrong(self):
        self._prepare_for_downloading()
        with self.assertRaises(RemoteResourceNotFound):
            self.client.download_directory(remote_path='wrong', local_path=self.local_path_dir)

    def test_download(self):
        self._prepare_for_downloading()
        self.client.download(local_path=self.local_path_dir, remote_path=self.remote_path_dir)
        self.assertTrue(path.exists(self.local_path_dir), 'Expected the directory is downloaded.')
        self.assertTrue(path.isdir(self.local_path_dir), 'Expected this is a directory.')
        self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.local_file),
                        'Expected the file is downloaded')
        self.assertTrue(path.isfile(self.local_path_dir + os.path.sep + self.local_file),
                        'Expected this is a file')

    def test_download_sync(self):
        self._prepare_for_downloading()

        def callback():
            self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.local_file),
                            'Expected the file is downloaded')
            self.assertTrue(path.isfile(self.local_path_dir + os.path.sep + self.local_file),
                            'Expected this is a file')

        self.client.download_sync(local_path=self.local_path_dir + os.path.sep + self.local_file,
                                  remote_path=self.remote_path_file, callback=callback)
        self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.local_file),
                        'Expected the file has already been downloaded')

    def test_download_async(self):
        self._prepare_for_downloading()

        def callback():
            self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.local_file),
                            'Expected the file is downloaded')
            self.assertTrue(path.isfile(self.local_path_dir + os.path.sep + self.local_file),
                            'Expected this is a file')

        self.client.download_async(local_path=self.local_path_dir + os.path.sep + self.local_file,
                                   remote_path=self.remote_path_file, callback=callback)
        self.assertFalse(path.exists(self.local_path_dir + os.path.sep + self.local_file),
                         'Expected the file has not been downloaded yet')
        # It needs for ending download before environment will be cleaned in tearDown
        sleep(0.4)

    def test_upload_from(self):
        self._prepare_for_uploading()
        buff = StringIO()
        buff.write(u'test content for testing of webdav client')
        self.client.upload_to(buff=buff, remote_path=self.remote_path_file)
        self.assertTrue(self.client.check(self.remote_path_file), 'Expected the file is uploaded.')

    def test_upload(self):
        self._prepare_for_uploading()
        self.client.upload(remote_path=self.remote_path_file, local_path=self.local_path_dir)
        self.assertTrue(self.client.check(self.remote_path_dir), 'Expected the directory is created.')
        self.assertTrue(self.client.check(self.remote_path_file), 'Expected the file is uploaded.')

    def test_upload_file(self):
        self._prepare_for_uploading()
        self.client.upload_file(remote_path=self.remote_path_file, local_path=self.local_file_path)
        self.assertTrue(self.client.check(remote_path=self.remote_path_file), 'Expected the file is uploaded.')

    def test_upload_sync(self):
        self._prepare_for_uploading()

        def callback():
            self.assertTrue(self.client.check(self.remote_path_dir), 'Expected the directory is created.')
            self.assertTrue(self.client.check(self.remote_path_file), 'Expected the file is uploaded.')

        self.client.upload_sync(remote_path=self.remote_path_file, local_path=self.local_path_dir, callback=callback)

    def test_copy(self):
        self._prepare_for_downloading()
        self.client.mkdir(remote_path=self.remote_path_dir2)
        self.client.copy(remote_path_from=self.remote_path_file, remote_path_to=self.remote_path_file2)
        self.assertTrue(self.client.check(remote_path=self.remote_path_file2))

    def test_move(self):
        self._prepare_for_downloading()
        self.client.mkdir(remote_path=self.remote_path_dir2)
        self.client.move(remote_path_from=self.remote_path_file, remote_path_to=self.remote_path_file2)
        self.assertFalse(self.client.check(remote_path=self.remote_path_file))
        self.assertTrue(self.client.check(remote_path=self.remote_path_file2))

    def test_clean(self):
        self._prepare_for_downloading()
        self.client.clean(remote_path=self.remote_path_dir)
        self.assertFalse(self.client.check(remote_path=self.remote_path_file))
        self.assertFalse(self.client.check(remote_path=self.remote_path_dir))

    def test_info(self):
        self._prepare_for_downloading()
        result = self.client.info(remote_path=self.remote_path_file)
        self.assertEqual(result['size'], '41')
        self.assertTrue('created' in result)
        self.assertTrue('modified' in result)

    def test_directory_is_dir(self):
        self._prepare_for_downloading()
        self.assertTrue(self.client.is_dir(self.remote_path_dir), 'Should return True for directory')

    def test_file_is_not_dir(self):
        self._prepare_for_downloading()
        self.assertFalse(self.client.is_dir(self.remote_path_file), 'Should return False for file')

    def test_get_property_of_non_exist(self):
        self._prepare_for_downloading()
        result = self.client.get_property(remote_path=self.remote_path_file, option={'name': 'aProperty'})
        self.assertEqual(result, None, 'For not found property should return value as None')

    def test_set_property(self):
        self._prepare_for_downloading()
        self.client.set_property(remote_path=self.remote_path_file, option={
            'namespace': 'http://test.com/ns',
            'name': 'aProperty',
            'value': 'aValue'
        })
        result = self.client.get_property(remote_path=self.remote_path_file,
                                          option={'namespace': 'http://test.com/ns', 'name': 'aProperty'})
        self.assertEqual(result, 'aValue', 'Property value should be set')

    def test_set_property_batch(self):
        self._prepare_for_downloading()
        self.client.set_property_batch(remote_path=self.remote_path_file, option=[
            {
                'namespace': 'http://test.com/ns',
                'name': 'aProperty',
                'value': 'aValue'
            },
            {
                'namespace': 'http://test.com/ns',
                'name': 'aProperty2',
                'value': 'aValue2'
            }
        ])
        result = self.client.get_property(remote_path=self.remote_path_file,
                                          option={'namespace': 'http://test.com/ns', 'name': 'aProperty'})
        self.assertEqual(result, 'aValue', 'First property value should be set')
        result = self.client.get_property(remote_path=self.remote_path_file,
                                          option={'namespace': 'http://test.com/ns', 'name': 'aProperty2'})
        self.assertEqual(result, 'aValue2', 'Second property value should be set')

    def test_pull(self):
        self._prepare_for_downloading(True)
        self.client.pull(self.remote_path_dir, self.local_path_dir)
        self.assertTrue(path.exists(self.local_path_dir), 'Expected the directory is downloaded.')
        self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.inner_dir_name), 'Expected the directory is downloaded.')
        self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.inner_dir_name), 'Expected the directory is downloaded.')
        self.assertTrue(path.isdir(self.local_path_dir), 'Expected this is a directory.')
        self.assertTrue(path.isdir(self.local_path_dir + os.path.sep + self.inner_dir_name), 'Expected this is a directory.')
        self.assertTrue(path.exists(self.local_path_dir + os.path.sep + self.local_file),
                        'Expected the file is downloaded')
        self.assertTrue(path.isfile(self.local_path_dir + os.path.sep + self.local_file),
                        'Expected this is a file')

    def test_push(self):
        self._prepare_for_uploading()
        self.client.push(self.remote_path_dir, self.local_path_dir)
        self.assertTrue(self.client.check(self.remote_path_dir), 'Expected the directory is created.')
        self.assertTrue(self.client.check(self.remote_path_file), 'Expected the file is uploaded.')

    def test_valid(self):
        self.assertTrue(self.client.valid())

    def test_check_is_overridden(self):
        self.assertEqual('GET', self.client.requests['check'])

    def test_pull_newer(self):
        init_modification_time = int(self._prepare_local_test_file_and_get_modification_time())
        sleep(1)
        self._prepare_for_downloading(base_path='time/')
        result = self.client.pull('time/' + self.remote_path_dir, self.local_path_dir)
        update_modification_time = int(os.path.getmtime(self.pulled_file))
        self.assertTrue(result)
        self.assertGreater(update_modification_time, init_modification_time)
        self.client.clean(remote_path='time/' + self.remote_path_dir)

    def test_pull_older(self):
        self._prepare_for_downloading(base_path='time/')
        sleep(1)
        init_modification_time = int(self._prepare_local_test_file_and_get_modification_time())
        result = self.client.pull('time/' + self.remote_path_dir, self.local_path_dir)
        update_modification_time = int(os.path.getmtime(self.pulled_file))
        self.assertFalse(result)
        self.assertEqual(update_modification_time, init_modification_time)
        self.client.clean(remote_path='time/' + self.remote_path_dir)

    def test_push_newer(self):
        self._prepare_for_downloading(base_path='time/')
        sleep(1)
        self._prepare_for_uploading()
        init_modification_time = self.client.info('time/' + self.remote_path_file)['modified']
        result = self.client.push('time/' + self.remote_path_dir, self.local_path_dir)
        update_modification_time = self.client.info('time/' + self.remote_path_file)['modified']
        self.assertTrue(result)
        self.assertNotEqual(init_modification_time, update_modification_time)
        self.client.clean(remote_path='time/' + self.remote_path_dir)

    def test_push_older(self):
        self._prepare_for_uploading()
        sleep(1)
        self._prepare_for_downloading(base_path='time/')
        init_modification_time = self.client.info('time/' + self.remote_path_file)['modified']
        result = self.client.push('time/' + self.remote_path_dir, self.local_path_dir)
        update_modification_time = self.client.info('time/' + self.remote_path_file)['modified']
        self.assertFalse(result)
        self.assertEqual(init_modification_time, update_modification_time)
        self.client.clean(remote_path='time/' + self.remote_path_dir)

    def _prepare_local_test_file_and_get_modification_time(self):
        if not path.exists(path=self.local_path_dir):
            os.mkdir(self.local_path_dir)
        if not path.exists(path=self.local_path_dir + os.sep + self.local_file):
            shutil.copy(src=self.local_file_path, dst=self.pulled_file)
        return os.path.getmtime(self.pulled_file)

def est_timer():
    time_consumption, h, m, s= lib_misc.format_time(time.time() - t0)         
    msg = 'Time Consumption: {}.'.format( time_consumption)#msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg)

def progress(c, t):
    logger.info(f"RX: {c} bytes / TX: {t} bytes")

def upload_async(webdav_client, remote_path, local_path):
    # Exception handling    
    try:
        # Upload resource async
        kwargs = {'remote_path': remote_path,
                  'local_path':  local_path,
                  'progress': progress
                }
        rtu_upload_status = webdav_client.upload_async(**kwargs)
        logger.info(f'rtu_upload_status: {rtu_upload_status}')      

        sleep(1)
    except WebDavException as exception:
        logger.info(f'exception: {exception}')

def chk_remote_images_num(remote_path, suffix='.jpg', opt_verbose='OFF'):  
    files = []        
    try:
        files4 = client.list(remote_path)
        files = [file for file in files4 if file.lower().endswith(suffix) ]
    
        if opt_verbose.lower() == 'on':
            logger.info(f'files4: {files4}')    
            logger.info(f'len of files: {len(files)}')
    
    except RemoteResourceNotFound:
            if not client.check(remote_path):
                client.mkdir(remote_path)

    return len(files), files

class remote_server_backup():
    def __init__(self, webdav_client, remote_path, local_path, 
                 remote_file_suffix, opt_verbose='OFF') -> None:
        self.webdav_client = webdav_client
        self.remote_path = remote_path
        self.local_path = local_path
        self.remote_file_suffix = remote_file_suffix
        self.opt_verbose = opt_verbose

    def chk_remote_images_num(self):    
        files = []        
        try:
            files4 = self.webdav_client.list(self.remote_path)
            files = [file for file in files4 if file.lower().endswith(self.remote_file_suffix) ]

            if self.opt_verbose.lower() == 'on':
                logger.info(f'files4: {files4}')    
                logger.info(f'len of files: {len(files)}')

        except RemoteResourceNotFound:
            if not self.webdav_client.check(remote_path=self.remote_path):
                self.webdav_client.mkdir(remote_path=self.remote_path)

        return len(files), files
    
    def query_remote_path_file(self):
        logger.info(f'query remote path : {self.remote_path} file(s)....')
        self.num_remote_files, self.list_remote_files = \
            self.chk_remote_images_num()
        
    def query_local_path_file(self):
        logger.info(f'query local path: {self.local_path} file(s)....')
        rec_file_type = '*.*'
        local_query_all_files= lib_misc.Query_all_files_in_dir(self.local_path, rec_file_type, opt_verbose='off')
        list_folder_wav_files= local_query_all_files.walk_in_dir()    
        self.list_local_wav_files = [wav_file.split('/')[-1]  for wav_file in list_folder_wav_files ]

    def backup_async(self):
        self.query_remote_path_file()
        self.query_local_path_file()

        logger.info(f'len of list_local_wav_files: { len(self.list_local_wav_files) }; len of list_remote_files: {self.num_remote_files}')

        list_diff_local_remote_files = lib_misc.Diff_List(self.list_local_wav_files, self.list_remote_files) 
        logger.info(f'len of list_diff_local_remote_files: {len(list_diff_local_remote_files)}')

        for diff_local_remote_file in list_diff_local_remote_files:
            logger.info(f'\nremote_file: {self.remote_path}/{diff_local_remote_file};\nlocal_file: {self.local_path}/{diff_local_remote_file}')
            
            upload_async(webdav_client= self.webdav_client, 
                     remote_path= f'{self.remote_path}/{diff_local_remote_file}' , 
                    local_path= f'{self.local_path}/{diff_local_remote_file}' 
                     )
            sleep(0.5)

        if len(list_diff_local_remote_files) > 0:
            self.query_remote_path_file()
            logger.info(f'len of list_local_wav_files: { len(self.list_local_wav_files) }; len of list_remote_files: {self.num_remote_files}')

    def backup_async_concurrent(self):
        self.query_remote_path_file()
        self.query_local_path_file()

        logger.info(f'len of list_local_wav_files: { len(self.list_local_wav_files) }; len of list_remote_files: {self.num_remote_files}')

        list_diff_local_remote_files = lib_misc.Diff_List(self.list_local_wav_files, self.list_remote_files) 
        logger.info(f'len of list_diff_local_remote_files: {len(list_diff_local_remote_files)}')

        list_remote_path_fname = [f'{self.remote_path}/{diff_local_remote_file}' for diff_local_remote_file in list_diff_local_remote_files]
        list_local_path_fname = [f'{self.local_path}/{diff_local_remote_file}' for diff_local_remote_file in list_diff_local_remote_files]

        if self.opt_verbose.lower() == 'on':
            logger.info(f'len of list_remote_path_fname: {len(list_remote_path_fname)}')
            logger.info(f'len of list_local_path_fname: {len(list_local_path_fname)}')

        # concurrent run segmentation (multi-process method)
        with concurrent.futures.ProcessPoolExecutor(max_workers=40) as executor:
            futures = executor.map(upload_async,
                                   [self.webdav_client]*len(list_diff_local_remote_files),
                                   list_remote_path_fname, 
                                   list_local_path_fname )
        
        if len(list_diff_local_remote_files) > 0:
            self.query_remote_path_file()
            logger.info(f'len of list_local_wav_files: { len(self.list_local_wav_files) }; len of list_remote_files: {self.num_remote_files}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test WebDAV for fsspec module')
    parser.add_argument('--conf', type=str, default='config.json', help='Config json')
    args = parser.parse_args()

    logger_set(strdirname)
    
    # Get present ti    me
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                            local_time.tm_hour,local_time.tm_min,local_time.tm_sec))
    
    opt_verbose = 'On'
    json_file= args.conf
    json_path_file = pathlib.Path(strdirname)/json_file
    
    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )
        est_timer()
        sys.exit()

    if (not os.path.isfile(json_file))  :
        msg = 'Please check json file:{}  if exist!!! '
        logger.info(msg.format(json_file) )
        est_timer()
        sys.exit()
    
    #with open(json_file, encoding="utf-8") as f:
    #    json_data = json.load(f)  

    json_data = json.load(json_path_file.open())

    home = os.path.expanduser("~")
    dir_data_training = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][0]["path_data_training"]    
    dir_data_testing = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][0]["path_data_testing"] 
    dir_data_validation = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][0]["path_data_validation"]

    dir_janke_choki = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][1]["path_janke_choki"]
    dir_janke_gu = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][1]["path_janke_gu"]
    dir_janke_pa = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][1]["path_janke_pa"]

    dir_faces = pathlib.Path(f'{home}/projects')/json_data["path_dataset"][2]["path_faces"]

    webdav_url = json_data["webdav_url"]
    auth_username = json_data["auth_username"]
    auth_api_key = json_data["auth_api_key"]
    webdav_timeout = json_data["webdav_timeout"]

    options = {
        'webdav_hostname': webdav_url,
        'webdav_login':    auth_username,
        'webdav_password': auth_api_key,
        'webdav_timeout': webdav_timeout
    }
    client = Client(options)

    # Checking existence of the resource
    #rtu_status = client.check(json_data["path_dataset"][0]["path_data_testing"])
    #logger.info(f'rtu_status: {rtu_status}')

    #rtu_info = client.info(json_data["path_dataset"][0]["path_data_testing"])
    #logger.info(f'rtu_info: {rtu_info}')

    #files1 = client.list()
    #logger.info(f'files1: {files1}')
    
    #files2 = client.list(json_data["path_dataset"][0]["path_data_testing"])
    #logger.info(f'files2: {files2}')
    #files3 = client.list(json_data["path_dataset"][0]["path_data_training"])
    #logger.info(f'files3: {files3}')

    #upload_async(json_data["path_dataset"][1]["path_janke_choki"], dir_janke_choki)
    #chk_images_num(json_data["path_dataset"][1]["path_janke_choki"])
    """
    local_remote_server_backup = remote_server_backup(webdav_client= client, 
                                                    remote_path = json_data["path_dataset"][0]["path_data_training"],
                                                    local_path = dir_data_training, 
                                                    remote_file_suffix = '.jpg', 
                                                    opt_verbose=opt_verbose )    
    local_remote_server_backup.backup_async()

    local_remote_server_backup = remote_server_backup(webdav_client= client, 
                                                    remote_path = json_data["path_dataset"][0]["path_data_testing"],
                                                    local_path = dir_data_testing, 
                                                    remote_file_suffix = '.jpg', 
                                                    opt_verbose=opt_verbose )    
    local_remote_server_backup.backup_async()

    local_remote_server_backup = remote_server_backup(webdav_client= client, 
                                                    remote_path = json_data["path_dataset"][0]["path_data_validation"],
                                                    local_path = dir_data_validation, 
                                                    remote_file_suffix = '.jpg', 
                                                    opt_verbose=opt_verbose )    
    local_remote_server_backup.backup_async()
    """
    
    local_remote_server_backup = remote_server_backup(webdav_client= client, 
                                                    remote_path = json_data["path_dataset"][2]["path_faces"],
                                                    local_path = dir_faces, 
                                                    remote_file_suffix = '.jpg', 
                                                    opt_verbose=opt_verbose )    
    
    local_remote_server_backup.backup_async_concurrent()
    
    #est_timer()