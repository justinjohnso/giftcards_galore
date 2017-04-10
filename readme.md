# Giftcards Galore!
Python script to auto-buy Amazon giftcards

Based off of: </br>
https://github.com/ageoldpun/amazon_gifts
</br>
http://pastebin.com/UW6eC3rn

---

### Dependencies:
* Selenium
* Chrome Webdriver
  ([download](https://sites.google.com/a/chromium.org/chromedriver/downloads))

---

### Installation/Setup:
Install Selenium using `pip install selenium`</br>
Download the Chrome Webdriver and put it in a location of your choice

#### Variables:
These are environment variables that you can define using whatever method works
best for you (`export` in `.bash_profile`, define in Python console or just
define in the script):

* `AMAZON_USERNAME`
* `AMAZON_PASSWORD`
* `CARD_NUMBERS`
* `CHROME_DRIVER`

You need your card numbers because Amazon will ask to confirm each one for the
first iteration of a given card.

`CHROME_DRIVER` is the location of your Chrome Webdriver (line 31).
Example: `/Users/Spock/Downloads/webdrivers/chromedriver`

These are arrays that correspond with the (0-indexed) list of cards on your
[Amazon Wallet](https://www.amazon.com/gp/wallet) page:

* `CARDS`
* `ITERATIONS`

---

### Usage:

In terminal, run `python giftcards_galore.py`. Selenium will open a new Chrome
window and start the script.

For testing purposes, I recommend either starting with one iteration per card,
or commenting out line 57. 
