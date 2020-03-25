from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import subprocess

driver = webdriver.Chrome(executable_path="/home/student/DM_assignment/chromedriver_linux64/chromedriver")

driver.set_page_load_timeout(30)
driver.maximize_window()
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

fileName = "goldprice_" + time.strftime("%d-%b-%Y_%H-%M-%S", time.localtime()) + ".csv"

resultFile = open(fileName, 'w')

resultFile.write("Date_D,Price,Open,High,Low,Volume,Change_%\n")

column = 1
for data in tableData:
    if column != 7:
        resultFile.write((data.text).replace(',', '') + ", ")
        column = column + 1
    else:
        resultFile.write(data.text + "\n")
        column = 1

resultFile.close()

def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err 

(ret, out, err)= run_cmd(['hdfs', 'dfs', '-put', '/home/student/DM_assignment/' + fileName, '/user/hdfs/DM'])

driver.close()

