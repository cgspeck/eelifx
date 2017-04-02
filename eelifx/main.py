#!/usr/bin/env python3
import sys
import asyncio
import logging

from functools import partial

import aiolifx


from eelifx.config import DEFAULT_CONFIG, setup_logging
from eelifx.util import wait_for_members, marshal_commanders
from eelifx.bulbs import Bulbs

setup_logging(logging.DEBUG)
config = DEFAULT_CONFIG

UDP_BROADCAST_PORT = 56700

config['endpoint'] = 'http://localhost:8080/exec.lua'

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
    asyncio.ensure_future(
        wait_for_members(
            loop,
            MyBulbs,
            lifx_commanders,
            poll_interval,
            config,
            mode='run'
        )
    )
    logging.info("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
