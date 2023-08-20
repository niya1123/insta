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

def make_dir_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def error_screen():
    screenShotFileName = '{}errorImage.png'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    screenShotFloderPath = os.path.dirname(os.path.abspath(__file__)) + '/insta_error'
    make_dir_if_not_exists(screenShotFloderPath)
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
    make_dir_if_not_exists(screenShotFloderPath)
    screenShotFullPath = os.path.join(screenShotFloderPath, screenShotFileName)
    driver.save_screenshot(screenShotFullPath)

def login(username, password):
    driver.get('https://www.instagram.com')
    userNameTextBoxName = 'username'
    passTextBoxName = 'password'
    elementUserNameTextBox = waitElement((By.NAME, userNameTextBoxName), 5)
    elementUserNameTextBox.send_keys(username)
    driver.find_element_by_name(passTextBoxName).send_keys(password)
    loginButton = driver.find_element_by_css_selector("button[type=submit]")
    loginButton.click()
    logging.info('ログインしました')
    loginSaveButtonXpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button'
    elementLoginSaveButton = waitElementClickable((By.XPATH, loginSaveButtonXpath), 5)
    if(elementLoginSaveButton):
        elementLoginSaveButton.click()
        logging.info('ログイン情報を保存しました')
    time.sleep(3)

def write_log_to_file():
    # ログファイルの設定を読み込む
    logging.config.fileConfig('logging.conf')

    # ロガーを取得する
    logger = logging.getLogger(__name__)

    # ログファイルのパス
    log_file_path = 'root.log'

    # ログファイルが存在する場合
    if os.path.exists(log_file_path):
        # ログファイルの内容を読み込む
        with open(log_file_path, 'r') as f:
            log_content = f.read()

        # ログファイルの内容がある場合
        if log_content:
            # 実行した日時を取得する
            now = datetime.now()
            date_str = now.strftime('%Y%m%d%H%M%S')

            # 新しいログファイル名を作成する
            new_log_file_name = f'{date_str}.log'

            # logsディレクトリが存在しない場合は作成する
            make_dir_if_not_exists('logs')

            # 新しいログファイルにログファイルの内容を書き込む
            with open(f'logs/{new_log_file_name}', 'w') as f:
                f.write(log_content)

            # ログファイルを削除する
            os.remove(log_file_path)

def isAlreadyPressLike(likeButton):
	label = likeButton.get_attribute('aria-label')
	if label == '「いいね！」を取り消す':
		return True
	else:
		return False 


try:
    write_log_to_file()
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
    with open('userdata.csv') as f:
        for userdata in f:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
            options=chrome_options)

            logging.info('プログラムを実行しました')
            logging.info('ただいまログイン中です')
            name, password = userdata.strip().split(",")
            login(name, password)
            logging.info('「'+name+'」'+'がログインが完了しました')

            with open('./url.csv') as f:
                for url in f:
                    logging.info('投稿を読み込んでいます')
                    driver.get(url)
                    likeButtonXpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]'
                    elementLikeButton = waitElementClickable((By.XPATH,likeButtonXpath) , 5)
                    if(elementLikeButton and not isAlreadyPressLike(elementLikeButton)):
                        elementLikeButton.click()
                        logging.info(url+'をいいねしました！')
                    elif(driver.current_url is not url):
                        logging.info('指定されたURLに飛べず、投稿を読み込めませんでした')
                    else:
                        logging.info('投稿を読み込めませんでした')
                    clip()
                    logging.info('プログラムが完了しました')
            driver.close()



except Exception as e:
    logging.info('エラーが発生しました')
    error_screen()
    driver.close()