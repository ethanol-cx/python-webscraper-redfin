# A simple webscraper for sold houses from Redfin.com


## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)


## Introduction

This tool is a simple webscraper that scrapes the following information of each house that has been sold for the past period of time: houseId, house address, house price, house status(should be all 'SOLD' or 'SOLD with Redfin' in this particular main.py usage), last listed price, number of bedrooms, number of bathrooms, size.

The information above is needed so that we could perform certain analysis on the data. For example, we could form a regression problem that given a house's address (could be either exact latitute, longitute or area code), number of bedrooms, number of bathrooms, size, it predicts the listed price of a house. In this case, these information is essential. If the main.py does not only focus on the sold houses, another example could be: given these stats of a house, predict whether a certain house could be sold within 3 month. The house address gives the accurate address of a house, so we could go through third-party API's such as google map API to get the latitute and longitute and visualize the list of data we have on the map. These examples show why I think the information above is important.

## Getting Started

1. Install [Python]()
2. Install all the packages listed in packages.txt. If you have [pip](https://pypi.org/project/pip/) installed, you could run `pip install -r packages.txt` to install all the packages.
3. Run main.py. The program will prompts for the past time period you want to search for sold houses. You could hit enter if you want to use the default setting. Even though the program has a sleeping mechanism to prevent being detected, here is a chance that the program is still detected as a robot. In this case, please pass the test manually and restart the program.

