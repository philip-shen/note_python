# 2019/09/18 Initial 

# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from logger import logger

class method_selenium():
    def __init__(self):
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

        #options.add_experimental_option('prefs', {'intl.accept_languages': locale})
        self.driver = webdriver.Chrome(chrome_options = chrome_options)
        
        logger.info('{0}'.format("Initial Chrome Webbrowser!"))
        
    def setup_method(self):
        self.vars = {}
  
    def method_teardown(self):
        logger.info('{0}'.format("Teardown Chrome Webbrowser!"))        
        self.driver.quit()

    def method_close(self):
        logger.info('{0}'.format("Close Chrome Webbrowser!"))        
        self.driver.close()

    def method_get(self,what):
        logger.info('Open url:{0}'.format(what))        
        self.driver.get(what)
  
    def method_set_window_size(self,x_val, y_val):
        logger.info('Set Browser Size:{0}*{1}'.format(x_val, y_val))
        self.driver.set_window_size(x_val, y_val)

    def method_execute_script(self,what,wait_time=130000):
        logger.info('Execute Script:{0}'.format(what))
        self.driver.execute_script(what)

    def method_by_ID_click(self,what,wait_time=130000):
        logger.info('Click by_ID:{0}'.format(what))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.ID, what)))
        self.driver.find_element(By.ID, what).click()    

    def method_by_ID_mouseOver(self,what,wait_time=130000):
        logger.info('Mouse Over by_ID:{0}'.format(what))
        WebDriverWait(self.driver, 5000).until(expected_conditions.visibility_of_element_located((By.ID, what)))   
        element = self.driver.find_element(By.ID, what)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def method_by_XPath_click(self,what,wait_time=130000):
        logger.info('Click by_XPath:{0}'.format(what))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.XPATH, what)))
        self.driver.find_element(By.XPATH, what).click()        

    def method_by_XPath_send_keys(self,what,keys,wait_time=130000):
        logger.info('Send Keys by_XPath:{0} login_password:{1}'.format(what,keys))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.XPATH, what)))
        self.driver.find_element(By.XPATH, what).send_keys(keys)

    def method_by_XPath_select(self,what,how,wait_time=130000):
        logger.info('Select(Drop down list) by_XPath:{0} value:{1}'.format(what,how))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.XPATH, what)))
        print('testing!')
        el = self.driver.find_element(By.XPATH, what)
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.XPATH, what)))
        print(el.find_elements_by_tag_name('option'))

        for option in el.find_elements_by_tag_name('option'):
            print(option)        
            if option.text in how:
                print(option.text)
                option.click()

    def method_by_LinkText_click(self,what,wait_time=130000):
        logger.info('Click by_Link_Text:{0}'.format(what))    
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, what)))   
        self.driver.find_element(By.LINK_TEXT, what).click()

    def method_by_ID_type(self,what,how,wait_time=130000):
        logger.info('Type by_ID:{0} value:{1}'.format(what,how))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.ID, what)))
        self.driver.find_element(By.ID, what).clear()
        self.driver.find_element(By.ID, what).send_keys(how)

    def method_by_ID_waitforelement_visibile(self,what,wait_time=130000):
        logger.info('Verify by_ID:{0} Visibile'.format(what))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.ID, what)))   
    
    
    def method_by_ID_waitforelement_Invisibile(self,what,wait_time=130000):
        logger.info('Verify by_ID:{0} Invisibile'.format(what))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.invisibility_of_element_located((By.ID, what)))

    def method_by_XPath_waitforelement_visibile(self,what,wait_time=130000):
        logger.info('Verify by_XPATH:{0} Visibile'.format(what))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.XPATH, what)))       
    
    def method_by_ID_verifytext(self,what,how,wait_time=130000):
        logger.info('Verify by_ID:{0} value:{1}'.format(what,how))    
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.ID, what)))   
        #self.driver.find_element(By.ID, "popalert_desc").click()
        assert self.driver.find_element(By.ID, what).text == how

    def method_by_ID_click_chkclickable(self,what,wait_time=130000):
        logger.info('Click by_ID:{0} by check clickable'.format(what))    
        WebDriverWait(self.driver, wait_time).until(expected_conditions.element_to_be_clickable((By.ID, what)))
        self.driver.find_element(By.ID, what).click()
        WebDriverWait(self.driver, wait_time).until(expected_conditions.element_to_be_clickable((By.ID, what)))

    def method_by_ID_verifytext_chkclickable(self,what,how,wait_time=130000):
        logger.info('Verify by_ID:{0} value:{1} by check clickable'.format(what,how))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.element_to_be_clickable((By.ID, what)))
        assert self.driver.find_element(By.ID, what).text == how        

    def method_by_CSS_SELECTOR_click(self,what,wait_time=130000):
        logger.info('Click by_CSS_SELECTOR:{0} '.format(what))
        WebDriverWait(self.driver, wait_time).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, what)))
        self.driver.find_element(By.CSS_SELECTOR, what).click()