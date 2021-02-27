#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 04:20:00 2021

@author: mickosis
"""

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dhooks import Webhook
from datetime import datetime

# Main Configuration

json_url = 'https://shopifywebsite.com/products.json'
shopify_url = 'https://shopifywebsite.com/products/'
wanted_item = 'Product Name XL'
chrome_driver_path = r'/Users/UserName/Desktop/chromedriver'
hook = Webhook('https://discord.com/api/webhooks/')
standby_interval = '180'

# Shipping Info

discount_code = 'DISC'
email_address = 'mikasa@aot.net'
first_name = 'Mikasa'
last_name = 'Ackerman'
address_1 = 'Liberio Internment Zone'
address_2 = 'Shiganshina'
city = 'Wall Rose'
country = 'Eldia'
city_state =  'Paradis Island'
zip_code = '1337'

# Main Functions

def has_item():
    r = requests.get(json_url)
    products = json.loads((r.text))['products']
    
    for product in products:
        
        product_name = product['title']
        
        if (product_name == wanted_item):
            product_url = shopify_url + product['handle']
            return product_url
    else:    
        return False


def buy_item(url):
    #Start Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)
    driver.get(str(url))
    
    #Add Item to Cart
    driver.find_element_by_xpath('//button[@class="btn product-form__cart-submit btn--secondary-accent"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//a[@class="cart-popup__cta-link btn btn--secondary-accent"]').click()
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@class="cart__submit btn btn--small-wide"]').click()
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Discount code"]').send_keys(discount_code)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//button[@class="field__input-btn btn"]').click()
    # time.sleep(0.5)
    
    #Add Shipping Information
    driver.find_element_by_xpath('//input[@placeholder="Email or mobile phone number"]').send_keys(email_address)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="First name (optional)"]').send_keys(first_name)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys(last_name)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys(address_1)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Apartment, suite, etc. (optional)"]').send_keys(address_2)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys(city)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//select[@placeholder="Country/Region"]').send_keys(country)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//select[@placeholder="State"]').send_keys(city_state)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys(zip_code)
    # time.sleep(0.5)
    
    #Check out to PayPal
    driver.find_element_by_xpath('//button[@class="step__footer__continue-btn btn"]').click()
    # time.sleep(0.5)
    driver.find_element_by_xpath('//button[@class="step__footer__continue-btn btn"]').click()
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@id="checkout_payment_gateway_46824685701"]').click()
    
    #Send Discord Notification
    awake = True
    while (awake):
        print('Please complete payment!')
        hook.send('Please complete payment!')
        time.sleep(3)
    
# Main Program

# Monitoring Loop
is_on = True
while (is_on):
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        store_url = has_item()
        if store_url != False:
            print('Product is Available!')
            hook.send('Product is available!')
            buy_item(store_url)
            is_on = False
        else:
            print(current_time + ' Product Not Yet Available')
            hook.send(current_time + ' Product Not Yet Available')
            time.sleep(standby_interval)
    except KeyboardInterrupt:
        print('Script stopped!')
        break