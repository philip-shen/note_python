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
import datetime

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
'''
#chrome_options.add_argument('user-agent="Chrome/73.0.3683.103"')
driver = webdriver.Chrome(chrome_options = chrome_options)

driver.set_window_position(550, 0)
actions = ActionChains(driver)
driver.get(url)
driver.implicitly_wait(15)
'''
url = 'http://192.168.0.1/'

def webdriver_initial(url):
    driver = webdriver.Chrome(chrome_options = chrome_options)

    driver.set_window_position(550, 0)
    actions = ActionChains(driver)
    driver.get(url)
    #driver.implicitly_wait(15)

    return driver

def weblogin(driver,passwd):
    # Need to keyin Password to meet WebGUI Spec.
    # driver.find_element_by_xpath('//*[@id="admin_Password"]').send_keys(Keys.ENTER)
    
    #driver.find_element_by_xpath('//*[@id="admin_Password"]').send_keys("123qwe")
    driver.find_element_by_xpath('//*[@id="admin_Password"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="logIn_btn"]').click()

    #time.sleep(3)


################################################################################
#For Wizard Kernel Panic
################################################################################

def weblogin_new(driver,passwd):
    count_login = 0
    while True:
        driver.get(url)
        r = requests.get(url,timeout=15)
        print ('http %i' %r.status_code)
        try:
            if r.status_code == 200:
                driver.find_element_by_xpath('//*[@id="admin_Password"]').send_keys(passwd)
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="logIn_btn"]').click()
                time.sleep(5)
                if driver.find_element_by_xpath('//*[@id="internetInfo"]/div[1]').is_displayed():
                    print ('Accessed to Home')
                    break
            else:
                print ('WebUI does not response , Will Retry')
        except:
            count_login += 1
            print ('Unable to weblogin . Will Retry for %i times' %count_login)
            if count_login > 10:
                print ('Failed')
                break
                            
def dut_reset(driver,passwd):
    driver.get('http://192.168.0.1/System.html')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="btn_restorToFactoryDefault"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="dialogBtn_restorToFactoryDefaultOk"]').click()
    for i in range(120):
        time.sleep(1)
    print ('Reset was done')


def wizard_flow(driver,passwd):
    wizard_agree = '//*[@id="btn_agree"]'
    wizard_next = '//*[@id="btn_next"]'
    wizard_wifi_name = '//*[@id="wifi_networkName24G_show"]'
    wizard_admin_password = '//*[@id="device_password"]'
    wizard_witing_time = 100

    driver.get(url)
    time.sleep(3)
    WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,wizard_agree)))
    driver.find_element_by_xpath(wizard_agree).click()
    time.sleep(3)
    WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,wizard_next)))
    driver.find_element_by_xpath(wizard_next).click()
    time.sleep(5)
    wifi_name = driver.find_element_by_xpath(wizard_wifi_name).text
    
    for i in range(10):
        try:
            if 'Wi-Fi' in wifi_name:
                break        
        except:
            print('Detect again')

    driver.find_element_by_xpath(wizard_next).click()
    driver.find_element_by_xpath(wizard_admin_password).send_keys(passwd)
    driver.find_element_by_xpath(wizard_next).click()
    time.sleep(2)
    driver.find_element_by_xpath(wizard_next).click()
    time.sleep(2)
    driver.find_element_by_xpath(wizard_next).click()
    time.sleep(2)
    driver.find_element_by_xpath(wizard_next).click()
    print ('Wizard setting was done')
    print ('Waiting for DUT Rebooting')
    for j in range(wizard_witing_time):
        time.sleep(1)
    print ('Reboot is done')

def dut_wizard_new(url,end_times,passwd):
    for i in range(1,end_times):
        print ('<< Running %s times >>' %i)
        driver=webdriver_initial(url)
        weblogin_new(driver,passwd)
        dut_reset(driver,passwd)
        wizard_flow(driver,passwd)
        driver.close()            
        driver.quit()

def ttime(driver):
    #Get time and output date of week
    global week
    #wait 3 secs to go to Time2.html by v1.01b04 
    time.sleep(3)
    
    driver.get('http://192.168.0.1/Time2.html')
    WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="nowDateTimeSpan"]')))
    time.sleep(3)
    dut_time = driver.find_element_by_xpath('//*[@id="nowDateTimeSpan"]')
    dut_time_value = dut_time.text
    print (dut_time_value)

    #import datetime
    year = dut_time_value[0:4]
    month = dut_time_value[5:7]
    day = dut_time_value[8:10]

    date1 = datetime.date(year=int(year),month=int(month),day=int(day))
    week = str(date1.weekday())
    print (week)

def dut_login_out_check(url,end_times,passwd):
    for i in range(1,end_times):
        print ('<< Running %s times >>' %i)
        driver=webdriver_initial(url)
        weblogin_new(driver,passwd)
        #dut_reset(driver,passwd)
        #wizard_flow(driver,passwd)
        ttime(driver)

        driver.close()            
        driver.quit()

if __name__ == '__main__':
    
    #dut_login_out_check(url,20,passwd="1234qwer")

    dut_wizard_new(url,5,passwd="12345678a")