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
from lifx_commander import LifxCommander

UDP_BROADCAST_PORT = 56700
EE_POLL_INTERVAL = 5
MAX_LUMINANCE = 100

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_ship_status(session, url):
    with async_timeout.timeout(10):
        async with session.post(url, data=luacode()) as response:
            return await response.text()


async def print_status(loop, bulbs, lifx_commander):
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
                lifx_commander.set_hue(50)

    session.close()
    await asyncio.sleep(EE_POLL_INTERVAL)
    asyncio.ensure_future(print_status(loop, bulbs, lifx_commander))


MyBulbs = Bulbs()
ship = Ship()
lifx_commander = LifxCommander(EE_POLL_INTERVAL, max_luminance=MAX_LUMINANCE)
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(aiolifx.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )

try:
    server = loop.create_task(coro)
    asyncio.ensure_future(print_status(loop, MyBulbs, lifx_commander))
    print("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
