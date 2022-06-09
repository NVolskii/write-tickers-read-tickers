from dotenv import load_dotenv
import requests
from random import random
import aiohttp
import asyncio
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

def generate_tickers():
    tickers = [f'ticker_{i:02}' for i in range(100)]
    res = []
    for ticker in tickers:
        res.append(requests.post(getenv('TICK_EP'), json={"tickername": ticker}).json())
    print(res)
    return res


async def post_one_by_one():
    # TODO: the first value is not added to db. If it is initial value it should be.
    tickers = generate_tickers()
    async with aiohttp.ClientSession() as s:
        while True:
            period = asyncio.create_task(asyncio.sleep(1))
            for ticker in tickers:
                await s.post(getenv('TICK_VAL_EP'), json=ticker)
                ticker['ticker_value'] += generate_movement()
            await period


async def post_batch():
    tickers = generate_tickers()
    async with aiohttp.ClientSession() as s:
        while True:
            period = asyncio.create_task(asyncio.sleep(1))
            res = asyncio.create_task(s.post(getenv('TICK_VAL_BATCH_EP'), json=tickers))
            tickers = [
                {
                    'ticker_id': t.get('ticker_id'),
                    'ticker_value': t.get('ticker_value') + generate_movement()
                } for t in tickers
            ]
            await res
            await period

if __name__ == '__main__':
    # asyncio.run(post_one_by_one())
    asyncio.run(post_batch())