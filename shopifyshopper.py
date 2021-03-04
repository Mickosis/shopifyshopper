#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 04:20:00 2021

@author: mickosis
"""

import socket
import requests
import json
import time
import os
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dhooks import Webhook
from datetime import datetime

# Main Configuration

json_url = "https://shopifywebsite.com/products.json"
shopify_url = "https://shopifywebsite.com/products/"
wanted_items = ["Product 1", "Product 2," "Product 3"]
chrome_driver_path = r"/Users/UserName/Desktop/chromedriver"
hook = Webhook("https://discord.com/api/webhooks/")
standby_interval = 180
account_sid = "account_sid"
auth_token = "auth_token"
phone_number = "phone_number"
twilio_number = "twilio_number"
twilio_url = "http://demo.twilio.com/docs/voice.xml"

# Shipping Info

discount_code = "DISC"
email_address = "mikasa@aot.net"
first_name = "Mikasa"
last_name = "Ackerman"
address_1 = "Liberio Internment Zone"
address_2 = "Shiganshina"
city = "Wall Rose"
country = "Eldia"
city_state = "Paradis Island"
zip_code = "1337"

# Main Functions


def has_item():
    r = requests.get(json_url)
    products = json.loads((r.text))["products"]
    for i in range(len(wanted_items)):
        for product in products:
            product_name = product["title"]
            if wanted_items[i] == product_name:
                product_url = shopify_url + product["handle"]
                return product_url
        else:
            return False


def buy_item(url):
    # Start Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        executable_path=chrome_driver_path, chrome_options=chrome_options
    )
    driver.get(str(url))

    # Add Item to Cart
    driver.find_element_by_xpath(
        '//button[@class="btn product-form__cart-submit btn--secondary-accent"]'
    ).click()
    time.sleep(3)
    driver.find_element_by_xpath(
        '//a[@class="cart-popup__cta-link btn btn--secondary-accent"]'
    ).click()
    # time.sleep(0.5)
    driver.find_element_by_xpath(
        '//input[@class="cart__submit btn btn--small-wide"]'
    ).click()
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Discount code"]').send_keys(
        discount_code
    )
    # time.sleep(0.5)
    driver.find_element_by_xpath('//button[@class="field__input-btn btn"]').click()
    # time.sleep(0.5)

    # Add Shipping Information
    driver.find_element_by_xpath(
        '//input[@placeholder="Email or mobile phone number"]'
    ).send_keys(email_address)
    # time.sleep(0.5)
    driver.find_element_by_xpath(
        '//input[@placeholder="First name (optional)"]'
    ).send_keys(first_name)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys(
        last_name
    )
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys(address_1)
    # time.sleep(0.5)
    driver.find_element_by_xpath(
        '//input[@placeholder="Apartment, suite, etc. (optional)"]'
    ).send_keys(address_2)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys(city)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//select[@placeholder="Country/Region"]').send_keys(
        country
    )
    # time.sleep(0.5)
    driver.find_element_by_xpath('//select[@placeholder="State"]').send_keys(city_state)
    # time.sleep(0.5)
    driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys(zip_code)
    # time.sleep(0.5)

    # Check out to PayPal
    driver.find_element_by_xpath(
        '//button[@class="step__footer__continue-btn btn"]'
    ).click()
    # time.sleep(0.5)
    driver.find_element_by_xpath(
        '//button[@class="step__footer__continue-btn btn"]'
    ).click()
    # time.sleep(0.5)
    driver.find_element_by_xpath(
        '//input[@id="checkout_payment_gateway_46824685701"]'
    ).click()

    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=phone_number,
        from_=twilio_number,
        url=twilio_url,
    )
    print(f"Attempt to call {phone_number} with SID {call.sid}")
    hook.send(f"Attempt to call {phone_number} with SID {call.sid}")

    # Send Discord Notification
    while True:
        print("Please complete payment!")
        hook.send("Please complete payment!")
        time.sleep(3)


# Main Program

# Monitoring Loop
host_name = socket.gethostname()
print(f"===MONITOR INITIATED ON {host_name}===")
hook.send(f"===MONITOR INITIATED ON {host_name}===")
is_on = True
while is_on:
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        store_url = has_item()
        if store_url != False:
            print(f"[{current_time}]: Attempting to purchase {store_url}...")
            hook.send(f"[{current_time}]: Attempting to purchase {store_url}...")
            buy_item(store_url)
            is_on = False
            print(f"===MONITOR STOPPED ON {host_name}===")
            hook.send(f"===MONITOR STOPPED ON {host_name}===")
        else:
            print(f"[{current_time}]: Product/s not yet available.")
            time.sleep(standby_interval)
    except KeyboardInterrupt:
        print(f"===MONITOR INTERRUPTED ON {host_name}===")
        hook.send(f"===MONITOR INTERRUPTED ON {host_name}===")
        break
