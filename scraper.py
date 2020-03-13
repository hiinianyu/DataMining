from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome(executable_path="C:\\Users\\yy932\\OneDrive\\Desktop\\DS\\data mining\\Assignment\\drivers\\chromedriver.exe")

driver.set_page_load_timeout(30)
driver.get("https://www.investing.com/commodities/gold-historical-data")

for i in range(5):
    dateRangeElements = driver.find_elements_by_xpath("//div[@id='widgetFieldDateRange']")
    
    if len(dateRangeElements) > 0:
        dateRangeElements[0].click()
        break
    else:
        print(str(i + 1) + " trial, can't find element")
    
    time.sleep(1)
    i = i + 1

elementStartDate = driver.find_element_by_xpath("//input[@id='startDate']")
elementStartDate.clear()
elementStartDate.send_keys("01/01/2019")

driver.find_element_by_xpath("//a[@id='applyBtn']").click()
time.sleep(3)

tableData = driver.find_elements_by_xpath("//table[@id='curr_table']/tbody/tr/td")

resultFile = open("goldprice_" + time.strftime("%d-%b-%Y %H-%M-%S", time.localtime()) + ".csv", 'w')

resultFile.write("Date,Price,Open,High,Low,Volume,Change %\n")

column = 1
for data in tableData:
    if column != 7:
        resultFile.write((data.text).replace(',', '') + ", ")
        column = column + 1
    else:
        resultFile.write(data.text + "\n")
        column = 1

resultFile.close()

driver.close()