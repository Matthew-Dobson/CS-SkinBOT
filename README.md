# CS Skin Marketplace Monitor

A Python project for monitoring CS skin marketplace listings and comparing listed prices against external market reference prices.

The script fetches recent listings from the SkinBaron API, checks estimated market value using the PriceEmpire API, and applies a simple profitability rule to decide whether an item may be worth purchasing. It also includes desktop and iOS notification logic for purchase attempts, successes, and failures.

## Features

- Fetches recent CS skin listings from SkinBaron
- Retrieves reference price data from PriceEmpire
- Compares listed price against estimated market value
- Applies simple purchase-decision logic
- Sends desktop notifications using `notify-py`
- Sends iOS notifications through Pushover
- Includes basic API/network error handling

## Project Structure

```text
CS-SkinBOT/
├── README.md
└── skinBot.py
