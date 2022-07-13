
from time import sleep
import random
import os
from fake_useragent import UserAgent
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN
from datetime import datetime
from bs4 import BeautifulSoup
from collections import OrderedDict
import sqlite3
import requests
import urllib
import re
import configparser
from requests_html import AsyncHTMLSession
from requests_html import HTMLSession

dirname = os.path.dirname(__file__)

class AdvertaisementNotAvailableError(Exception):
    pass

class RequestsError(Exception):
    pass



import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

# https://stackoverflow.com/questions/28330317/print-timestamp-for-logging-in-python
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    filename='./log/mining_content_log.log', level=logging.DEBUG)

parser = configparser.ConfigParser()
parser.read("./config/scrape.ini")
opt = parser.get('DEFAULT', 'mining_method')
headers = ''


def innerHTML(element):
    """Returns the inner HTML of an element as a UTF-8 encoded bytestring"""
    return element.encode_contents()


def get_analysis_data():
    driver.find_element(By.XPATH, "//button[@id='legend_show_data ui-btn ui-shadow ui-corner-all']").click()
    sleep(5)


def get_title():
    try:
        t = driver.find_element(By.XPATH, "//div[@id='div_datatable_txt']").get_attribute('innerHTML')
        return t
    except Exception as e:
        print(f'errror in start download as {e}')


def get_slider_start_end():
    try:
        slider = driver.find_element(By.XPATH, "//div[@class='ui-slider-track ui-shadow-inset ui-bar-inherit ui-corner-all ui-mini']")
        elem = slider.find_elements(By.XPATH, "//div[@class='sliderTickmarks']")
        for i in elem:
            print(i)

    except Exception as e:
        print(f'errror in start download as {e}')

def start_download():
    try:
        driver.find_element(By.XPATH, "//div[@id='div_datatable_but_download_csv']").click()
        #driver.find_element(By.XPATH, "//div[@id='div_datatable_but_download']").click()
    except Exception as e:
        print(f'errror in start download as {e}')



driver.find_element(By.XPATH, "//div[@data-theme_short='arbeitsmarkt']").click()



driver.find_element(By.XPATH, "//div[@data-theme_short='oeff_finanz_steuern']").click()


url ='https://statistik.at/atlas/'
for i in range(0,1):
    driver.get(url)
    driver.find_element(By.XPATH, "//div[@data-theme_short='bevoelkerung']").click()
    print(get_title())
    get_slider_start_end()
    get_analysis_data()
