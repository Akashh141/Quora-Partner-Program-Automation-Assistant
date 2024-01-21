import json
import praw
import os
from pytrends.request import TrendReq
import datetime
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

driver_path = r'C:\Users\MITT\quora\chromedriver.exe'
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.headless = True
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.quora.com/")

import praw
from pytrends.request import TrendReq
import datetime
import random


def fetch_questions_and_save_to_file():
    def get_random_keywords(retries=3):
        for attempt in range(retries):
            try:
                # Connect to Google Trends
                pytrends = TrendReq(hl='en-US', tz=360)

                # Get the current year
                current_year = datetime.datetime.now().year

                # Randomize the year for fetching top charts within the range of 2004 to the current year
                random_year = random.randint(2004, current_year)

                # Fetch top keywords for the random year
                top_keywords_random_year = pytrends.top_charts(date=random_year, hl='en-US', tz=300, geo='GLOBAL')

                # Extract titles from top keywords
                keyword_titles = top_keywords_random_year['title'].tolist()

                return keyword_titles

            except Exception as e:
                print(f"Attempt {attempt + 1} failed:", e)
                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(3)
                else:
                    print("Maximum retries exceeded.")
                    return []

    def scrape_reddit_questions_for_keywords(keywords, subreddits, num_questions_per_keyword=10):
        # Reddit API credentials
        reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                             client_secret='YOUR_CLIENT_SECRET',
                             user_agent='my-app YOUR_USERNAME')

        # Search for questions related to each keyword
        all_questions = []

        for keyword in keywords:
            for subreddit in subreddits:
                print(f"Searching for questions related to '{keyword}' in subreddit '{subreddit}'...")
                # Search for questions related to the keyword in the specified subreddit
                search_results = reddit.subreddit(subreddit).search(keyword, limit=num_questions_per_keyword,
                                                                    sort='relevance')

                # Extract titles of the questions
                questions = [submission.title for submission in search_results if submission.title.endswith('?')]

                print(f"Found {len(questions)} questions.")
                all_questions.extend(questions)

        return all_questions

    if __name__ == "__main__":
        # Check if the previous questions.txt file exists
        if os.path.exists('questions.txt'):
            delete_previous = input(
                "A previous questions.txt file exists. Do you want to delete it? (yes/no): ").lower()
            if delete_previous == 'yes':
                os.remove('questions.txt')
                print("Previous questions.txt file deleted.")
            else:
                print("Exiting the program.")
                exit()


        keywords = get_random_keywords()

        if keywords:
            # Specify subreddits for Q&A
            subreddits = ['AskReddit', 'AskScience', 'AskHistorians']

            # Fetch 10 questions for each keyword from specified subreddits
            num_questions_per_keyword = 10
            questions = scrape_reddit_questions_for_keywords(keywords, subreddits, num_questions_per_keyword)

            # Write questions to a file
            with open('questions.txt', 'w') as file:
                for question in questions:
                    file.write(question + '\n')

            print("Questions have been saved to 'questions.txt' file.")
        else:
            print("Failed to fetch keywords from Google Trends. Please check your internet connection and try again.")



fetch_questions_and_save_to_file()

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

# Repeat the process until there are no more questions
while True:
    repeat()
    with open('questions.txt') as f:
        if not f.readlines():
            break


input("Press any key to exit...")

# Close the WebDriver session
driver.quit()
