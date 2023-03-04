import logging.config
import os
import random
import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

def error_screen():
    screenShotFileName = '{}errorImage.png'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__))
    screenShotFullPath = os.path.join(screenShotFloderPath, screenShotFileName)
    driver.save_screenshot(screenShotFullPath)

def waitElementClickable(elementLocator, seconds):
	wait = WebDriverWait(driver, 10)
	element = wait.until(expected_conditions.element_to_be_clickable(elementLocator))
	time.sleep(seconds)
	return element

def waitElement(elementLocator, seconds):
	wait = WebDriverWait(driver, 10)
	element = wait.until(expected_conditions.presence_of_element_located(elementLocator))
	time.sleep(seconds)
	return element

def clip():
    screenShotFileName = '{}clipImage.png'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__))
    screenShotFullPath = os.path.join(screenShotFloderPath, screenShotFileName)
    driver.save_screenshot(screenShotFullPath)

def login():
    driver.get('https://www.instagram.com')
    userNameTextBoxName = 'username'
    passTextBoxName = 'password'
    elementUserNameTextBox = waitElement((By.NAME, userNameTextBoxName), 10)
    elementUserNameTextBox.send_keys('klrqkcgngm')
    time.sleep(1)
    driver.find_element_by_name(passTextBoxName).send_keys('yayaya#1234')
    time.sleep(1)
    loginButton = driver.find_element_by_css_selector("button[type=submit]")
    loginButton.click()
    time.sleep(random.randint(2, 3))
    laterButtonXpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/div/button'
    elementLaterButton = waitElementClickable((By.XPATH, laterButtonXpath), 5)
    elementLaterButton.click()
    time.sleep(random.randint(2, 3))
    logging.info('Clicked later')

def like(url):
    driver.get(url)
    likeButtonXpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
    elementLikeButton = waitElementClickable((By.XPATH,likeButtonXpath) , 2)
    elementLikeButton.click()
    logging.info('like clicked')

try:
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()

    logging.info('Start!!!')
    logging.info('Now login...')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options)
    time.sleep(3)
    login()
    logging.info('Done Login')

    with open('./url.csv') as f:
        for url in f:
            time.sleep(random.randint(2, 3))

            like(url)
            time.sleep(random.randint(2, 3))
            clip()
            time.sleep(random.randint(2, 3)*10)
    driver.close()



except Exception as e:
    error_screen()
    driver.close()