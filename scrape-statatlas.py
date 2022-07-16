
from time import sleep
from time import time
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
#from requests_html import AsyncHTMLSession
#from requests_html import HTMLSession

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
import configparser



dirname = os.path.dirname(__file__)


class RequestsError(Exception):
    pass


import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    filename='./log/log.log', level=logging.DEBUG)

#parser = configparser.ConfigParser()
#parser.read("./config/scrape.ini")
#opt = parser.get('DEFAULT', 'mining_method')




def make_driver():
    opt = Options()
    ua = UserAgent()
    path = f'{os.path.join(os.path.dirname(__file__))}\chromedriver.exe'
    opt.add_argument(f'user-agent={ua.random}')
    driver = webdriver.Chrome(service = Service(path), options=opt)
    return driver


def delete_cache(driver):
    # source: https://stackoverflow.com/questions/50456783/python-selenium-clear-the-cache-and-cookies-in-my-chrome-webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    driver.execute_script("window.open('');")
    sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    sleep(2)
    driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
    sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3) # send right combination
    actions.perform()
    sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER)
    actions.perform()
    sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def get_analysis_data(driver):
    try:
        sleep(1)
        driver.find_element(By.XPATH, "//button[@class='legend_show_data ui-btn ui-shadow ui-corner-all']").click()
        sleep(5)
    except Exception as e:
        print(f'Error in get analysis data: {e}')


def get_title(driver):
    try:
        t = driver.find_element(By.XPATH, "//div[@id='div_datatable_txt']").get_attribute('innerHTML')
        return t
    except Exception as e:
        print(f'errror in start download as {e}')


def get_slider_start_end(driver):
    try:
        slider = driver.find_elements(By.XPATH, "//div[@class='ui-slider-track ui-shadow-inset ui-bar-inherit ui-corner-all ui-mini']")[1]
        elem = slider.find_elements(By.XPATH, "//div[@class='sliderTickmarks']")
        mini = driver.find_element(By.XPATH, "//div[@id='div_sidebar_txt_slider_min']").get_attribute('innerHTML')
        maxi = driver.find_element(By.XPATH, "//div[@id='div_sidebar_txt_slider_max']").get_attribute('innerHTML')

        #while True:

        print(maxi)
        for i in elem:
            tmp = i.get_attribute('innerHTML')
            print(tmp)

    except Exception as e:
        print(f'Error in get_slider_start_end as {e}')


def start_download(driver):
    try:
        driver.find_element(By.XPATH, "//div[@id='div_datatable_but_download']").click()
        sleep(1)
        driver.find_element(By.XPATH, "//button[@id='div_datatable_but_download_csv']").click()
    except Exception as e:
        print(f'Error in start download as {e}')


# method to get the downloaded file name
def getDownLoadedFileName(driver, waitTime):
    """source: https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading"""
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    #endTime = time()+waitTime
    sleep(2)
    while True:
        try:
            # get downloaded percentage
            #downloadPercentage = driver.execute_script(
            #    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            #if downloadPercentage == 100:
                # return the file name once the download is completed
            return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        sleep(1)
        #if time() > endTime:
        #    break


def rename_file(filename, year):
    import os
    try:
        path = f'C:\\Users\\Arlin\\Downloads\\'
        name = filename.split('.')[0]
        ext = filename.split('.')[1]
        path_wo_extension = os.path.splitext(path)[0]  # remove extension!!!
        print(f'{path}{year}_{name}.{ext}')
        os.rename(f'{path}{filename}', f'{path}{year}_{name}.{ext}')
    except FileExistsError as e:
        print("file already exits")




def run():
    # driver.find_element(By.XPATH, "//div[@data-theme_short='arbeitsmarkt']").click()
    # driver.find_element(By.XPATH, "//div[@data-theme_short='oeff_finanz_steuern']").click()

    top = ['arbeitsmarkt']  # , bevoelkerung 'arbeitsmarkt', 'oeff_finanz_steuern']

    url = 'https://statistik.at/atlas/'
    driver = make_driver()
    for i in top:
        try:
            driver.get(url)
        except Exception as e:
            print("loading page error!")

        sleep(3)
        driver.find_element(By.XPATH, f"//div[@data-theme_short='{i}']").click()
        sleep(5)
        driver.find_element(By.XPATH, "//a[@data-map_id='them_bevoelkerung_erwerb']").click()
        sleep(1)
        print(f"title: {get_title(driver)}")
        get_slider_start_end(driver)
        get_analysis_data(driver)
        start_download(driver)
        filename = getDownLoadedFileName(driver, 1)
        rename_file(filename, 2022)

run()

