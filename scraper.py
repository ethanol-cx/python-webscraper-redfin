import requests
from house import House
from random import uniform
import time
from bs4 import BeautifulSoup
from datetime import datetime


class Scraper():
    max_iter = 15
    user_agent_header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

    def __init__(self):
        self.url = 'https://www.redfin.com/city/11203/CA/Los-Angeles/'
        self.session = requests.Session()
        self.houses = dict()  # id to house

    def random_sleep(self):
        time.sleep(uniform(0, 1))

    def parse_status_dates(self, statusDate):
        splitArray = statusDate.split(' ')
        return [' '.join(splitArray[:-3]), datetime.strptime(' '.join(splitArray[-3:]), '%b %d, %Y')]

    def get_page_soup(self, url):
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

    def search_houses(self, query, center):
        viewport = ''
        for loc in center:
            viewport += str(loc)
            viewport += ':'
        viewport = viewport[:-1]
        url = self.url + \
            '/filter/include={},viewport={}'.format(query, viewport)
        soup = self.get_page_soup(url)
        # first finds the number of pages in the search list
        numPages = int(soup.find_all('span', attrs={'class': 'pageText'})[
            0].text.split()[-1])
        for i in range(numPages):
            if i != 0:
                soup = self.get_page_soup(url + '/page-{}'.format(i+1))
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
            for j in range(len(ids)):
                id = ids[j]
                address = addresses[j]
                [status, date] = statusDates[j]
                price = prices[j]
                [bed, bath, size] = stats[j]
                self.houses[id] = (House(id=id, streetAddress=address, status=status, date=date,
                                         lastListedPrice=price, numBed=bed, numBath=bath, size=size))
                print(id, address, status, date, price, bed, bath, size)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.search_houses('sold-6mo',
                          [34.02667, 34.00418, -118.27654, -118.30448])
