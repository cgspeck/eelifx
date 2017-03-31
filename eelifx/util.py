import sys
import typing
import asyncio
import logging
from copy import deepcopy
from pprint import pformat

from eelifx.bulbs import Bulbs
from eelifx.lifx_commander import LifxCommander


def compile_items(_list, item_key):
    for item in _list:
        if item_key not in item:
            logging.warning(
                "Could not find %s in object %s.",
                item_key,
                item
            )
            next
        try:
            item['%s_compiled' % item_key] = compile(item[item_key], '<string>', 'exec')
        except Exception as e:
            logging.exception("Unable to compile the following code to a python code object: %s" % pformat(item[item_key]))
            raise


async def wait_for_members(
    loop: asyncio.AbstractEventLoop,
    bulbs: Bulbs,
    lifx_commanders: typing.Sequence[LifxCommander],
    poll_interval: int,
    config: typing.Dict
):
    ok = True
    if 'wait_for_members' in config and config['wait_for_members']:
        logging.info('Checking to see if our groups have members yet')
        if not all([l.has_members(bulbs) for l in lifx_commanders]):
            ok = False
            logging.info(
                'At least one group has no members and wait_for_members is set to true, will retry in %s seconds.',
                poll_interval
            )
            # requeue check
            await asyncio.sleep(poll_interval)
            asyncio.ensure_future(wait_for_members(loop, bulbs, lifx_commanders, poll_interval, config))

    if ok:
        logging.info('At least one globe in each group is present, or wait_for_members is set to false.')
        logging.info('Compiling base states...')
        compile_items(config['groups'], 'base_state')

        groups = []

        for group in config['groups']:
            groups.append(deepcopy(group))
            logging.info('Compiling rule statements...')
            compile_items(groups[-1]['rules'], 'statement')
            logging.info('Compiling effects statements...')
            compile_items(groups[-1]['rules'], 'effect')

        asyncio.ensure_future(group_test(loop, bulbs, lifx_commanders, poll_interval, groups, 0, 0))


async def group_test(
    loop: asyncio.AbstractEventLoop,
    bulbs: Bulbs,
    lifx_commanders: typing.Sequence[LifxCommander],
    poll_interval: int,
    groups: typing.Dict,
    group: int,
    rule: int
):
    logging.info(
        "Resetting lights to base state"
    )
    lc_index = group
    exec(groups[group]['base_state_compiled'])
    lifx_commanders[lc_index].apply(bulbs)
    await asyncio.sleep(poll_interval)
    logging.info(
        "[Group %s][Rule %s] Running block for condition '%s'",
        group,
        rule,
        groups[group]['rules'][rule]['statement']
    )
    exec(groups[group]['rules'][rule]['effect_compiled'])
    lifx_commanders[lc_index].apply(bulbs)
    lifx_commanders[lc_index].reset()
    await asyncio.sleep(poll_interval)
    if rule == len(groups[group]['rules']):
        rule = 0
        if group == len(groups):
            group = 0
            rule = 0
        else:
            group += 1
    else:
        rule += 1

    asyncio.ensure_future(group_test(loop, bulbs, lifx_commanders, poll_interval, groups, group, rule))


def marshal_commanders(config):
    lifx_commanders = []
    for group in config['groups']:
        lifx_commanders.append(
            LifxCommander(
                poll_interval=config['poll_interval'],
                target_group=group['match'],
                max_luminance=group['max_luminance'],
                colour_temp=group['colour_temp']
            )
        )

    if len(lifx_commanders) == 0:
        logging.error('No groups have been defined in the config!')
        sys.exit(1)

    return lifx_commanders
