# Twitch Data Scraper v7
Twitch Data Scraper including Instagram and Youtube Data

# Features of Twitch Data Scraper:
- Get streamer data & chat data for 6 most recommended channels a list of the most popular games.
- Converts all data into a .json file and creates a descriptives .csv file for all chat information
- Instagram followers are added at start and end.
- Youtube subscribers are added at start and end.

# How to use Twitch Data Scraper v7

Before using the scraper make sure you have done the following:

1. Install the following packages:
- pip install selenium
- pip install webdriver-manager
- pip install beautifulsoup4
- pip install requests

2. Set your screen resolution to 2550x1440 to make sure Selenium can find all web elements.

3. Run the scraper, enter your start game int(number between 0 and 6), enter your end game int(number between 0 and 6) and enter the amount of minutes to scrape.

When done, the scraper will provide you with a .json file containing all data and a .csv file which provides descriptives about the chat.
