from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scraper import Scraper
import time
import pandas as pd
if __name__ == '__main__':
    # the periods options that we could choose from
    # for example: 1wk means to search for the houses that were sold in last week
    periods = ['1wk', '1mo', '3mo', '6mo', '1yr', '2yr', '3yr']

    # Getting input from the console.
    periodIdx = input(
        'How far back in time do you want to search? (Hit enter if you want default option: 3 month) \n 1: 1 week \n 2: 1 month \n 3: 3 months \n 4: 6 months \n 5: 1 year \n 6: 2 years \n 7: 3 years \n')
    if periodIdx == '':
        periodIdx = 3

   # create the scraper
    scraper = Scraper()

    # scrape the information from the page
    scraper.search_houses('sold-{}'.format(periods[int(periodIdx) - 1]))
    scraper.houses.to_csv(
        'LA-sold-{}.csv'.format(periods[int(periodIdx) - 1]), index=False)
