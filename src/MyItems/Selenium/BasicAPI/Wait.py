# coding:utf-8
import os
import time
import Getbrowser
import sys
from selenium.webdriver.support.ui import WebDriverWait #Need to import package WebDriverWait

def Wait(): #8
    driver = Getbrowser.Chrome()
    URL = 'http://www.baidu.com'
    driver.get(URL)
    SearchBox = WebDriverWait(driver, 10).until(lambda driver :  driver.find_element_by_id('kw')) # Use WebDriverWait to wait 10 seconds
    SearchBox.send_keys("WebDriverWait")
    
    driver.implicitly_wait(30) #implicitly wait for 30 seconds
    driver.find_element_by_id('su').click()

    time.sleep(5) # wait for 5 seconds
    driver.quit()
    
if __name__ == '__main__':
    Wait()
