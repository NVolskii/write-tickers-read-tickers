import requests
from random import random
import time
import aiohttp
import asyncio

TICK_EP = 'http://127.0.0.1:5000/ticker/'
TICK_VAL_EP = 'http://127.0.0.1:5000/ticker_value/'


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

def generate_tickers():
    tickers = [f'ticker_{i:02}' for i in range(100)]
    res = []
    for ticker in tickers:
        resp = requests.post(TICK_EP, json={"tickername": ticker}).json()
        res.append((resp.get('id'), resp.get('val')))
    print(res)
    return res


async def main():
    tickers = generate_tickers()
    async with aiohttp.ClientSession() as s:
        while True:
            tickers = [(t[0], t[1] + generate_movement()) for t in tickers]
            for t in tickers:
                await s.post(TICK_VAL_EP, json={'ticker_id': t[0], 'ticker_value': t[1]})
            time.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
