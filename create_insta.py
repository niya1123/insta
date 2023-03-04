import os
import time
from datetime import datetime

from operate_csv import generate_user_data
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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

def sign_up():
    email, fullname, username, password= generate_user_data()
    try:
        # 名前等の入力画面
        driver.get('https://www.instagram.com/accounts/emailsignup/')
        elementEmailOrPhoneTextBox = waitElement((By.NAME, 'emailOrPhone'), 3)
        elementEmailOrPhoneTextBox.send_keys(email)
        elementFullNameTextBox = waitElement((By.NAME, 'fullName'), 3)
        elementFullNameTextBox.send_keys(fullname)
        elementUserNameTextBox = waitElement((By.NAME, 'username'), 3)
        elementUserNameTextBox.send_keys(username)
        elementPassWordTextBox = waitElement((By.NAME, 'password'), 3)
        elementPassWordTextBox.send_keys(password)
        nextButtonXpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/button'
        elementNextButton = waitElementClickable((By.XPATH, nextButtonXpath), 3)
        elementNextButton.click()
        wait.until(EC.presence_of_all_elements_located)

        # 生年月日入力画面
        yearXpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select'
        elementYear =  waitElementClickable((By.XPATH, yearXpath), 3)
        yearSelect = Select(elementYear)
        yearSelect.select_by_visible_text("1999")
        nextButtonXpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div/div[6]'
        elementNextButton = waitElementClickable((By.XPATH, nextButtonXpath), 3)
        elementNextButton.click()
        wait.until(EC.presence_of_all_elements_located)
    except Exception as e:
        print(e)
        error_screen()
        print('アカウントは作成されませんでした')

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
    sign_up()
    driver.close()
    driver.quit()

except Exception as e:
    error_screen()
    driver.close()
    driver.quit()

finally:
    clip()
    driver.close()
    driver.quit()