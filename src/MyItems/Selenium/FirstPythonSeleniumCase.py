import os
from selenium import webdriver 
import time

IEdriver = "D:\John's Code Project\MySeleniumCases\Drivers\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = IEdriver 


driver = webdriver.Ie(IEdriver)

driver.get("http://www.sogou.com")
time.sleep(3)

print driver.title

driver.quit()
