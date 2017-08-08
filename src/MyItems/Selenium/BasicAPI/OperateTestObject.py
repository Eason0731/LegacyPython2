# coding:utf-8
import os
import time
import Getbrowser
import sys

def OperateTestObject(): #4
    driver = Getbrowser.Chrome()
    URL = 'http://www.baidu.com'
    Content = 'Hello Selenium'
    driver.get(URL)
    driver.find_element_by_name('wd').send_keys(Content) #send_keys that can input words
    time.sleep(2)
    driver.find_element_by_name('wd').clear() # clear can delete all the content
    time.sleep(2)
    driver.find_element_by_name('wd').send_keys(Content)
    time.sleep(2)
    driver.find_element_by_id('su').click() #click the button
    time.sleep(2)
    driver.back()
    driver.find_element_by_name('wd').send_keys(Content)
    driver.find_element_by_id('su').submit() #submit the content
    time.sleep(2)
    if Content + u'_百度搜索' in driver.title:
        print "Pass"
    else:
        print "Current page title is: " + driver.title
    driver.quit()
    
if __name__ == '__main__':
    OperateTestObject()
