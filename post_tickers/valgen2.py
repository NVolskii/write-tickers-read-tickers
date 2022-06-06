import requests
from random import random
import time

TICK_EP = 'http://127.0.0.1:5000/ticker/'
TICK_VAL_EP = 'http://127.0.0.1:5000/ticker_value/'

def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

def generate_tickers():
    tickers = [f'ticker_{i:02}' for i in range(100)]
    res = []
    for ticker in tickers:
        res.append(
            (requests.post(TICK_EP, json={"tickername": ticker}).json()['id'], 0)
        )
    print(res)
    return res


def main():
    tickers = generate_tickers()
    while True:
        tickers = [(tick, val + generate_movement()) for (tick, val) in tickers]
        for tick in tickers:
            requests.post(TICK_VAL_EP, json={'ticker_id': tick[0], 'ticker_value': tick[1]})
        time.sleep(1)

if __name__ == '__main__':
    main()
