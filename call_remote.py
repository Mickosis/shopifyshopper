#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 1 04:20:00 2021

@author: mickosis
"""

import socket
import requests
import json
import time
import os
from twilio.rest import Client
from dhooks import Webhook
from datetime import datetime

# Main Configuration

json_url = "https://shopifywebsite.com/products.json"
wanted_items = ["Product 1", "Product 2," "Product 3"]
hook = Webhook("https://discord.com/api/webhooks/")
aws_hook = Webhook("https://discord.com/api/webhooks/")
standby_interval = 60
account_sid = "account_sid"
auth_token = "auth_token"
phone_number = "phone_number"
twilio_number = "twilio_number"
twilio_url = "http://demo.twilio.com/docs/voice.xml"

# Main Functions


def has_item(products):
    for i in range(len(wanted_items)):
        for product in products:
            product_name = product["title"]
            if wanted_items[i] == product_name:
                return product_name
    else:
        return False


def call_user():
    for i in range(1, 6):
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            to=phone_number,
            from_=twilio_number,
            url=twilio_url,
        )
        print(f"[{i}] Attempt to call {phone_number} with SID {call.sid}")
        hook.send(f"[{i}] Attempt to call {phone_number} with SID {call.sid}")
        time.sleep(standby_interval)


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
        r = requests.get(json_url)
        products = json.loads((r.text))["products"]
        item_name = has_item(products)
        if item_name != False:
            print(f"[{current_time}]: Product {item_name} is available!")
            hook.send(f"[{current_time}]: Product {item_name} is available!")
            aws_hook.send(f"[{current_time}]: Product {item_name} is available!")
            call_user()
            is_on = False
            print(f"===MONITOR STOPPED ON {host_name}===")
            hook.send(f"===MONITOR STOPPED ON {host_name}===")
        else:
            print(f"[{current_time}] [{len(products)}]: Product/s not yet available.")
            aws_hook.send(
                f"[{current_time}] [{len(products)}]: Product/s not yet available."
            )
            time.sleep(standby_interval)
    except KeyboardInterrupt:
        print(f"===MONITOR INTERRUPTED ON {host_name}===")
        hook.send(f"===MONITOR INTERRUPTED ON {host_name}===")
        break
