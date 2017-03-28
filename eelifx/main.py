#!/usr/bin/env python3
import sys
import asyncio
from asyncio import coroutine
import aiolifx as alix
import aiohttp
import async_timeout

from functools import partial
from time import sleep
from bulbs import Bulbs

UDP_BROADCAST_PORT = 56700


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'http://date.jsontest.com/')
        print(html)


async def print_status(loop, bulbs):
    print(MyBulbs.bulbs)
    session = aiohttp.ClientSession()
    await main(loop)
    session.close()
    await asyncio.sleep(5)
    asyncio.ensure_future(print_status(loop, bulbs))


MyBulbs = Bulbs()
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(alix.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )

try:
    server = loop.create_task(coro)
    asyncio.ensure_future(print_status(loop, MyBulbs))
    print("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
