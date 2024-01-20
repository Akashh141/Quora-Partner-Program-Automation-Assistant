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
    print("Timeout: Login button not found or not clickable")

WebDriverWait(driver, 10).until(EC.url_matches("https://www.quora.com/"))

def add_questions():
    time.sleep(6)
    add_question_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add question']")))
    add_question_button.click()

def placeholdeer():
    try:
        placeholder = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@class, 'q-text-area') and contains(@class, 'qu-fontSize--large') and contains(@class, 'qu-lineHeight--regular') and contains(@class, 'TextInput___StyledTextArea-sc-9srrla-1') and contains(@class, 'idHrmV')]")))
    except TimeoutException:
        print("Timeout: Placeholder not found within 10 seconds. Reloading the page...")
        driver.refresh()
        add_questions()
        placeholder = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@class, 'q-text-area') and contains(@class, 'qu-fontSize--large') and contains(@class, 'qu-lineHeight--regular') and contains(@class, 'TextInput___StyledTextArea-sc-9srrla-1') and contains(@class, 'idHrmV')]")))

    with open('questions.txt', 'r+') as f:
        lines = f.readlines()
        if lines:
            first_line = lines.pop(0)
            f.seek(0)
            f.truncate()
            f.writelines(lines)
            placeholder.send_keys(first_line.strip())

def submit_questions():
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".q-click-wrapper.qu-active--textDecoration--none.qu-focus--textDecoration--none.qu-borderRadius--pill.qu-alignItems--center.qu-justifyContent--center.qu-whiteSpace--nowrap.qu-userSelect--none.qu-display--inline-flex.qu-bg--blue.qu-tapHighlight--white.qu-textAlign--center.qu-cursor--pointer.qu-hover--textDecoration--none.ClickWrapper___StyledClickWrapperBox-zoqi4f-0.iyYUZT.base___StyledClickWrapper-lx6eke-1.hIqLpn.puppeteer_test_modal_submit")))
    submit_button.click()

    use_suggestion_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/button')))
    use_suggestion_button.click()

    view_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/button')))
    view_question.click()

    driver.refresh()


    WebDriverWait(driver, 10).until(EC.url_matches("https://www.quora.com/"))

def repeat():
    add_questions()
    placeholdeer()
    submit_questions()