import os
import random
import string
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def error_screen():
    screenShotFileName = '{}errorImage.png'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__)) + '/insta_error'
    screenShotFullPath = os.path.join(screenShotFloderPath, screenShotFileName)
    driver.save_screenshot(screenShotFullPath)

def clip():
    screenShotFileName = '{}clipImage.png'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__)) + '/insta_clip'
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

def generate_random_string(n, used_strings):
    while True:
        random_string = ''.join(random.choices(string.ascii_letters, k=n))
        if random_string not in used_strings:
            used_strings.append(random_string)
            return random_string
        
def generate_user_data():
      # 生成したlastname, firstname, username, passwordを格納するリスト
    lastnames = []
    firstnames = []
    usernames = []
    passwords = []
   
    # csvファイルの読み込み
    df = pd.read_csv('userdata.csv')
    for i in range(len(df)):
        used_lastnames = list(df['lastname'])
        used_firstnames = list(df['firstname'])
        used_usernames = list(df['username'])
        used_passwords = list(df['password'])
        
        lastnames.append(generate_random_string(8, used_lastnames))
        firstnames.append(generate_random_string(8, used_firstnames))
        usernames.append(generate_random_string(8, used_usernames)+''.join(random.choice(string.digits) if j == 2 else random.choice(string.ascii_letters) for j in range(8)))
        while True:
            password = generate_random_string(random.randint(8, 12), used_passwords)
            if len(password) >= 8 and len(password) <= 12:
                break
        passwords.append(password)
    
    # 生成したランダムな文字列をデータフレームに追加してcsvファイルに保存
    new_df = pd.DataFrame({'lastname': lastnames, 'firstname': firstnames, 'username': usernames, 'password': passwords})
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv('userdata.csv', index=False)

def sign_up():
    lastnames = []
    firstnames = []
    usernames = []
    passwords = []
   
    # csvファイルの読み込み
    df = pd.read_csv('userdata.csv')
    for i in range(len(df)):
        lastnames = list(df['lastname'])
        firstnames = list(df['firstname'])
        usernames = list(df['username'])
        passwords = list(df['password'])

    driver.get('https://www.instagram.com/accounts/emailsignup/')
    elementLastNameTextBox = waitElement((By.NAME, 'fullName'), 3)
    elementLastNameTextBox.send_keys(lastnames[-1])
    userNameXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input'
    elementUserNameTextBox = waitElement((By.NAME, 'Username'), 3)
    driver.find_element_by_xpath(userNameXpath).clear()
    elementUserNameTextBox.send_keys(usernames[-1])
    elementPassWordTextBox = waitElement((By.NAME, 'Passwd'), 3)
    elementPassWordTextBox.send_keys(passwords[-1])
    elementConfirmPassWordTextBox = waitElement((By.NAME, 'ConfirmPasswd'), 3)
    elementConfirmPassWordTextBox.send_keys(passwords[-1])
    nextButtonXpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
    elementNextButton = waitElementClickable((By.XPATH, nextButtonXpath), 3)
    elementNextButton.click()
    wait.until(EC.presence_of_all_elements_located)

try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--proxy-server=socks5://tor-proxy:9050")
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options)
    wait = WebDriverWait(driver=driver, timeout=180)
    generate_user_data()
    sign_up()
    time.sleep(9)
    clip()
    driver.close()
    driver.quit()

except Exception as e:
    error_screen()
    driver.close()
    driver.quit()

finally:
    driver.close()
    driver.quit()