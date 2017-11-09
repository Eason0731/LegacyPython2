import os
from selenium import webdriver
import time

def IE():
    if os.name == 'nt':
        IEDriverFile = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir,os.path.pardir,'Drivers','IEDriverServer.exe'))
        #IEDriverFile =  os.path.join(os.path.abspath('..'),os.path.abspath('..'),os.path.abspath('..'),'Drivers','IEDriverServer.exe')
        os.environ['webdriver.ie.driver'] = IEDriverFile
        driver = webdriver.Ie(IEDriverFile)
        driver.maximize_window()
    else:
        print "IE Browser cannot be ran on non-Windows os."
    return driver

def Chrome():
    if os.name == 'nt':
        ChromeDrvier = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir,os.path.pardir,'Drivers','chromedriver.exe'))
        #ChromeDrvier = os.path.join(os.path.abspath('..'),'Drivers','chromedriver.exe')
    elif os.name == 'posix':
        ChromeDrvier = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir,os.path.pardir,'Drivers','chromedriver'))
        #ChromeDrvier = os.path.join(os.path.abspath('..'),'Drivers','chromedriver')
    os.environ['webdriver.chrome.driver'] = ChromeDrvier
    driver = webdriver.Chrome(ChromeDrvier)
    driver.maximize_window()
    return driver

def FireFox():
    if os.name == 'nt':
        FireFoxDriver = 'C:\Program Files\Mozilla Firefox'
        os.environ['PATH'] = FireFoxDriver
    elif os.name == 'posix':
        FireFoxDriver = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir,os.path.pardir,'Drivers','geckodriver'))
        #FireFoxDriver = os.path.join(os.path.abspath('..'),'Drivers','geckodriver')
        os.environ['webdriver.gecko.driver'] = FireFoxDriver
    driver = webdriver.Firefox(FireFoxDriver)
    driver.maximize_window()
    return driver

