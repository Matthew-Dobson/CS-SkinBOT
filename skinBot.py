from notifypy import Notify
import http.client, urllib
import requests
import json
import time

class Notifier:
    def __init__(self, notification_key):
        self.notification_key = notification_key

    def send_desktop_attempt_notification(self):
        notification = Notify()
        notification.title = "PURCHASE ATTEMPT"
        notification.message = "PURCHASE ATTEMPT - A profitable item has been listed and an attempt to purchase is being made."
        notification.send()

    def send_desktop_success_notification(self):
        notification = Notify()
        notification.title = "PURCHASE SUCCESS"
        notification.message = "PURCHASE SUCCESS - A profitable item has been successfully purchased."
        notification.send()

    def send_desktop_failure_notification(self):
        notification = Notify()
        notification.title = "PURCHASE FAILURE"
        notification.message = "PURCHASE FAILURE - There has been a purchase failure on a marketplace item."
        notification.send()

    def send_ios_attempt_notification(self):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode({
                "token": "your_pushover_token",  # Add Pushover token here
                "user": self.notification_key,
                "message": "PURCHASE ATTEMPT - A profitable item has been listed and an attempt to purchase is being made.",
            }),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()

    def send_ios_success_notification(self):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode({
                "token": "your_pushover_token",  # Add Pushover token here
                "user": self.notification_key,
                "message": "PURCHASE SUCCESS - A profitable item has been successfully purchased.",
            }),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()

    def send_ios_failure_notification(self):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode({
                "token": "your_pushover_token",  # Add Pushover token here
                "user": self.notification_key,
                "message": "PURCHASE FAILURE - There has been a purchase failure on a marketplace item.",
            }),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()


class Marketplace:

    def __init__(self, skinBaron_api_key, priceEmpire_api_key, skinBaron_base_url, priceEmpire_base_url):
        self.skinBaron_api_key = skinBaron_api_key
        self.priceEmpire_api_key = priceEmpire_api_key
        self.skinBaron_base_url = skinBaron_base_url
        self.priceEmpire_base_url = priceEmpire_base_url

    def fetch_latest_item(self):

        def skinbaron_listing():
            try:
                url = self.skinBaron_base_url
                payload = json.dumps({
                    "apikey": self.skinBaron_api_key,
                    "appid": 730,
                    "min": 1,
                    "max": 3,
                    "items_per_page": 1,
                    "stackable": False,
                })
                headers = {
                    "Content-Type": "application/json",
                    "x-requested-with": "XMLHttpRequest",
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                if response.status_code != 200:
                    print(f"SkinBaron API failed. Error Code: {response.status_code}")
                    return None

                data = response.json()

                if "sales" not in data:
                    print(f"Unexpected JSON format from SkinBaron: {data}")
                    return None

                for sale in data["sales"]:
                    market_name = sale["market_name"]
                    price = sale["price"]
                    sales_id = sale["id"]

                return market_name, price, sales_id

            except requests.exceptions.RequestException as e:
                print(f"Network error with SkinBaron: {e}")
                return None

            except ValueError as ve:
                print(f"Data error with SkinBaron: {ve}")
                return None

            except Exception as e:
                print(f"An unexpected error occurred with SkinBaron: {e}")
                return None

        def price_empire(name):
            encoded_market_name = urllib.parse.quote(name)
            item_url = (
                self.priceEmpire_base_url + encoded_market_name +
                "?api_key=" + self.priceEmpire_api_key + "&currency=EUR&source=buff_buy"
            )

            try:
                headers = {"Authorization": f"Bearer {self.priceEmpire_api_key}"}
                response = requests.get(item_url, headers=headers)

                if response.status_code != 200:
                    print(f"PriceEmpire API failed. Error Code: {response.status_code}")
                    return None

                data = response.json()

                item_price = data["item"]["prices"]["buff163_quick"]["price"]

                return item_price / 100

            except requests.exceptions.RequestException as e:
                print(f"Network error with PriceEmpire: {e}")
                return None

            except ValueError as ve:
                print(f"Data error with PriceEmpire: {ve}")
                return None

            except Exception as e:
                print(f"An unexpected error occurred with PriceEmpire: {e}")
                return None

        item_skinbaron_details = skinbaron_listing()

        if item_skinbaron_details is None:
            return None

        name = item_skinbaron_details[0]
        skinBaron_price = item_skinbaron_details[1]
        sale_id = item_skinbaron_details[2]

        priceEmpire_price = price_empire(name)

        return name, skinBaron_price, sale_id, priceEmpire_price


class BuyManager:
    def __init__(self, marketplace, notifier):
        self.marketplace = marketplace
        self.notifier = notifier

    def decide_and_buy(self):

        def is_worth_buying(listed_price, market_price):
            return float(listed_price) < float(market_price) * 2

        item_details = self.marketplace.fetch_latest_item()

        if item_details is None or None in item_details:
            print(f"Error fetching item details.")
            return

        name = item_details[0]
        skinBaron_price = item_details[1]
        sale_id = item_details[2]
        priceEmpire_price = item_details[3]

        if is_worth_buying(skinBaron_price, priceEmpire_price):
            self.notifier.send_ios_attempt_notification()
            self.notifier.send_desktop_attempt_notification()

            print(f"\nPURCHASE ATTEMPT")
            print(f"\nItem {name} is worth purchasing.")
            print(f"Listed for: {skinBaron_price} and worth {priceEmpire_price}")
            print(f"\n--------------------------------------------------------")  
            
            try:
                url = "https://api.skinbaron.de/BuyItems"
                payload = json.dumps({
                    "apikey": "your_skinbaron_api_key",  # Add SkinBaron API key here
                    "total": skinBaron_price,
                    "toInventory": True,
                    "saleids": [sale_id],
                })
                headers = {"Content-Type": "application/json", "x-requested-with": "XMLHttpRequest"}

                response = requests.post(url, headers=headers, data=payload)

                if response.status_code != 200:
                    raise Exception(f"Error with SkinBaron purchase: {response.status_code}")

                data = response.json()

                print(data)

                quit()

            except Exception as e:
                self.notifier.send_ios_failure_notification()
                self.notifier.send_desktop_failure_notification()
                print(f"Purchase failure: {e}")

            else:
                self.notifier.send_ios_success_notification()
                self.notifier.send_desktop_success_notification()
                print(f"Purchase success.")

        else:
            print(f"\nItem {name} is not worth purchasing.")
            print(f"Listed for: {skinBaron_price} and worth {priceEmpire_price}")
            print(f"\n--------------------------------------------------------")      


def main():
    marketplace = Marketplace(
        skinBaron_api_key="your_skinbaron_api_key",  # Add SkinBaron API key here
        priceEmpire_api_key="your_priceempire_api_key",  # Add PriceEmpire API key here
        skinBaron_base_url="https://api.skinbaron.de/Search",
        priceEmpire_base_url="https://api.pricempire.com/v2/items/"
    )

    notifier = Notifier(notification_key="your_notification_key")  # Add notification key here

    buy_manager = BuyManager(marketplace, notifier)

    while True:
        buy_manager.decide_and_buy()
        time.sleep(10)


if __name__ == "__main__":
    main()
