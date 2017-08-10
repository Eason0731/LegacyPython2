# coding:utf-8
import os
import time
import Getbrowser
import sys
from selenium.webdriver.support.ui import WebDriverWait #Need to import package WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains #Need to import package ActionChains

def UseJavaScriptOnSogou(): #15.38
    driver = Getbrowser.Chrome()
    URL = 'http://www.sogou.com'
    driver.get(URL)
    Content = 'Hello Selenium'
    time.sleep(3)
    
    TitleName = driver.execute_script('return document.title')
    if u'搜狗搜索引擎 - 上网从搜狗开始' == TitleName:
        print "Title name is correct!"
    else:
        print "Current title name is " + TitleName

    SearchBox = driver.find_element_by_id('query')
    SearchButton = driver.find_element_by_id('stb')

    driver.execute_script('arguments[0].value = "'+ Content + '"',SearchBox) #Use js to input words on SearchBox .value = send_keys
    time.sleep(2)

    driver.execute_script('arguments[0].click()',SearchButton) #Click the button
    time.sleep(2)

    TitleName2 = driver.execute_script('return document.title')
    if Content + u' - 搜狗搜索' == TitleName2:
        print "Title name of search is correct!"
    else:
        print "Current title name is " + TitleName2
    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
   UseJavaScriptOnSogou()
