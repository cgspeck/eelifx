#!/usr/bin/env python3
import sys
import asyncio
import logging
from functools import partial

import aiolifx

from eelifx.bulbs import Bulbs
from eelifx.config import DEFAULT_CONFIG, setup_logging
from eelifx.util import wait_for_members, marshal_commanders

setup_logging(level=logging.DEBUG)

config = DEFAULT_CONFIG

UDP_BROADCAST_PORT = 56700
poll_interval = config['poll_interval']

MyBulbs = Bulbs()

lifx_commanders = marshal_commanders(config)
#  Initialise the event loop
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(aiolifx.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )
try:
    server = loop.create_task(coro)
    asyncio.ensure_future(wait_for_members(loop, MyBulbs, lifx_commanders, poll_interval, config))
    print("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
