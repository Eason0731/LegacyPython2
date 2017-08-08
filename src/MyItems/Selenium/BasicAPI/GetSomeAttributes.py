# coding:utf-8
import os
import time
import Getbrowser
import sys

def GetSomeAttributes(): #5
    driver = Getbrowser.Chrome()
    URL = 'http://www.baidu.com'
    driver.get(URL)
    print driver.find_element_by_id('kw').size # get the size of search box
    time.sleep(2)
    print driver.find_element_by_id('jgwab').text # get the text on this link
    time.sleep(2)
    print driver.find_element_by_id('su').get_attribute('type') # get the type of search button
    time.sleep(2)
    print driver.find_element_by_name('wd').is_displayed() #to judge whether this element is display or not
    driver.quit()
    
if __name__ == '__main__':
    GetSomeAttributes()
