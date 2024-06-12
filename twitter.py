# from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


target_urls = [
    "https://x.com/Mr_Derivatives",
    "https://x.com/warrior_0719",
    "https://x.com/ChartingProdigy",
    "https://x.com/allstarcharts",
    "https://x.com/yuriymatso",
    "https://x.com/TriggerTrades",
    "https://x.com/AdamMancini4",
    "https://x.com/CordovaTrades",
    "https://x.com/Barchart",
    "https://x.com/RoyLMattox"]


def get_tweets(target_url, driver):
    driver.maximize_window()
    driver.get(target_url)
    # input("Log in manually in the opened browser window and press Enter here...")
    time.sleep(10)

    tweets = driver.find_elements(
        By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")
    return tweets


def get_stock_count(tweet):
    reg = r"\$[A-Z]+"

    time = tweet.find_element(By.CSS_SELECTOR, "time")
    print(time.text)
    # print(tweet)
    try:
        ttext = "14h"
        # if (time.text).find("h") != -1 and int(time.text[:2]) <=15:
        if (ttext).find("h") != -1 and int(ttext[:2]) <= 15:
            # print("Tweeted less than 15 minute ago")
            text = tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")
            # print(text.text)
            stock = (re.findall(reg, text.text))
            return stock
    except Exception as e:
        return []

    return []


if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Chrome()
    found = {}
    for target_url in target_urls:
        print(target_url.split("/")[-1])
        found = {}
        tweets = get_tweets(target_url, driver)
        for tweet in tweets:
            labels = get_stock_count(tweet)
            for label in labels:
                if label in found:
                    found[label] += 1
                else:
                    found[label] = 1
        print(found)
    driver.quit()
