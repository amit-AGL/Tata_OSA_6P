# from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pymysql
import time
import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time



def Chrome_Driver():
	try:
	    chrome_options = Options()
	    chrome_options = webdriver.ChromeOptions()
	    # chrome_options.add_argument('--headless')
	    chrome_options.add_argument('--no-sandbox')
	    chrome_options.add_argument('--start-maximized')
	    # chrome_options.add_argument('--incognito')
	    driver = webdriver.Chrome(options=chrome_options)
	except Exception as e:
	    print(e)
	else:
		# cookies and
		return driver



def main():
    driver = Chrome_Driver()
    driver.get('https://www.1mg.com/otc/kapiva-weight-wise-foods-himalayan-apple-cider-vinegar-acv-for-hunger-pangs-weight-management-otc411590')

if __name__ == "__main__":
	main()
