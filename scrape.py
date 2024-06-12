# First, open the terminal and run: 'pip install ntscraper'
from ntscraper import Nitter
from datetime import datetime, timedelta
import re
import argparse
import time

# time_diff = 15

# regex $ then char A-Z
reg = r"\$[A-Z]+"


def check_tweets(username, scraper, timee):
    # check if user(username) has tweets mentioning stocks
    date = datetime.now()  # curent time
    date_15 = date - timedelta(minutes=timee)  # get time difference to use
    # get last 10 tweets from user
    tweets = scraper.get_tweets(username, mode='user', number=10)
    n = {}
    i = 0
    for tweet in tweets['tweets']:
        tweet_date = datetime.strptime(
            tweet['date'], "%b %d, %Y · %I:%M %p UTC")
        stocks = re.findall(reg, tweet['text'])
        print(tweet['date'], tweet['text'][:50])
        # check if user has a tweet that has a stock in the time interval specified
        if tweet_date >= date_15 and tweet_date <= date:
            for stock in stocks:
                if stock in n:
                    n[stock] += 1
                else:
                    n[stock] = 1
        elif (i > 1):
            break
        break

        i += 1
    return n


def displayAll(user_data, time):
    # this display function just prints the collected data
    stocks = {}
    print(user_data)
    for user in user_data:  # prints data for each user
        print("----------\n", user, ": ")
        for stock in user_data[user]:
            print("mentioned '", stock, "':",
                  user_data[user][stock], "times in the last ", time, " minutes.")
            if stock in stocks:
                stocks[stock] += user_data[user][stock]
            else:
                stocks[stock] = user_data[user][stock]

    # print stocks total data collected for all 10 users
    print("----------\nTotal: ")
    for stock in stocks:
        print("'", stock, "' was mentioned",
              stocks[stock], "times in the last ", time, " minutes.")


if __name__ == '__main__':
    # get desired time for intervals to check
    parser = argparse.ArgumentParser()
    parser.add_argument('--time', type=int,
                        help='time between checks in minutes', default='15')
    args = parser.parse_args()

    user_data = dict()
    urls = [
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

    scraper = Nitter()
    while True:
        # repeat every x minutes
        user_data = {}
        for url in urls:
            username = url.split("/")[-1]
            user_data[username] = check_tweets(username, scraper, args.time)
        displayAll(user_data, args.time)

        print("Will check again in", args.time, "minutes")
        time.sleep(10)  # args.time*60)
        # if KeyboardInterrupt:
        break
    exit(0)
