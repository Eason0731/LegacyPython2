# coding:utf-8
import os
from selenium import webdriver 
import time

IEdriver = os.path.join(os.path.abspath('.'),'Drivers','IEDriverServer.exe') #Use relative path to get the path of IEDriverServer
os.environ["webdriver.ie.driver"] = IEdriver #Set a system environment for ie browser then load IEDriverServer file path
driver = webdriver.Ie(IEdriver)# Lanuch IE browser
driver.maximize_window() #Maxmize the IE browser

# Open sogou website then wait for 3 seconds
driver.get("http://www.sogou.com")
time.sleep(3)

#Store a content then find searchbox and button on website
Content = "Hello Selenium"
SearchBox = driver.find_element_by_id("query")
SearchButton = driver.find_element_by_id("stb")
time.sleep(3)

#Input the content and click searchbutton on website
SearchBox.send_keys(Content)
time.sleep(3)
SearchButton.click()
time.sleep(3)

print Content + u' - 搜狗搜索 '
#To check the titile is right
if Content in driver.title:
    print "Title of search page is right!"
else:
    print "Current title name is " + driver.title

if Content + u' - 搜狗搜索' == driver.title: #Should add a 'u' before Chinese string
    print "Title of search page is right!"
else:
    print "Current title name is " + driver.title

try:
    assert Content + u' - 搜狗搜索' in driver.title
    print "Title of search page is right!"
except Exception,e:
    print e
    print "Current title name is " + driver.title
    
driver.quit() #Quit the browser


