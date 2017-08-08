# coding:utf-8
import os
import time
import Getbrowser
import sys

def GetSimpleElement(): #3
    driver = Getbrowser.Chrome()
    URL = 'http://www.baidu.com'
    driver.get(URL)
    time.sleep(2)
    driver.find_element_by_id('su') #find id element
    driver.find_element_by_name('wd') #find name element
    driver.find_element_by_link_text('贴吧') #find link text element
    driver.find_element_by_class_name('c-tips-container') #find class name element
    driver.find_element_by_xpath('//*[@id="kw"]') #find xpath element
    driver.find_element_by_tag_name('div') #find div element
    driver.find_element_by_partial_link_text('新') #find part of link text element
    driver.quit()
    
if __name__ == '__main__':
    GetSimpleElement()
