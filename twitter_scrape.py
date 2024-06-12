from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse, re, time
from datetime import datetime, timedelta

# fatemaaaaa73187
def convert_to_datetime(time_str):
    result = None
    if time_str.endswith("h"):
        # Case: xh
        hours = int(time_str[:-1])
        delta = timedelta(hours=hours)
        result = datetime.now() + delta
    elif time_str.endswith("m"):
        # Case: xm
        minutes = int(time_str[:-1])
        delta = timedelta(minutes=minutes)
        result = datetime.now() + delta
    else:
        # Case: 01 Jun or 01 Jun 2023
        try:
            result = datetime.strptime(time_str, "%b %d")
        except ValueError:
            result = datetime.strptime(time_str, "%b %d, %Y")

    return result

def get_tweets(target_url, driver):
    # driver.maximize_window()
    driver.get(target_url)
    time.sleep(15)

    tweets = driver.find_elements(
        By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")
    # print("Tweets found for", target_url.split("/")[-1], "are", len(tweets))
    return tweets


def get_stock_count(tweet, time_int, unit):
    reg = r"\$[A-Z]+"
    try:
        time = tweet.find_element(By.CSS_SELECTOR, "time")
        time_time = convert_to_datetime(time.text)
        time_delta= datetime.now() - (timedelta(minutes=time_int) if unit=='m' else timedelta(hours=time_int))
        # if time time is closer to time now than time_delta
        if time_time > time_delta:
            text = tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")
            stock = (re.findall(reg, text.text))
            return stock
    except Exception as e:
        return []
    return []

def display(found, time, unit, user):
    print("Stocks mentioned in last '", time, "' minutes by '" if unit=='m' else "' hours by '", user, "' are:", end="")
    for key, value in found.items():
        print(key, ":", value, "times", end=" | ")
    print("\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--time', type=int,
                        help='time between checks in minutes', default='15')
    parser.add_argument('--unit', type=str,
                        help='time between checks in minutes', default='m')
    args = parser.parse_args()
    
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
    
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(options=options)


    # Open Twitter login page
    driver.get('https://twitter.com/login')

    input('Press Enter after you have logged in...')
    
    # Get the tweets
    found = {}
    i=0
    while True:
        for target_url in target_urls:
            user = (target_url.split("/")[-1])
            found = {}
            tweets = get_tweets(target_url, driver)
            for tweet in tweets:
                labels = get_stock_count(tweet, args.time, args.unit)
                for label in labels:
                    if label in found:
                        found[label] += 1
                    else:
                        found[label] = 1
                if i>10:
                    break
                i += 1
            display(found, args.time, args.unit, user)
            
        print("sleeping for",args.time,end="")
        if args.unit == 'm':
            print(" minutes")
            time.sleep(args.time*60)
        else:
            print(" hours")
            time.sleep(args.time*60*60)

        if KeyboardInterrupt:
            break
    driver.quit()

