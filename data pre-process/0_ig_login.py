# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 00:32:12 2024

@author: shama
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from DrissionPage import ChromiumPage, errors
import requests
import os



IGID = 's1100611_'
IGpassword = 'yzu1100611'
account='tougeyuzo'

# 自動下載ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())

# 關閉通知提醒
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
# 以下三個註解打開，瀏覽器就不會開啟
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs",prefs)

# 開啟瀏覽器
driver = webdriver.Chrome(service=service, options=chrome_options)
time.sleep(5)

####### 開始操作 輸入帳號密碼登入 到IG首頁 ####### 
driver.get("https://www.instagram.com/")
time.sleep(1)
assert "Instagram" in driver.title

time.sleep(3)
driver.find_element(By.XPATH, value='//*[@name="username"]').send_keys(IGID) #輸入登入帳號
time.sleep(1)
driver.find_element(By.XPATH, value='//*[@name="password"]').send_keys(IGpassword) # 輸入登入密碼
time.sleep(3)

driver.find_element(By.XPATH, value='//*[@type="submit"]').click()
time.sleep(3)

print(driver.find_elements(By.XPATH, value='//*[@type="button"]')[0].text)
# 瀏覽器會問是否儲存
driver.find_elements(By.XPATH, value='//*[@type="button"]')[0].click() 
time.sleep(3)

driver.find_elements(By.XPATH, value='//*[@role="img"]')[2].click() 
time.sleep(3)

#輸入要查的帳號
driver.find_element(By.XPATH, value='//*[@type="text"]').send_keys(account) 
time.sleep(3)
#點選要查的帳號
driver.find_element(By.XPATH, value='//*[@tabindex="0"]').click() 
time.sleep(3)