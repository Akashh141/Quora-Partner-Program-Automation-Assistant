import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

driver_path = r'C:\Users\MITT\quora\chromedriver.exe'
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.headless = True
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.quora.com/")

with open('credentials.json') as f:
    credentials = json.load(f)
    email = credentials['email']
    password = credentials['password']

email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(email)

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(password)

try:
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".q-click-wrapper.qu-active--textDecoration--none.qu-focus--textDecoration--none.qu-borderRadius--pill.qu-alignItems--center.qu-justifyContent--center.qu-whiteSpace--nowrap.qu-userSelect--none.qu-display--inline-flex.qu-bg--blue.qu-tapHighlight--white.qu-textAlign--center.qu-cursor--pointer.qu-hover--textDecoration--none")))
    login_button.click()
except TimeoutException:
    print("Timeout: Login button not found or not clickablee")

WebDriverWait(driver, 10).until(EC.url_matches("https://www.quora.com/"))