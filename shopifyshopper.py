#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:00:00 2021

@author: mickosis
"""

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dhooks import Webhook
from datetime import datetime

def has_item():
    r = requests.get('https://shopifywebsite.com/products.json')
    products = json.loads((r.text))['products']
    
    for product in products:
        
        product_name = product['title']
        
        if (product_name == 'Product Name'):
            product_url = 'https://shopifywebsite.com/products/' + product['handle']
            return product_url
    else:    
        return False


def buy_item(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=r'/Users/UserName/Desktop/chromedriver', chrome_options=chrome_options)
    driver.get(str(url))
    
    #Add Item to Cart
    driver.find_element_by_xpath('//button[@class="btn product-form__cart-submit btn--secondary-accent"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//a[@class="cart-popup__cta-link btn btn--secondary-accent"]').click()
    driver.find_element_by_xpath('//input[@class="cart__submit btn btn--small-wide"]').click()
    
    driver.find_element_by_xpath('//input[@placeholder="Discount code"]').send_keys('PVRP')
    driver.find_element_by_xpath('//button[@class="field__input-btn btn"]').click()
    
    #Add Shipping Information
    driver.find_element_by_xpath('//input[@placeholder="Email or mobile phone number"]').send_keys('Email')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="First name (optional)"]').send_keys('Mico')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys('Rigunay')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys('3407 East Marina Boulevard')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Apartment, suite, etc. (optional)"]').send_keys('Suite: 807-1980')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys('Burbank')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//select[@placeholder="Country/Region"]').send_keys('United States')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//select[@placeholder="State"]').send_keys('California')
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys('661055')
    
    #Check out to PayPal
    driver.find_element_by_xpath('//button[@class="step__footer__continue-btn btn"]').click()
    
    driver.find_element_by_xpath('//button[@class="step__footer__continue-btn btn"]').click()
    
    driver.find_element_by_xpath('//input[@id="checkout_payment_gateway_46824685701"]').click()
    
    #Send Discord Notification
    awake = True
    while (awake):
        print('Please complete payment!')
        hook.send('Please complete payment!')
        time.sleep(3)
    
# Main Program

# Set Discord Webhook
hook = Webhook('https://discord.com/api/webhooks/')

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
            # Set to specified interval (in Seconds)
            time.sleep(300)
    except KeyboardInterrupt:
        print('Script stopped!')
        break