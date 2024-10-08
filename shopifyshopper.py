#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopify Auto-Purchase Script
Created by Mickosis on Fri Feb 26 04:20:00 2021
"""

import socket
import requests
import time
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dhooks import Webhook
from datetime import datetime

# Main Configuration
CONFIG = {
    "json_url": "https://shopifywebsite.com/products.json",
    "shopify_url": "https://shopifywebsite.com/products/",
    "wanted_items": ["Product 1", "Product 2", "Product 3"],
    "chrome_driver_path": r"/Users/UserName/Desktop/chromedriver",
    "discord_webhook": "https://discord.com/api/webhooks/",
    "standby_interval": 180,
    "twilio": {
        "account_sid": "account_sid",
        "auth_token": "auth_token",
        "to_phone": "phone_number",
        "from_phone": "twilio_number",
        "voice_url": "http://demo.twilio.com/docs/voice.xml"
    },
    "shipping_info": {
        "discount_code": "DISC",
        "email": "mikasa@aot.net",
        "first_name": "Mikasa",
        "last_name": "Ackerman",
        "address_1": "Liberio Internment Zone",
        "address_2": "Shiganshina",
        "city": "Wall Rose",
        "country": "Eldia",
        "state": "Paradis Island",
        "zip": "1337"
    }
}

hook = Webhook(CONFIG["discord_webhook"])

# Functions

def find_product_url(products):
    """Returns the URL of the wanted product if available."""
    for product in products:
        if product["title"] in CONFIG["wanted_items"]:
            return f"{CONFIG['shopify_url']}{product['handle']}"
    return None

def purchase_product(url):
    """Automates the purchase process using Selenium."""
    with webdriver.Chrome(executable_path=CONFIG["chrome_driver_path"], options=create_chrome_options()) as driver:
        driver.get(url)
        add_to_cart(driver)
        fill_checkout(driver)
        initiate_twilio_call()

def create_chrome_options():
    """Create and return Chrome options."""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    return chrome_options

def add_to_cart(driver):
    """Adds the item to the cart and proceeds to checkout."""
    driver.find_element_by_xpath('//button[contains(@class, "btn--secondary-accent")]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//a[contains(@class, "cart-popup__cta-link")]').click()
    driver.find_element_by_xpath('//input[contains(@class, "cart__submit")]').click()

def fill_checkout(driver):
    """Fills in the checkout form with shipping information."""
    apply_discount(driver)
    fill_shipping_info(driver)
    driver.find_element_by_xpath('//button[contains(@class, "step__footer__continue-btn")]').click()

def apply_discount(driver):
    """Applies the discount code."""
    driver.find_element_by_xpath('//input[@placeholder="Discount code"]').send_keys(CONFIG["shipping_info"]["discount_code"])
    driver.find_element_by_xpath('//button[contains(@class, "field__input-btn")]').click()

def fill_shipping_info(driver):
    """Fills in the shipping information on the Shopify checkout page."""
    shipping = CONFIG["shipping_info"]
    driver.find_element_by_xpath('//input[@placeholder="Email or mobile phone number"]').send_keys(shipping["email"])
    driver.find_element_by_xpath('//input[@placeholder="First name"]').send_keys(shipping["first_name"])
    driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys(shipping["last_name"])
    driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys(shipping["address_1"])
    driver.find_element_by_xpath('//input[@placeholder="Apartment, suite, etc. (optional)"]').send_keys(shipping["address_2"])
    driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys(shipping["city"])
    driver.find_element_by_xpath('//select[@placeholder="Country/Region"]').send_keys(shipping["country"])
    driver.find_element_by_xpath('//select[@placeholder="State"]').send_keys(shipping["state"])
    driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys(shipping["zip"])

def initiate_twilio_call():
    """Initiates a Twilio call."""
    client = Client(CONFIG["twilio"]["account_sid"], CONFIG["twilio"]["auth_token"])
    call = client.calls.create(
        to=CONFIG["twilio"]["to_phone"],
        from_=CONFIG["twilio"]["from_phone"],
        url=CONFIG["twilio"]["voice_url"]
    )
    message = f"Attempt to call {CONFIG['twilio']['to_phone']} with SID {call.sid}"
    print(message)
    hook.send(message)

# Main Program

def main():
    host_name = socket.gethostname()
    print(f"=== MONITOR INITIATED ON {host_name} ===")
    hook.send(f"=== MONITOR INITIATED ON {host_name} ===")
    
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            products = fetch_products()
            product_url = find_product_url(products)
            
            if product_url:
                message = f"[{current_time}]: Attempting to purchase {product_url}..."
                print(message)
                hook.send(message)
                purchase_product(product_url)
                break
            else:
                print(f"[{current_time}]: Product/s not yet available.")
                time.sleep(CONFIG["standby_interval"])
        except KeyboardInterrupt:
            print(f"=== MONITOR INTERRUPTED ON {host_name} ===")
            hook.send(f"=== MONITOR INTERRUPTED ON {host_name} ===")
            break

def fetch_products():
    """Fetches product data from the Shopify API."""
    response = requests.get(CONFIG["json_url"])
    return response.json().get("products", [])

if __name__ == "__main__":
    main()
