import math
from notifypy import Notify
import http.client, urllib
import requests
import json
import time


def item_check(a,b): #function - which returns true if the item it was ran on is a "buy" and false if it is a "leave"
    if a < b:
        return True
    else:
        return False
    
def notification(): #function - which sends ios and desktop notification

    # Create a notification object
    notification = Notify()

    # Set the title and message for the notification
    notification.title = "Buy alert"
    notification.message = "A buyable item has been added to your basket."

    # Display the notification
    notification.send()

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
    "token": "ai9ktjpiiyjrg1viscw9o5tmzqzzbd",
    "user": "usoxvhzp5co1ek5xveoxmthpsia54i",
    "message": "A buyable item has been added to your basket",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def price_empire_from_market_hash_name(market_hash): #function - which returns the price empire price of any item given its market hash name

    def change_market_name_into_url(market_hash_name): # function - which returns the price empire api url for any item given its market hash name

        encoded_market_name = urllib.parse.quote(market_hash_name)

        item_url = "https://api.pricempire.com/v2/items/" +encoded_market_name+"?api_key=4f671762-dd61-4ad0-a1a9-f7e1ae8d5a67&currency=USD&source=buff_buy"

        return item_url

    def price_empire_item_price(api_url): # function - which returns the price empire price of the item given in the api_url in dollars

        # Replace 'your_api_key_here' with your actual API key
        api_key = '4f671762-dd61-4ad0-a1a9-f7e1ae8d5a67'

        # Set up the headers with your API key
        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        # Make the request to the API
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Print the data or process it as needed

            item_price = data['item']['prices']['buff163_quick']['price'] #extracting the integer value of the price from the json

            def add_decimal_point(number):
                return number / 100.0
            
            item_price_formatted = add_decimal_point(item_price)


        else:
            # Print the error if the request was not successful
            print(f'Error: {response.status_code} - {response.text}')

        return item_price_formatted

    url = change_market_name_into_url(market_hash)

    return price_empire_item_price(url)

def skin_baron(): #function - which returns the price, quality and name of any item listed on skin baron

    def skin_baron_item_listed():
        
        url = "https://api.skinbaron.de/NewestItems"
        payload = json.dumps({
            "apikey": "3511225-ac864ae1-15e5-48de-af05-81362a249a0b",
            "appId": 730,
            "size": 1
        })
        headers = {
            'Content-Type': 'application/json',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("POST",url, headers=headers, data=payload)
            
        if response.status_code != 200:
            exit()
        else:
            # Parse the JSON response
            data = response.json()

            return data
            
    def get_name(dictionary):
        try:
            name = dictionary['newestItems'][0]['itemName']
            return name
        except KeyError:
            return None
        
    def get_price(dictionary):
        try:
            price = dictionary['newestItems'][0]['itemPrice']
            return price
        except KeyError:
            return None
        
    def get_quality(dictionary):
        try:
            price = dictionary['newestItems'][0]['exteriorName']
            return price
        except KeyError:
            return None

    item = skin_baron_item_listed()
    name = str(get_name(item))
    price = get_price(item)
    quality = str(get_quality(item))

    variable_price = 5


    if get_price(item) == None or get_quality(item) == None:
        print(f"{name} is not eligible")
        return None

    elif price >= variable_price:
        return f"{name}",f"{price}",f"{quality}"
    
    else:
        print(f"{name} price is too low")
        return None

while True:
    if skin_baron() != None:
        item_name = f"{skin_baron()[0]} ({skin_baron()[2]})"
        baron_price = skin_baron()[1]
        empire_price = price_empire_from_market_hash_name(item_name) * 0.92 

        print(f"{item_name} is listed for {baron_price} euros on skin baron - item is worth {empire_price} euros")

        if item_check(baron_price,empire_price) == True:
            notification()
            time.sleep(30)
        else:
            time.sleep(30)

    else:
        time.sleep(30)






#to install for tim: update pip then install notifypy - all through the cmd
#to install for tim: create him a user code for his phone on the pushover api website
#make tim update euro price every 5 days or smth
#show tim where to edit the minimum of 50 euros


