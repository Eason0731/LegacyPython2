# coding:utf-8
import os
from selenium import webdriver 
import time 

IEdriver = os.path.join(os.path.abspath('.'),'Drivers','IEDriverServer.exe')
os.environ["webdriver.ie.driver"] = IEdriver 
driver = webdriver.Ie(IEdriver)
driver.maximize_window()

driver.get("http://www.sogou.com")
time.sleep(3)
Content = "Hello Selenium"
SearchBox = driver.find_element_by_id("query")
SearchButton = driver.find_element_by_id("stb")
time.sleep(3)

SearchBox.send_keys(Content)
time.sleep(3)
SearchButton.click()
time.sleep(3)

if Content in driver.title:
    print "Title of search page is right!"
else:
    print "Current title name is " + driver.title

driver.quit()
