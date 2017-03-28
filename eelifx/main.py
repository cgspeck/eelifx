#!/usr/bin/env python3
import sys
import json
import asyncio
import async_timeout
from functools import partial

import aiolifx
import aiohttp

from bulbs import Bulbs
from luacode import luacode
from ship import Ship

UDP_BROADCAST_PORT = 56700


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_ship_status(session, url):
    with async_timeout.timeout(10):
        async with session.post(url, data=luacode()) as response:
            return await response.text()


async def print_status(loop, bulbs):
    print(MyBulbs.bulbs)
    session = aiohttp.ClientSession()
    html = await get_ship_status(session, 'http://localhost:8080/exec.lua')
    try:
        ship_data = json.loads(html)
    except json.JSONDecodeError:
        print('Unable to parse EmptyEpsilon response')
    else:
        if 'ERROR' in ship_data.keys():
            print('Error returned by EmptyEpsilon:%s' % ship_data['ERROR'])
            print('Executed LUA:\n---%s---' % luacode())
        else:
            try:
                ship.update(ship_data)
            except Exception as e:
                raise
            else:
                print(ship)

    session.close()
    await asyncio.sleep(5)
    asyncio.ensure_future(print_status(loop, bulbs))


MyBulbs = Bulbs()
ship = Ship()
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(aiolifx.LifxDiscovery, loop, MyBulbs),
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
