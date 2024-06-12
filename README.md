# TWITTER SCRAPER
This is a simple Twitter scraper that uses the Twitter API to scrape tweets from a user's timeline. The scraper is written in Python and uses the Tweepy library to interact with the Twitter API.
### INSTALL: (required libraries)
- selenium

### NOTICE:
- make sure to login to your twitter account when prompted on the terminal then press `Enter` to continue
- the scraper will scrape then scrape the tweets from all user timelines
- if you want to stop the program, press `Ctrl + C` on the terminal window.

### USAGE:
- run the program by typing `python twitter_scraper.py` on the terminal
- default time interval is 15 minutes if you want to change it
    - pass `--time <>` argument to change time in minutes
    - pass `--unit h` to change time interval from minutes to hours (default is minutes if no arg passed)
