import requests
from house import House
from random import uniform
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


class Scraper():
    """
        Scraper class contains the basic information that is needed for scraping.
        Each Scraper instance should contains its own session as well as the houses that it has obtained from the webpage.
    """

    # max_iter defines the max number of reqeust attempts. If the max number of attempt is reached, the requests might be blocked.
    max_iter = 15
    user_agent_header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

    def __init__(self, url='https://www.redfin.com/city/11203/CA/Los-Angeles/'):
        """
        Constructor of the Scraper class
        Keyword Arguments:
            url {str} -- [The url corresponding to the city that user chooses from the beginning] (default: {'https://www.redfin.com/city/11203/CA/Los-Angeles/'})
        """
        self.url = url
        self.session = requests.Session()
        # self.houses = dict()  # id to house
        self.houses = pd.DataFrame(columns=[
                                   'id', 'address', 'status', 'date', 'lastListedPrice', 'numBed', 'numBath', 'size'])

    def random_sleep(self):
        """
        Allows the program to sleep for random amount of time to avoid blocked by the site
        Raises:
            Exception -- If the provided url is not valid (HTTP 404) or the network condition is off, an exception will be thrown.
        Returns:
            None
        """
        time.sleep(uniform(0, 10))

    def parse_status_dates(self, statusDate):
        """
        Parses the status(i.e. 'SOLD, SOLD with Redfin, etc.') and the date from the statusDate string that is displayed on the site
        Arguments:
            statusDate {[str, str]} -- A list with two elements: status, date
        """
        splitArray = statusDate.split(' ')
        return [' '.join(splitArray[:-3]), datetime.strptime(' '.join(splitArray[-3:]), '%b %d, %Y')]

    def get_page_soup(self, url):
        """
        Given the url, it return the BeautifulSoup object containing the page source of that url.
        Arguments:
            url {str} -- the url linking to the page that the program is going to scrape
        """
        # sleep to avoid detection
        self.random_sleep()

        # repeat the request for max_iter times just to avoid package loss or network glitches
        for i in range(self.max_iter):
            self.random_sleep()
            resp = self.session.get(
                url, headers=self.user_agent_header, verify=False)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, 'html.parser')
            print('ERROR with status code {}'.format(resp))
            print('HTTP response body {}'.format(resp.text))
        raise Exception(
            'Request failed {} times. It is probably blocked.'.format(self.max_iter))
        return None

    def search_houses(self, query):
        """
        Given the query string (i.e. sold-6mo), we search the houses from Redfin.
        Arguments:
            query {str} -- a query string that acts as the filter of the search
        """
        url = self.url + \
            '/filter/include={}'.format(query)
        soup = self.get_page_soup(url)

        # first finds the number of pages in the search list
        numPages = int(soup.find_all('span', attrs={'class': 'pageText'})[
            0].text.split()[-1])
        # loop through every page of the search result
        for i in range(numPages):
            # if this is not the first iteration, go to the next page of the search results
            if i != 0:
                soup = self.get_page_soup(url + '/page-{}'.format(i+1))
                self.random_sleep()
            # get the corresponding information on the page
            try:
                ids = list(map(lambda tag: tag['href'].split('/')
                               [-1], soup.find_all('a', attrs={'class': 'cover-all'})))
                addresses = list(map(lambda tag: tag.text, soup.find_all(
                    'span', attrs={'data-rf-test-id': 'abp-streetLine'})))
                statusDates = list(map(lambda tag: self.parse_status_dates(tag.text), soup.find_all(
                    'span', attrs={'class': 'HomeSash font-weight-bold roundedCorners'})))
                prices = list(map(lambda tag: tag.text, soup.find_all(
                    'span', attrs={'class': 'homecardV2Price'})))
                stats = [list(map(lambda tag: tag.text, singleHouseStats))
                         for singleHouseStats in soup.find_all('div', attrs={'class': 'HomeStatsV2'})]
                print("Finished page {}/{} of the results".format(i+1, numPages))
            except:
                raise("Exception occurred when parsing the information from the page {}.The page might have been changed and the scraping script is probably not updated.".format(url))

            # loop through all information we obtained and store them as house objects
            for j in range(len(ids)):
                id = ids[j]
                if (j < len(addresses)):
                    address = addresses[j]
                if (j < len(statusDates)):
                    [status, date] = statusDates[j]
                if (j < len(prices)):
                    price = prices[j]
                if (j < len(stats)):
                    [bed, bath, size] = stats[j]
                # self.houses[id] = (House(id=id, streetAddress=address, status=status, date=date,
                #                          lastListedPrice=price, numBed=bed, numBath=bath, size=size))
                #
                # alternatively keep a dataframe
                self.houses = self.houses.append(
                    {'id': id, 'address': address, 'status': status, 'date': date, 'lastListedPrice': price, 'numBed': bed, 'numBath': bath, 'size': size}, ignore_index=True)
