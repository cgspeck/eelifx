#!/usr/bin/env python3
import sys
import asyncio as aio
import aiolifx as alix
from functools import partial
from time import sleep
from bulbs import Bulbs

UDP_BROADCAST_PORT = 56700



def print_status(loop, bulbs):
    print(MyBulbs.bulbs)
    loop.call_later(5, print_status, loop, bulbs)


MyBulbs = Bulbs()
loop = aio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(alix.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )

try:
    # loop.add_reader(sys.stdin, readin)
    server = loop.create_task(coro)
    loop.call_soon(print_status, loop, MyBulbs)
    print("Hit \"Enter\" to start")
    print("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
