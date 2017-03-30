#!/usr/bin/env python3
import sys
import asyncio
import logging
from functools import partial

import aiolifx

from bulbs import Bulbs
from lifx_commander import LifxCommander
from config import DEFAULT_CONFIG, setup_logging
from compiler import compile_items

setup_logging()

config = DEFAULT_CONFIG

logging.info('Compiling base states')
compile_items(config['groups'], 'base_state')

for group in config['groups']:
    logging.info('Compiling rule statements')
    compile_items(group['rules'], 'statement')
    logging.info('Compiling effects statements')
    compile_items(group['rules'], 'effect')

UDP_BROADCAST_PORT = 56700
poll_interval = config['poll_interval']
MAX_LUMINANCE = config['groups'][0]['max_luminance']


async def group_test(loop, bulbs, lifx_commander, group, rule):
    logging.info(
        "Resetting lights to base state"
    )
    exec(config['groups'][group]['base_state_compiled'])
    lifx_commander.reset()
    await asyncio.sleep(poll_interval)
    logging.info(
        "[Group %s][Rule %s] Running block for condition '%s'",
        group,
        rule,
        config['groups'][group]['rules'][rule]['statement']
    )
    exec(config['groups'][group]['rules'][rule]['effect_compiled'])
    lifx_commander.reset()
    await asyncio.sleep(poll_interval)
    if rule == len(config['groups'][group]['rules']):
        rule = 0
        if group == len(config['groups']):
            group = 0
        else:
            group += 1
    else:
        rule += 1

    asyncio.ensure_future(group_test(loop, bulbs, lifx_commander, group, rule))


MyBulbs = Bulbs()
lifx_commander = LifxCommander(poll_interval, max_luminance=MAX_LUMINANCE)
loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
            partial(aiolifx.LifxDiscovery, loop, MyBulbs),
            local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
        )

try:
    server = loop.create_task(coro)
    asyncio.ensure_future(group_test(loop, MyBulbs, lifx_commander, 0, 0))
    print("Use Ctrl-C to quit")
    loop.run_forever()
except:
    pass
finally:
    server.cancel()
    loop.remove_reader(sys.stdin)
    loop.close()
