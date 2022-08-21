import re
from logger import *

"""
Parsing hostname and port from string or url
https://stackoverflow.com/questions/9530950/parsing-hostname-and-port-from-string-or-url

p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

m = re.search(p,'http://www.abc.com:123/test')
m.group('host') # 'www.abc.com'
m.group('port') # '123'
"""
from GetCsvColumn import CsvFile,EXCLUDE
        
def get_host_port_globalserver(dir_csv_file_cmd, opt_verbose='OFF'):    
    host, port= '', ''
    p = '(?:globalserver.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

    csvfile = CsvFile(dir_csv_file_cmd)
    """
    globalserver_header,globalserver_cmd,remark
    globalserver,-MicDefault //192.168.3.21/qa/02_Sound_files/01_FW_Test/Mantis_ID1394/test_wav/Cafe_shop_noise_for_PE_01.wav -Dur 10 -SampleRate 48000
    server,globalserver://192.168.3.160:8050
    """
    # example 2: get a column filtered by another column
    header, cmd= csvfile.get_column( 'globalserver_header', 'globalserver_cmd')
    for idx, x in enumerate(header):
        if x.lower() == 'server':
            url_audacity_srv= cmd[idx] 
            
            m = re.search(p, url_audacity_srv)
            host= m.group('host')
            port= m.group('port')

            if opt_verbose.lower() == 'on':
                log_msg='\n url_globalserver_srv: {}; host: {}; port: {} '
                logger.info(log_msg.format(url_audacity_srv, host, port) )
    
    return host, port

def format_time(timesec):
    m, s = divmod(timesec, 60)
    h, m = divmod(m, 60)
    str_format_time= ''
    if h == 0:
        if m == 0:
            str_format_time= "%02ds" % (s)
            #return "%02ds" % (s)
        else:
            str_format_time= "%02dm%02ds" % (m, s)
            #return "%02dm%02ds" % (m, s)
    else:
        str_format_time= "%dh%02dm%02ds" % (h, m, s)
        #return "%dh%02dm%02ds" % (h, m, s)

    return str_format_time, h, m, s
