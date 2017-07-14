import os
from selenium import webdriver 
import time

IEdriver = "D:\John's Code Project\MySeleniumCases\Drivers\IEDriverServer.exe"
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

try:
    assert Content in driver.title
    print "Pass!"
except Exception as e:
    print e

print driver.title

driver.quit()
