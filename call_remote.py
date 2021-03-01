#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 1 04:20:00 2021

@author: mickosis
"""

import requests
import json
import time
import os
from twilio.rest import Client
from dhooks import Webhook
from datetime import datetime

# Main Configuration

json_url = "https://shopifywebsite.com/products.json"
wanted_item = "Product Name XL"
hook = Webhook("https://discord.com/api/webhooks/")
aws_hook = Webhook("https://discord.com/api/webhooks/")
standby_interval = 30
account_sid = "account_sid"
auth_token = "auth_token"
phone_number = "phone_number"
twilio_number = "twilio_number"
twilio_url = "http://demo.twilio.com/docs/voice.xml"

# Main Functions


def has_item():
    r = requests.get(json_url)
    products = json.loads((r.text))["products"]
    for product in products:
        product_name = product["title"]
        if product_name == wanted_item:
            return True
    else:
        return False


def call_user():
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=phone_number,
        from_=twilio_number,
        url=twilio_url,
    )
    print(call.sid)

    # Send Discord Notification
    while True:
        print("Please complete payment!")
        hook.send("Please complete payment!")
        time.sleep(3)


# Main Program

# Monitoring Loop
print("====================MONITOR INITIATED====================")
hook.send("====================MONITOR INITIATED====================")
is_on = True
while is_on:
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if has_item():
            print("Product is Available!")
            hook.send("Product is available!")
            call_user()
            is_on = False
        else:
            print(current_time + " Product Not Yet Available")
            aws_hook.send(current_time + " Product Not Yet Available")
            time.sleep(standby_interval)
    except KeyboardInterrupt:
        print("====================MONITOR STOPPED====================")
        hook.send("====================MONITOR STOPPED====================")
        break
