# coding:utf-8
import os
import time
import Getbrowser
import sys
from selenium.webdriver.support.ui import WebDriverWait #Need to import package WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains #Need to import package ActionChains

def UploadFiles(): #15
    driver = Getbrowser.Chrome()
    URL = os.path.join(os.path.abspath('.'),'Html','upload_file.html')
    driver.get(URL)
    
    driver.find_element_by_name('file').send_keys('C:\123.txt') #Use send_keys to upload file
    time.sleep(3)
    driver.quit()
    
if __name__ == '__main__':
    UploadFiles()
