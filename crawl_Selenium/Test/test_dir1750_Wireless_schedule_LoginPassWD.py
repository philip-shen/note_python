# -*- coding: UTF-8 -*-
#for DLINK-1750 develop

from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select # import select to drop down menu
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
from time import sleep

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('lang=en_US')
#chrome_options.add_argument('--headless') # running in background
chrome_options.add_argument('--proxy-server="direct://"')
chrome_options.add_argument('--proxy-bypass-list=*')
chrome_options.add_argument('--disable-extensions')
#chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"D:\download",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False,
})

#chrome_options.add_argument('user-agent="Chrome/73.0.3683.103"')
driver = webdriver.Chrome(chrome_options = chrome_options)

driver.set_window_position(550, 0)
actions = ActionChains(driver)
url = 'http://192.168.0.1/'
driver.get(url)
driver.implicitly_wait(15)


def weblogin():
    # Need to keyin Password to meet WebGUI Spec.
    # driver.find_element_by_xpath('//*[@id="admin_Password"]').send_keys(Keys.ENTER)
    
    driver.find_element_by_xpath('//*[@id="admin_Password"]').send_keys("123qwe")
    driver.find_element_by_xpath('//*[@id="logIn_btn"]').click()

    time.sleep(3)

def apply():
    driver.find_element_by_xpath('//*[@id="Save_btn"]').click() # Apply_Setting
    time.sleep(50)
    print('Apply config ok')



##################################################################################################

def ttime():
    #Get time and output date of week
    global week
    driver.get('http://192.168.0.1/Time2.html')
    WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="nowDateTimeSpan"]')))
    time.sleep(3)
    dut_time = driver.find_element_by_xpath('//*[@id="nowDateTimeSpan"]')
    dut_time_value = dut_time.text
    #print (dut_time_value)

    import datetime
    year = dut_time_value[0:4]
    month = dut_time_value[5:7]
    day = dut_time_value[8:10]

    date1 = datetime.date(year=int(year),month=int(month),day=int(day))
    week = str(date1.weekday())
    #print (week)
    

def Wireless_Schedule_on_week():
    #Wireless on Schedule Setting
    
    if week == '0':
        day_of_week = 'Monday'
    elif week == '1':
        day_of_week = 'Tuesday'
    elif week == '2':
        day_of_week = 'Wednesday'
    elif week == '3':
        day_of_week = 'Thursday'
    elif week == '4':
        day_of_week = 'Friday'
    elif week == '5':
        day_of_week = 'Saturday'
    elif week == '6':
        day_of_week = 'Sunday'
   
    day_start = '//*[@id="Monday"]/ul/li[1]'
    day_start = day_start.replace('Monday',day_of_week)
    day_start1 = driver.find_element_by_xpath(day_start)
    
    day_end = '//*[@id="Monday"]/ul/li[24]'
    day_end = day_end.replace('Monday',day_of_week)
    day_end1 = driver.find_element_by_xpath(day_end)
    
    ActionChains(driver).drag_and_drop(day_start1,day_end1).perform()
    time.sleep(0.1)
        
    driver.find_element_by_xpath('//*[@id="save_td"]/center/button').click()
    #print ('Add %s Rule of Schedule' %day_of_week)

def Wireless_Schedule_on():
    #Wireless on Schedule Setting
    #Smart connect on
    
    driver.get('http://192.168.0.1/WiFi.html')
    WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="RADIO_smart"]/table/tbody/tr[1]/td/div')))
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="RADIO_24"]/div[1]/span').click()
    driver.find_element_by_xpath('//*[@id="scheduleDrop_24"]').click()
    #a = driver.find_element_by_xpath('//*[@id="scheduleDrop_24"]/div/ul/li[8]')
    # schedule time interval changes from 60 minutes to 30. 
    a = driver.find_element_by_xpath('//*[@id="scheduleDrop_24"]/div/ul/li[16]')

    if a.get_attribute('data-name') == 'Add': 
        #print ('Found Add button')
        driver.find_element_by_xpath('//*[@id="scheduleDrop_24"]/div/ul/li[8]').click()
        Wireless_Schedule_on_week()
        print('Configure 2G on Schedule')
    else:
        print('Not found Add button ,Try again')

    driver.find_element_by_xpath('//*[@id="RADIO_5"]/div[1]/span').click()
    driver.find_element_by_xpath('//*[@id="scheduleDrop_5"]').click()
    #a = driver.find_element_by_xpath('//*[@id="scheduleDrop_5"]/div/ul/li[8]')
    # schedule time interval changes from 60 minutes to 30. 
    a = driver.find_element_by_xpath('//*[@id="scheduleDrop_5"]/div/ul/li[16]')

    if a.get_attribute('data-name') == 'Add': 
       #print ('Found Add button')
       driver.find_element_by_xpath('//*[@id="scheduleDrop_5"]/div/ul/li[8]').click()
       Wireless_Schedule_on_week()
       print('Configure 5G on Schedule')
    else:
       print('Not found Add button ,Try again')

def Wireless_Schedule_Clear():
    driver.get('http://192.168.0.1/WiFi.html')
    WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="RADIO_smart"]/table/tbody/tr[1]/td/div')))
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="RADIO_24"]/div[1]/span').click()

    driver.find_element_by_xpath('//*[@id="scheduleDrop_24"]').click()
    driver.find_element_by_xpath('//*[@id="scheduleDrop_24"]/div/ul/li[1]/div/label').click()
    pop_message = driver.find_element_by_xpath('//*[@id="popMessage"]').text 

    if 'Always Enable' in pop_message:
        #print ('Confirm Message')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="scheduleBtn_ok"]').click()
        print('Clear 2g Schedule')
    else:
        print ('Not Found Message')

    driver.find_element_by_xpath('//*[@id="RADIO_5"]/div[1]/span').click()

    driver.find_element_by_xpath('//*[@id="scheduleDrop_5"]').click()
    driver.find_element_by_xpath('//*[@id="scheduleDrop_5"]/div/ul/li[1]/div/label').click()
    pop_message = driver.find_element_by_xpath('//*[@id="popMessage"]').text

    if 'Always Enable' in pop_message:
        #print ('Confirm Message')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="scheduleBtn_ok"]').click()
        print('Clear 5g Schedule')
    else:
        print ('Not Found Message')

        
if __name__ == '__main__':

    for i in range(1,2):
        print ('<< Running %s times >>' %i)
        r = requests.get(url,timeout=15)
        print ('http %i' %r.status_code)
        page_status_code = r.status_code
        driver.get(url)

        if page_status_code == 200:
            weblogin()
            ttime()
            Wireless_Schedule_on()
            apply()
            Wireless_Schedule_Clear()
            apply()
            
            driver.close()
            driver.quit()
        else:
            print ('Fail - Unable to login the DUT , Please check again ')
            driver.close()
            driver.quit()
            break

    

    
