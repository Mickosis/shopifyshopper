#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Monitor with Twilio Call Notification
Created by Mickosis on Mon Mar 1 04:20:00 2021
"""

import socket
import requests
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

def notify(message):
    """Send a notification message via Discord webhook and print to console."""
    print(message)
    hook.send(message)

def find_wanted_product(products):
    """Check if any of the wanted products are available in the product list."""
    return next((product["title"] for product in products if product["title"] in CONFIG["wanted_items"]), None)

def call_user(client):
    """Attempt to call the user via Twilio multiple times."""
    for attempt in range(1, 6):
        call = client.calls.create(
            to=CONFIG["twilio"]["to_phone"],
            from_=CONFIG["twilio"]["from_phone"],
            url=CONFIG["twilio"]["voice_url"]
        )
        notify(f"[{attempt}] Attempt to call {CONFIG['twilio']['to_phone']} with SID {call.sid}")
        time.sleep(CONFIG["standby_interval"])

def check_products(client):
    """Check the availability of wanted products and notify accordingly."""
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            response = requests.get(CONFIG["json_url"])
            products = response.json().get("products", [])
            product_name = find_wanted_product(products)

            if product_name:
                notify(f"[{current_time}]: Product {product_name} is available!")
                aws_hook.send(f"[{current_time}]: Product {product_name} is available!")
                call_user(client)
                break
            else:
                notify(f"[{current_time}] [{len(products)} products]: Not available.")
                aws_hook.send(f"[{current_time}] [{len(products)} products]: Not available.")
                time.sleep(CONFIG["standby_interval"])
        except KeyboardInterrupt:
            host_name = socket.gethostname()
            notify(f"=== MONITOR INTERRUPTED ON {host_name} ===")
            break

def main():
    host_name = socket.gethostname()
    notify(f"=== MONITOR INITIATED ON {host_name} ===")
    
    client = Client(CONFIG["twilio"]["account_sid"], CONFIG["twilio"]["auth_token"])
    check_products(client)

if __name__ == "__main__":
    main()
