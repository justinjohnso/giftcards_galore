"""Autobuy Amazon Giftcards"""

import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException

# Load env variables from ".env" file in the same folder
load_dotenv()

# User-defined variables
AMAZON_USERNAME = os.getenv('AMAZON_USERNAME')
    # Your Amazon username (email)
AMAZON_PASSWORD = os.getenv('AMAZON_PASSWORD')
    # Your Amazon password
CARDS = [0, 1]
    # 0-indexed array of your Amazon payment methods
    # Refer to https://www.amazon.com/gp/wallet
CARD_NUMBERS = [
    os.getenv('CC0'),
    os.getenv('CC1')]
    # Your credit card numbers, corresponding to the index of each card in the CARDS array
ITERATIONS = [1, 1]
    # Iterations array, corresponds to the number of purchases for each card
GIFT_CARD_AMOUNT = os.getenv('GIFT_CARD_AMOUNT')
    # Amount to be loaded onto each gift card

class AuthenticationError(Exception):
    pass
    
def giftcard_buyer():
    "Function to buy the giftcards"

    driver = webdriver.Chrome()
        # Ensure Chrome Webdriver is on System PATH
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.amazon.com/asv/reload/')
    driver.find_element_by_id('form-submit-button').click()
    wait.until(EC.title_is('Amazon.com Sign In'))
    driver.find_element_by_id('ap_email').send_keys(AMAZON_USERNAME)
    driver.find_element_by_id('continue').click()
    driver.find_element_by_id('ap_password').send_keys(AMAZON_PASSWORD)
    driver.find_element_by_id('signInSubmit').click()
    try:
        driver.find_element_by_xpath("//h1[contains(.,'Authentication Required')]")
        raise AuthenticationError("You need to manually confirm your login")
    except NoSuchElementException:
        pass

    i = 0
    for card in CARDS:
        print "card: %r" %(card)
        for iteration in range(ITERATIONS[i]):
            print "iteration: %r" %(iteration + 1)
            if driver.title != 'Reload Your Balance':
                driver.get('https://www.amazon.com/asv/reload/')
            wait.until(EC.title_is('Reload Your Balance'))
            driver.find_element_by_id('asv-manual-reload-amount').send_keys(str(GIFT_CARD_AMOUNT))
            time.sleep(0.5)
            driver.find_elements_by_class_name('pmts-credit-card-row')[card].click()
            if iteration == 0:
                try:
                    driver.find_element_by_name('addCardNumber').send_keys(CARD_NUMBERS[card - 1])
                    driver.find_element_by_xpath("//button[contains(.,'Confirm Card')]").click()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
            else:
                time.sleep(random.randint(120,361)
            driver.find_element_by_id('form-submit-button').click()
            time.sleep(1)
            try:
                driver.find_element_by_xpath("//span[contains(.,'this message again')]").click()
                time.sleep(.5)
                driver.find_element_by_id('asv-reminder-action-primary').click()
                time.sleep(1)
            except NoSuchElementException:
                pass
            driver.get('https://www.amazon.com/asv/reload/')
        i += 1

giftcard_buyer()
