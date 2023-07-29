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
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__)) + '/insta_error'
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
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__)) + '/insta_clip'
    screenShotFullPath = os.path.join(screenShotFloderPath, screenShotFileName)
    driver.save_screenshot(screenShotFullPath)

def login():
    driver.get('https://www.instagram.com')
    userNameTextBoxName = 'username'
    passTextBoxName = 'password'
    elementUserNameTextBox = waitElement((By.NAME, userNameTextBoxName), 5)
    elementUserNameTextBox.send_keys('takesiins')
    driver.find_element_by_name(passTextBoxName).send_keys('Insta#1234')
    loginButton = driver.find_element_by_css_selector("button[type=submit]")
    loginButton.click()
    logging.info('ログインしました')
    loginSaveButtonXpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button'
    elementLoginSaveButton = waitElementClickable((By.XPATH, loginSaveButtonXpath), 5)
    if(elementLoginSaveButton):
        elementLoginSaveButton.click()
        logging.info('ログイン情報を保存しました')

# def like(url):
#     driver.get(url)
#     logging.info('投稿を読み込んでいます')
#     likeButtonXpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div/span/svg'
#     elementLikeButton = waitElementClickable((By.XPATH,likeButtonXpath) , 2)
#     elementLikeButton.click()
#     logging.info(url+'をいいねしました！')

try:
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()

    logging.info('プログラムを実行しました')
    logging.info('ただいまログイン中です')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options)
    login()
    logging.info('ログインが完了しました')

    with open('./url.csv') as f:
        for url in f:
            driver.get(url)
            logging.info('投稿を読み込んでいます')
            likeButtonXpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]'
            elementLikeButton = waitElementClickable((By.XPATH,likeButtonXpath) , 5)
            if(elementLikeButton):
                elementLikeButton.click()
                logging.info(url+'をいいねしました！')
            else:
                logging.info('投稿を読み込めませんでした')
            # like(url)
            clip()
    logging.info('プログラムが完了しました')
    driver.close()



except Exception as e:
    logging.info('エラーが発生しました')
    error_screen()
    driver.close()