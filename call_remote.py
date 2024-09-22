#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Monitor with Twilio Call Notification
Created by Mickosis on Mon Mar 1 04:20:00 2021
"""

import socket
import requests
import json
import time
from twilio.rest import Client
from dhooks import Webhook
from datetime import datetime

# Main Configuration
CONFIG = {
    "json_url": "https://shopifywebsite.com/products.json",
    "wanted_items": ["Product 1", "Product 2", "Product 3"],
    "discord_webhook": "https://discord.com/api/webhooks/",
    "aws_webhook": "https://discord.com/api/webhooks/",
    "standby_interval": 60,
    "twilio": {
        "account_sid": "account_sid",
        "auth_token": "auth_token",
        "to_phone": "phone_number",
        "from_phone": "twilio_number",
        "voice_url": "http://demo.twilio.com/docs/voice.xml"
    }
}

# Initialize Webhooks
hook = Webhook(CONFIG["discord_webhook"])
aws_hook = Webhook(CONFIG["aws_webhook"])

# Functions

def find_wanted_product(products):
    """Checks if any of the wanted products are available in the product list."""
    for item in CONFIG["wanted_items"]:
        for product in products:
            if item == product["title"]:
                return product["title"]
    return False

def call_user(client):
    """Attempts to call the user via Twilio."""
    for attempt in range(1, 6):
        call = client.calls.create(
            to=CONFIG["twilio"]["to_phone"],
            from_=CONFIG["twilio"]["from_phone"],
            url=CONFIG["twilio"]["voice_url"]
        )
        message = f"[{attempt}] Attempt to call {CONFIG['twilio']['to_phone']} with SID {call.sid}"
        print(message)
        hook.send(message)
        time.sleep(CONFIG["standby_interval"])

# Main Program

def main():
    host_name = socket.gethostname()
    print(f"=== MONITOR INITIATED ON {host_name} ===")
    hook.send(f"=== MONITOR INITIATED ON {host_name} ===")
    
    client = Client(CONFIG["twilio"]["account_sid"], CONFIG["twilio"]["auth_token"])
    
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            response = requests.get(CONFIG["json_url"])
            products = response.json()["products"]
            product_name = find_wanted_product(products)
            
            if product_name:
                message = f"[{current_time}]: Product {product_name} is available!"
                print(message)
                hook.send(message)
                aws_hook.send(message)
                call_user(client)
                break
            else:
                print(f"[{current_time}] [{len(products)} products]: Not available.")
                aws_hook.send(f"[{current_time}] [{len(products)} products]: Not available.")
                time.sleep(CONFIG["standby_interval"])
        except KeyboardInterrupt:
            print(f"=== MONITOR INTERRUPTED ON {host_name} ===")
            hook.send(f"=== MONITOR INTERRUPTED ON {host_name} ===")
            break

if __name__ == "__main__":
    main()
