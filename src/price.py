#!/usr/bin/env python3

import requests
import sys


URL = "https://api.e-money.com/v1/rate/{}/usd"

def get(symbol):
    usd_price = requests.get(URL.format(symbol)).content
    return float(usd_price)
    
if __name__ == "__main__":
    try:
        print(get(sys.argv[1]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)