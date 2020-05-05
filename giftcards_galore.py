"""Autobuy Amazon Giftcards"""

import os
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException

# User-defined variables
AMAZON_USERNAME = os.getenv('AMAZON_USERNAME')
    # Your Amazon username (email)
AMAZON_PASSWORD = os.getenv('AMAZON_PASSWORD')
    # Your Amazon password
CARDS = [1, 2, 3, 4]
    # 0-indexed array of your Amazon payment methods
    # Refer to https://www.amazon.com/gp/wallet
CARD_NUMBERS = [
    os.getenv('TD_DEBIT'),
    os.getenv('CSR'),
    os.getenv('CFU'),
    os.getenv('CF2')]
    # Your credit card numbers, corresponding to the index of each card in the CARDS array
ITERATIONS = [1, 1, 1, 1]
    # Iterations array, corresponds to the number of purchases for each card

def giftcard_buyer():
    "Function to buy the giftcards"

    driver = webdriver.Chrome(os.getenv('CHROME_DRIVER'))
        # Path to your chrome webdriver file
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.amazon.com/asv/reload/')
    driver.find_element_by_id('form-submit-button').click()
    wait.until(EC.title_is('Amazon.com Sign In'))
    driver.find_element_by_id('ap_email').send_keys(AMAZON_USERNAME)
    driver.find_element_by_id('ap_signin_existing_radio').click()
    driver.find_element_by_id('ap_password').send_keys(AMAZON_PASSWORD)
    driver.find_element_by_id('signInSubmit').click()

    i = 0
    for card in CARDS:
        print "card: %r" %(card)
        for iteration in range(ITERATIONS[i]):
            print "iteration: %r" %(iteration + 1)
            if driver.title != 'Reload Your Balance':
                driver.get('https://www.amazon.com/asv/reload/')
            wait.until(EC.title_is('Reload Your Balance'))
            driver.find_element_by_id('asv-manual-reload-amount').send_keys('1')
            time.sleep(1)
            driver.find_elements_by_class_name('pmts-credit-card-row')[card].click()
            if iteration == 0:
                driver.find_element_by_name('addCardNumber').send_keys(CARD_NUMBERS[card - 1])
                driver.find_element_by_xpath("//button[contains(.,'Confirm Card')]").click()
                time.sleep(1)
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
