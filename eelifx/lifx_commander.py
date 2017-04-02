import re
import typing
import logging
from functools import wraps

from aiolifx import aiolifx
from colour import Color


def run_once(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if f.__name__ in args[0]._command_stack:
            return None

        return f(*args, **kwds)
    return wrapper


class LifxCommander():
    def __init__(self, poll_interval: int=20, max_luminance: float=1.0, target_group: str='.*', colour_temp: int=3500):
        self._poll_interval = poll_interval
        self._max_luminance = max_luminance
        self._command_stack = {}
        self._supported_effects = ['none', 'strobe', 'flicker']
        self._target_group = re.compile(target_group, flags=re.I)
        self._target_group_orig = target_group
        self._colour_temp = colour_temp

    def reset(self):
        self._command_stack = {}

    def set_colour(self, val):
        logging.debug('setting colour %s', val)
        self._command_stack['set_colour'] = val

    def set_effect(self, val):
        assert val in self._supported_effects
        logging.debug('setting effect, %s', val)
        self._command_stack['set_effect'] = val

    def set_luminance(self, val):
        logging.debug('setting luminance %s', val)
        self._command_stack['set_luminance'] = val

    def set_power(self, val):
        '''
        Can be called as many times as required but latches off if called with false
        '''
        if 'set_power' in self._command_stack and not self._command_stack['set_power']:
            return

        logging.debug(f'setting power to {val}')
        self._command_stack['set_power'] = val

    def has_members(self, bulbs: typing.Sequence[aiolifx.Light]) -> bool:
        res = len(list(bulbs.filter_group(self._target_group))) > 0
        logging.info(
            'Group %s has %s',
            self._target_group_orig,
            'at least one member' if res else 'not got any members'
        )
        return res

    def apply(self, bulbs):
        if len(self._command_stack) == 0:
            logging.warning('Apply called but no commands registered')
            return

        logging.debug('Candidate bulbs are %s' % bulbs)
        command_stack = self._command_stack

        target_bulbs = bulbs.filter_group(self._target_group)

        m_colour = None

        for bulb in target_bulbs:
            if 'set_power' in command_stack:
                # change bulb's power if it differs
                desired_state = command_stack['set_power']
                observed_state = True if bulb.get_power() == 65535 else False

                if observed_state != desired_state:
                    bulb.set_power(desired_state)

                if not desired_state:
                    next

            if 'set_colour' in command_stack:
                m_colour = Color(command_stack['set_colour'])
                logging.debug(
                    'Commanded colour is %s (%s)',
                    m_colour,
                    m_colour.hsl
                )
                logging.debug(m_colour.luminance)
                if m_colour.luminance > self._max_luminance:
                    logging.debug(
                        'Clipping colour\'s luminance to %s',
                        self._max_luminance
                    )
                    m_colour.luminance = self._max_luminance

            logging.debug(m_colour.luminance)
            if 'set_luminance' in command_stack:
                if m_colour:
                    m_colour.luminance = m_colour.luminance * command_stack['set_luminance']
                else:
                    logging.info('Unable to scale luminance without colour being set')

            logging.debug(
                'Scaled colour is %s (%s)',
                m_colour,
                m_colour.hsl
            )
            #  color is [Hue, Saturation, Brightness, Kelvin], duration in ms
            #  def set_color(self, value, callb=None, duration=0, rapid=False):
            bulb.set_color([
                int(round((float(m_colour.hue)*65535.0)/1.0)),
                int(round((float(m_colour.saturation)*65535.0)/1.0)),
                int(round((float(m_colour.luminance)*65535.0)/1.0)),
                self._colour_temp
            ])
