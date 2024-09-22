# Shopify Monitor and Auto-Purchase Scripts

This repository contains two Python scripts: 

1. **call_remote.py**: Monitors a Shopify store for specific products and sends notifications via Discord and Twilio calls when a desired product becomes available.
2. **shopifyshopper.py**: Automates the process of purchasing products from a Shopify store using Selenium and integrates with Twilio to notify the user via calls when a purchase attempt is made.

## Features

- **Product Monitoring**: Continuously checks a Shopify store's products JSON for the availability of specified items.
- **Notifications**: Sends notifications to Discord via webhooks and calls the user using Twilio when a product becomes available.
- **Auto-Purchase**: Automatically adds the product to the cart, applies a discount code, fills in shipping information, and proceeds to checkout.
- **Error Handling**: Includes graceful handling of interruptions (e.g., keyboard interrupts) and logs events to Discord for transparency.

---

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Selenium WebDriver for Chrome (`chromedriver`)
- Twilio account (for sending call notifications)
- Discord webhook URL (for sending notifications)

### Clone the Repository

```bash
git clone https://github.com/your-repository/shopify-monitor.git
cd shopify-monitor
```

### Install Required Libraries

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configuration

Modify the following parameters in both `call_remote.py` and `shopifyshopper.py` to suit your needs:

#### Main Configuration
- `json_url`: URL of the Shopify store's product JSON.
- `wanted_items`: List of products to monitor.
- `discord_webhook`: URL of your Discord webhook for sending notifications.
- `standby_interval`: Time (in seconds) between product checks.

#### Twilio Configuration
- `account_sid`: Twilio account SID.
- `auth_token`: Twilio authentication token.
- `phone_number`: Your phone number to receive calls.
- `twilio_number`: Twilio phone number for sending calls.

#### Shipping Info (for `shopifyshopper.py`)
- Add your shipping information (email, name, address, etc.) under the `shipping_info` section.

### Running the Scripts

1. **Run the Monitor Script (`call_remote.py`)**

```bash
python3 call_remote.py
```

This will initiate monitoring for your desired products and notify you via Discord and Twilio when available.

2. **Run the Auto-Purchase Script (`shopifyshopper.py`)**

```bash
python3 shopifyshopper.py
```

This script will automatically attempt to purchase the specified products from the Shopify store.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please reach out via email: [mico.rigunay@gmail.com](mailto:mico.rigunay@gmail.com).