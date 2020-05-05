#### Note: Amazon changed the layout and IDs of their giftcard reload page, so this script is currently broken. Feel free to make an issue and/or fork the script if you want to make fixes yourself.
---

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
* python-dotenv

---

### Installation/Setup:
Install Selenium using `pip install selenium`</br>
Download the Chrome Webdriver and put it in a location of your choice</br>
Install python-dotenv using `pip install python-dotenv`

#### Variables:
These are environment variables:

* `AMAZON_USERNAME`
* `AMAZON_PASSWORD`
* `CARD_NUMBERS`
* `CHROME_DRIVER`

You can define using whatever method works
best for you (`export` in `.bash_profile`, define in Python console, or just
define in the script), or you can create a .env file in the following format:
```
# .env file
AMAZON_USERNAME=user@domain.com
AMAZON_PASSWORD=password
CC0=1234567890123456
CC1=7890123456789012
```

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
