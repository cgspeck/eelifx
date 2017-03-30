#!/usr/bin/env python3
import sys
import json
import asyncio
import logging
import async_timeout
from functools import partial

import aiolifx
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

from bulbs import Bulbs
from luacode import luacode
from ship import Ship
from lifx_commander import LifxCommander
from config import DEFAULT_CONFIG, setup_logging

setup_logging()
config = DEFAULT_CONFIG

UDP_BROADCAST_PORT = 56700
poll_interval = config['poll_interval']
MAX_LUMINANCE = config['groups'][0]['max_luminance']

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_ship_status(session, url):
    with async_timeout.timeout(10):
        async with session.post(url, data=luacode()) as response:
            return await response.text()


async def print_status(loop, bulbs, lifx_commander):
    logging.debug(MyBulbs.bulbs)
    session = aiohttp.ClientSession()

    html = None
    try:
        html = await get_ship_status(session, 'http://localhost:8080/exec.lua')
    except ClientConnectorError as e:
        logging.warn("Unable to connect to EmptyEpsilon, is its http server running?")
        logging.warn(e)

    ship_data = None

    if html:
        try:
            ship_data = json.loads(html)
        except json.JSONDecodeError:
            logging.warning('Unable to parse EmptyEpsilon response')
        else:
            if 'ERROR' in ship_data.keys():
                logging.critical('Error returned by EmptyEpsilon:%s' % ship_data['ERROR'])
                logging.critical('Executed LUA:\n---%s---' % luacode())
                ship_data = None

    if ship_data:
        try:
            ship.update(ship_data)
        except Exception as e:
            raise
        else:
            logging.debug(ship)

    session.close()
    await asyncio.sleep(poll_interval)
    asyncio.ensure_future(print_status(loop, bulbs, lifx_commander))


MyBulbs = Bulbs()
ship = Ship()
lifx_commander = LifxCommander(poll_interval, max_luminance=MAX_LUMINANCE)
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(aiolifx.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )


try:
    server = loop.create_task(coro)
    asyncio.ensure_future(print_status(loop, MyBulbs, lifx_commander))
    logging.info("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
