# coding:utf-8
import os
from selenium import webdriver 
import time
import sys
import platform

def GetIE():
    if platform.system() == 'Windows':
        IEdriver = os.path.join(os.path.abspath('.'),'Drivers','IEDriverServer.exe') #Use relative path to get the path of IEDriverServer
        os.environ["webdriver.ie.driver"] = IEdriver #Set a system environment for ie browser then load IEDriverServer file path
        driver = webdriver.Ie(IEdriver)# Lanuch IE browser
        RunSogou(driver,sys._getframe().f_code.co_name[3:])
    else:
        print "IE cannot be ran on non-Windows OS"
    
def GetChrome():
    if platform.system() == 'Windows':
        ChromeDriver = os.path.join(os.path.abspath('.'),'Drivers','ChromeDriver.exe')  
    elif platform.system() == 'Darwin':
        ChromeDriver = os.path.join(os.path.abspath('.'),'Drivers','ChromeDriver')
    os.environ['webdriver.chrome.driver'] = ChromeDriver
    driver = webdriver.Chrome(ChromeDriver)
    RunSogou(driver,sys._getframe().f_code.co_name[3:])

def GetFireFox():
    if platform.system() == 'Windows':
        FireFox = 'C:\Program Files (x86)\Mozilla Firefox'
        os.environ['path'] = FireFox #Should add firefox browser to PATH environment for additional
        #Should copy geckodriver.exe to C:\Program Files (x86)\Mozilla Firefox
        driver = webdriver.Firefox()
    elif platform.system() == 'Darwin':
        GeckoDriver = os.path.join(os.path.abspath('.'),'Drivers','geckodriver')
        os.environ['webdriver.gecko.driver'] = GeckoDriver
        driver = webdriver.Firefox(GeckoDriver)
    RunSogou(driver,sys._getframe().f_code.co_name[3:])

def RunSogou(driver,browser):
    driver.maximize_window() #Maxmize the IE browser
    # Open sogou website then wait for 3 seconds
    driver.get("http://www.sogou.com")
    time.sleep(3)
    #Store a content then find searchbox and button on website
    SearchBox = driver.find_element_by_id("query")
    SearchButton = driver.find_element_by_id("stb")
    time.sleep(3)
    #Input the content and click searchbutton on website
    SearchBox.send_keys(browser)
    time.sleep(3)
    SearchButton.click()
    time.sleep(3)
    #To check the titile is right
    if browser in driver.title:
        print "Title of search page is right!"
        print "Pass: " + browser
    else:
        print "Current title name is " + driver.title

    if browser + u' - 搜狗搜索' == driver.title: #Should add a 'u' before Chinese string
        print "Title of search page is right!"
    else:
        print "Current title name is " + driver.title

    try:
        assert browser + u' - 搜狗搜索' in driver.title
        print "Title of search page is right!"
    except Exception,e:
        print e
        print "Current title name is " + driver.title
    
    driver.quit() #Quit the browser

if __name__ == '__main__':
    GetIE()
    GetChrome()
    GetFireFox()
