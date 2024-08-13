import math
from notifypy import Notify
import http.client, urllib
import requests
import json
import time



def notification(): #function - which sends ios and desktop notification

    #notification keys for matt and tim's phones
    tim_notification_key = "utavdrr9v5ewr9oqtyyxas1yum97io"
    matt_notification_key = "utfu9mkpnagz1iu8c9b1s3iticobt3"

    # Create a desktop notification object
    notification = Notify()

    # Set the title and message for the desktop notification
    notification.title = "Buy alert"
    notification.message = "A buyable item has been added to your basket."

    # Display the desktop notification
    notification.send()


    #ios notification api
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
    "token": "ai9ktjpiiyjrg1viscw9o5tmzqzzbd",
    "user": tim_notification_key,
    "message": "A buyable item has been added to your basket",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def skin_baron(): #function - which returns an array contatining the name, price, wear
                    #and stickers of the most recently listed item greater than 50 euro
    
    #api keys for tim and matt for skinbaron
    matt_skinbaron_api_key = "3511225-47480af6-d14e-43ac-99cb-938351b1c96b"
    tim_skinbaron_api_key = "2131850-7d3bd279-c44d-4965-80ad-4d1b5cccf2a5"

    def skinbaron_listing():

        #skinbaron api returns the most recent item listed greater than 50 euro
        url = "https://api.skinbaron.de/Search"
        payload = json.dumps({
                    "apikey": tim_skinbaron_api_key,
                    "appid": 730,
                    "min": 50,
                    "max": 100000,
                    "items_per_page": 1
                    })
        headers = {
            'Content-Type': 'application/json',
            'x-requested-with': 'XMLHttpRequest'
        }

        #response is parsed into a json
        response = requests.request("POST",url, headers=headers, data=payload)
        data = response.json()

        return data
    
    for sale in skinbaron_listing()['sales']:
        market_name = sale['market_name']
        price = sale['price']
        wear = sale['wear']
        stickers = sale['stickers']

    return market_name , price , wear , stickers

def price_empire(name_baron): #function - which returns the empire price of item from name

    tim_empire_api = "44b5ace6-5b89-43bf-9669-b4038bb58aee"
    matt_empire_api = "4f671762-dd61-4ad0-a1a9-f7e1ae8d5a67"

    def name_to_url(name): #parses market hash name into the url for the empire api

        encoded_market_name = urllib.parse.quote(name)
        item_url = "https://api.pricempire.com/v2/items/" +encoded_market_name+"?api_key="+tim_empire_api+"&currency=USD&source=buff_buy"
        return item_url
    
    def price_empire_price(api_url): #returns json with price of item

        #return api price
        headers = {
            'Authorization': f'Bearer {tim_empire_api}'
        }
        response = requests.get(api_url, headers=headers)

        #parse and return json
        data = response.json()
        return data

    #return json of price
    url = name_to_url(name_baron)
    price_json = price_empire_price(url)

    #index's price from the json
    item_price = price_json['item']['prices']['buff163_quick']['price']

    #formats price properly
    item_price = item_price / 100

    return item_price

def item_check(a,b): #function - which returns true if the item it was ran on is a "buy" and false if it is a "leave"
    if float(a) < float(b) * 0.85:
        return True
    else:
        return False


while True:

    #loops every 10 seconds to keep the variables updated
    if skin_baron() != None:
        name = skin_baron()[0]
        wear = skin_baron()[2]
        stickers = skin_baron()[3]

        baron_price = skin_baron()[1]
        empire_price = price_empire(name) * 0.916   
        price_difference_buy = empire_price - baron_price
        price_difference_sell = baron_price - empire_price

        time.sleep(10)
    else:
        print("error with item listed on skinbaron")
        time.sleep(10)



    try:
        if item_check(baron_price,empire_price) == True:
            notification()
            
            print(f"An item named {name} has been listed on SkinBaron and meets the requirements.\n")
            print(f"Name: {name}")
            print(f"Price: {baron_price}")
            print(f"Wear: {wear}")
            print(f"Stickers: {stickers}\n")
            print(f"It is listed for {price_difference_buy:.2f} cheaper than it is worth. \n")

            time.sleep(10)

        else:
            print(f"An item named {name} has been listed on SkinBaron but does not meet the requirements.\n")
            print(f"Name: {name}")
            print(f"Price: {baron_price}")
            print(f"Wear: {wear}")
            print(f"Stickers: {stickers}\n")
            print(f"It is listed for {price_difference_sell:.2f} more than it is worth. \n")

            time.sleep(10)

    except Exception as e:
            # Print the error message
            print(f"An error occurred: {e}. Retrying in 10 seconds...")

            # Wait for 10 seconds before retrying
            time.sleep(10)
        

    

