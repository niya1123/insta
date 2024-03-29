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

likeCounter = 0
notLikeCounter = 0
alreadyLikeCounter = 0
continueLikeTooMuchCounter = 0
continuousLikeCounter = 0

def login():
	driver.get('https://www.instagram.com/')
	time.sleep(1)
	userNameTextBoxName = 'username'
	passTextBoxName = 'password'
	elementUserNameTextBox = waitElement((By.NAME, userNameTextBoxName), 10)
	elementUserNameTextBox.send_keys('boylw12')
	time.sleep(1)
	driver.find_element_by_name(passTextBoxName).send_keys('ad#1234')
	time.sleep(1)

	# loginButtonClassName = '_ab8w  '
	# elementLoginButton = waitElementClickable((By.CLASS_NAME, loginButtonClassName), 10)
	# elementLoginButton.click() #class="sqdOP  L3NKy   y3zKF     "
	loginButton = driver.find_element_by_css_selector("button[type=submit]")
	loginButton.click()
	time.sleep(random.randint(2, 5))

def searchByTag(tag):
	logger.info('search by {}'.format(tag))
	instaurl = 'https://www.instagram.com/explore/tags/'
	driver.get(instaurl + tag)
	time.sleep(random.randint(2, 5))

def isAlreadyPressLike(likeButton):
	label = likeButton.get_attribute('aria-label')
	if label == '「いいね！」を取り消す':
		return True
	else:
		return False

def pressLike():
	global likeCounter
	global alreadyLikeCounter
	global continueLikeTooMuchCounter
	global continuousLikeCounter
	likeButtonClassName = 'fr66n'
	elementLikeButton = waitElementClickable((By.CLASS_NAME,likeButtonClassName) , 2)
	element = elementLikeButton.find_element_by_xpath('./button/div/span')
	element1 = element.find_element_by_class_name('_8-yf5 ')
	if isAlreadyPressLike(element1):
		time.sleep(1)
		alreadyLikeCounter = alreadyLikeCounter + 1
		logger.info('already press like_{}'.format(alreadyLikeCounter))
		continuousLikeCounter = 0
	else:
		if continuousLikeCounter >= 10:		
			time.sleep(1)
			continueLikeTooMuchCounter = continueLikeTooMuchCounter + 1
			logger.info('pressed like continuously {} times, so not press like. This is {} times.'.format(continuousLikeCounter, continueLikeTooMuchCounter))
			continuousLikeCounter = 0
		else:
			time.sleep(random.randint(2, 5))
			elementLikeButton.click()
			likeCounter = likeCounter + 1
			continuousLikeCounter = continuousLikeCounter + 1
			logger.info('press like_{}'.format(likeCounter))

def clickLike():
	global notLikeCounter
	global continuousLikeCounter
	targetImageClassName = '_aagw'
	elementtargetImages =  waitElements((By.CLASS_NAME,targetImageClassName) , 2)
	elementImageToScroll = elementtargetImages[10]
	actions = ActionChains(driver)
	actions.move_to_element(elementImageToScroll)
	actions.perform()
	time.sleep(random.randint(2, 3))

	driver.find_elements_by_class_name(targetImageClassName)[9].click()
	time.sleep(random.randint(2, 3))

	pressLikeLoopCount = random.randint(5, 6)
	for pressLikeLoopCounter in range(pressLikeLoopCount):
		if random.randint(1, 6) % 6 == 0:
			notLikeCounter += 1
			continuousLikeCounter = 0
			logger.info('not to try press like_{}'.format(notLikeCounter))
			time.sleep(1)
		else:
			pressLike()
			time.sleep(random.randint(2, 3))
		
		if pressLikeLoopCounter == pressLikeLoopCount - 1:
			break

		nextArrowClassName = 'coreSpriteRightPaginationArrow'
		elementNextArrow = waitElementClickable((By.CLASS_NAME, nextArrowClassName), 2)
		elementNextArrow.click()
		time.sleep(random.randint(2, 5))

def convertMinutesToSeconds(minutes):
    return (minutes*5)

def waitElement(elementLocator, seconds):
	wait = WebDriverWait(driver, 10)
	element = wait.until(expected_conditions.presence_of_element_located(elementLocator))
	time.sleep(seconds)
	return element
	
def waitElements(elementLocator, seconds):
	wait = WebDriverWait(driver, 10)
	elements = wait.until(expected_conditions.presence_of_all_elements_located(elementLocator))
	time.sleep(seconds)
	return elements

def waitElementClickable(elementLocator, seconds):
	wait = WebDriverWait(driver, 10)
	element = wait.until(expected_conditions.element_to_be_clickable(elementLocator))
	time.sleep(seconds)
	return element

def startAutomation():
	global continuousLikeCounter

	topLoopCount = random.randint(5, 6)
	for topLoopCounter in range(topLoopCount):
		continuousLikeCounter = 0
		searchByTag(random.choice(taglist))
		clickLike()
		if topLoopCounter == topLoopCount - 1:
			break#最後のループは待機せずブラウザを閉じに行く
		time.sleep(random.randint(15, 30))

if __name__ == '__main__':
	taglist = ['ポケモン', 'ドラえもん']
	logging.config.fileConfig('logging.conf')
	logger = logging.getLogger()

	loopCount = 0
	errorCount = 0
	logging.info('Start!!!')
	while True:
		try:
			driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
			desired_capabilities=DesiredCapabilities.CHROME)
			loopCount += 1
			logging.info('Loop Count_{}'.format(loopCount))
			login()
			time.sleep(random.randint(2, 3))

			# laterButtonXpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button"
			# elementLaterButton = waitElementClickable((By.XPATH, laterButtonXpath), 2)
			# elementLaterButton.click()
			# time.sleep(random.randint(2, 3))

			# # //*[@id="mount_0_0_Aq"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]
			# laterButtonXpath2 = "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
			# elementLaterButton2 = waitElementClickable((By.XPATH, laterButtonXpath2), 2)
			# elementLaterButton2.click()
			# time.sleep(random.randint(2, 3))
			startAutomation()
		except Exception as e:
			errorCount += 1
			import traceback
			logging.error(traceback.format_exc())

			screenShotFileName = '{}errorImage{}.png'.format(datetime.now().strftime("%Y%m%d_%H%M%S") , errorCount)
			screenShotFloderPath = os.path.dirname(os.path.abspath(__file__))
			screenShotFullPath = os.path.join(screenShotFloderPath, screenShotFileName)
			driver.save_screenshot(screenShotFullPath)

			if errorCount == 10:
				logging.error('Error. End system.')
				driver.close()
				break

			logging.error('error {} times'.format(errorCount))
			driver.close()
			waitTime = random.randint(convertMinutesToSeconds(60), convertMinutesToSeconds(65))
			logging.info('wait for {} secs'.format(waitTime))
			time.sleep(waitTime)
		else:			
			if loopCount % 10 == 0:
				waitTime = random.randint(convertMinutesToSeconds(30), convertMinutesToSeconds(32))
				logging.info('wait for {} secs'.format(waitTime))
				driver.close()
				time.sleep(waitTime)
			else:			 
				waitTime = random.randint(convertMinutesToSeconds(10), convertMinutesToSeconds(12))
				logging.info('wait for {} secs'.format(waitTime))
				driver.close()
				time.sleep(waitTime)
