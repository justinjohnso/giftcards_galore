"""Autobuy Amazon Giftcards"""

import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

# Load env variables from ".env" file in the same folder
load_dotenv()

# -------- User-defined variables --------

# Your Amazon username (email)
AMAZON_USERNAME = os.getenv('AMAZON_USERNAME')

# Your Amazon password
AMAZON_PASSWORD = os.getenv('AMAZON_PASSWORD')

# 0-indexed array of your Amazon payment methods
# Refer to https://www.amazon.com/gp/wallet
# code for two cards:
# CARDS = [0, 1]
# code for one card:
CARDS = [0]

# Your credit card numbers, corresponding to the index of each card in the CARDS array
# code for two cards:
# CARD_NUMBERS = [
#     os.getenv('CC0'),
#     os.getenv('CC1')
# ]
# code for one card:
CARD_NUMBERS = [
    os.getenv('CC0')
]

# Iterations array, corresponds to the number of purchases for each card
# code for two cards, 5 iterations each:
# ITERATIONS = [5, 5]
# code for one card, 10 iterations:
ITERATIONS = [10]

# Amount to be loaded onto each gift card
GIFT_CARD_AMOUNT = os.getenv('GIFT_CARD_AMOUNT')


class AuthenticationError(Exception):
    pass

def giftcard_buyer():
    "Function to buy the giftcards"

    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    # Ensure Chrome Webdriver is on System PATH
    driver = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.amazon.com/asv/reload/')
    driver.find_element_by_id('form-submit-button').click()
    WebDriverWait(driver, 10).until(EC.title_contains("Amazon Sign-In"))
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
        print "Starting Card # %r" %(card)
        for iteration in range(ITERATIONS[i]):
            if driver.title != 'Reload Your Balance':
                driver.get('https://www.amazon.com/asv/reload/')
            wait.until(EC.title_is('Reload Your Balance'))
            driver.find_element_by_id('asv-manual-reload-amount').send_keys(str(GIFT_CARD_AMOUNT))
            time.sleep(0.5)
            try:
                driver.find_elements_by_class_name('pmts-credit-card-row')[card].click()
                driver.find_element_by_id('form-submit-button').click()
                time.sleep(5)
            except IndexError:
                # Need to give password again
                driver.find_element_by_id('form-submit-button').click()
                driver.find_element_by_id('ap_password').send_keys(AMAZON_PASSWORD)
                driver.find_element_by_id('signInSubmit').click()
            if iteration == 0:
                try:
                    driver.find_element_by_xpath("//input[contains(@name,'addCreditCardNumber')]").send_keys(CARD_NUMBERS[card])
                    driver.find_element_by_xpath("//button[contains(@aria-label,'Verify card')]").click()
                    time.sleep(5)
                    driver.find_element_by_id('form-submit-button').click()
                    time.sleep(5)
                except NoSuchElementException:
                    pass
            else:
                time.sleep(random.randint(120,361))
            try:
                driver.find_element_by_xpath("//span[contains(.,'this message again')]").click()
                time.sleep(.5)
                driver.find_element_by_id('asv-reminder-action-primary').click()
                time.sleep(1)
            except (NoSuchElementException, ElementNotInteractableException):
                pass
            driver.get('https://www.amazon.com/asv/reload/')
            print "Completed iteration %r" %(iteration + 1)
        print "Completed card # %r" %(card)
        i += 1
    driver.quit()
    print "Finished!"

giftcard_buyer()
