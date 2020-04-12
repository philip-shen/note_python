# 2020/04/12 Initial 
######################################################


"""
http://wiki.alarmchang.com/index.php?title=Python_%E4%BD%BF%E7%94%A8_zipfile_%E5%B0%87%E6%95%B4%E5%80%8B%E7%9B%AE%E9%8C%84%E9%83%BD%E5%A3%93%E8%B5%B7%E4%BE%86

版本二～如果要指定壓縮後的檔案路徑，修改如下
他會將 Z:\alarmchang\AutoUpdate 目錄壓起來
存放到 Z:\alarmchang\xyz.zip 中
"""
import zipfile
import os
 
def Achive_Folder_To_ZIP(sFilePath, dest = ""):
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    if (dest == ""):
        zf = zipfile.ZipFile(sFilePath + '.ZIP', mode='w')
    else:
        zf = zipfile.ZipFile(dest, mode='w')
 
    os.chdir(sFilePath)
    #print sFilePath
    for root, folders, files in os.walk(".\\"):
        for sfile in files:
            aFile = os.path.join(root, sfile)
            #print aFile
            zf.write(aFile)
    zf.close()
 
 
if __name__ == "__main__":
    Achive_Folder_To_ZIP(r"Z:\alarmchang\AutoUpdate", r"Z:\alarmchang\xyz.zip")