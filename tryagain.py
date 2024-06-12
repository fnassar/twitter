from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time

# Get the targeted data stockSymbols in no_of_mentions and username.


def account_web_scraper(account_url, ticker, driver):
    try:
        driver.maximize_window()
        driver.get(account_url)
        time.sleep(20)

        username = driver.find_element(
            By.XPATH, ("//div[@data-testid='UserName']")).text.split("\n")[1]
        stock_symbols = driver.find_elements(
            By.XPATH, ("//span[@class='r-18u37iz']"))
        No_of_mentions = 0
        for symbol in stock_symbols:
            if ticker == symbol.text.upper():
                No_of_mentions += 1
    except (WebDriverException, TimeoutException) as e:
        print(f"failed to scraping the profile as {e}.")

    return [No_of_mentions, username]


'''
    Funtion to display the scraped data.
'''


def display_web_scraper(accounts_urls, ticker, time_interval):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    while 1:
        for url in accounts_urls:
            mentioned, username = account_web_scraper(url, ticker, driver)
            print(f"'{ticker}' was mentioned '{mentioned}'times in the last '{
                  time_interval}'minutes in account'{username}'. ")
        print(f"next scraping session in '{time_interval}'minutes")
        time.sleep(time_interval * 60)


if __name__ == '__main__':
    twitter_accounts = [
        "https://twitter.com/Mr_Derivatives",
        "https://twitter.com/warrior_0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades",
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox"
    ]
    ticker = input(
        "Enter the stock symbol to Scrap(e.g. $TSLA, $AAPL, $SPY,etc..): ")
    interval_time_in_minutes = 15
    display_web_scraper(twitter_accounts, ticker, interval_time_in_minutes)
