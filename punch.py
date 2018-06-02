from selenium import webdriver
import time, os
 
path = os.getcwd() + '/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(chrome_options=options, executable_path=path)
driver.get('https://punchsubs.net/principal')


