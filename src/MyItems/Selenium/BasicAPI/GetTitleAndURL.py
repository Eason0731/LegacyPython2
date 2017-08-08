# coding:utf-8
import os
import time
import Getbrowser
import sys

def GetTitleAndURL():
    driver = Getbrowser.Chrome()
    driver.get('http://www.baidu.com')
    time.sleep(2)
    if u'百度一下，你就知道' in driver.title: # "driver.title" to get the page title name on current page
        print "Pass: " + sys._getframe().f_code.co_name
    else:
        print "Current page title is " + driver.title
    print driver.current_url # "current_url" to get the page title URL address on current page
    driver.quit()
    
if __name__ == '__main__':
    GetTitleAndURL()
