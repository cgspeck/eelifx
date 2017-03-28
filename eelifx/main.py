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

@coroutine
def fetch(session, url):
    with aiohttp.Timeout(10):
        response = yield from session.get(url)
        try:
            if response.status != 200:
                print('Error connecting to %s' % url)
            return (yield from response.text())
        finally:
            if sys.exc_info()[0] is not None:
                # on exceptions, close the connection altogether
                response.close()
            else:
                yield from response.release()

# @coroutine
async def print_status(loop, bulbs):
    print(MyBulbs.bulbs)
    session = aiohttp.ClientSession()
    # resp = await(fetch(session, 'https://api.github.com/events'))
    # print(resp)
    # loop.run_until_complete(main(loop))
    await main(loop)
    await asyncio.sleep(5)
    # sleep(5)
    session.close()
    asyncio.ensure_future(print_status(loop, bulbs))
    # loop.call_later(5, print_status, loop, bulbs)


MyBulbs = Bulbs()
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(alix.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )



async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'http://date.jsontest.com/')
        print(html)


try:
    # loop.add_reader(sys.stdin, readin)
    server = loop.create_task(coro)
    # loop.call_soon(print_status, loop, MyBulbs)
    asyncio.ensure_future(print_status(loop, MyBulbs))
    # loop.call_soon(main, loop)
    print("Hit \"Enter\" to start")
    print("Use Ctrl-C to quit")
    loop.run_forever()
    # loop.run_until_complete(main(loop))
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
