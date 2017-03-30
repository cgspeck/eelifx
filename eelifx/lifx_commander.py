import re
import logging
from functools import wraps

from colour import Color


def run_once(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if f.__name__ in args[0]._command_stack:
            return None

        return f(*args, **kwds)
    return wrapper


class LifxCommander():
    def __init__(self, poll_interval, max_luminance, target_group='.*'):
        self._poll_interval = poll_interval
        self._max_luminance = max_luminance
        self._command_stack = {}
        self._supported_effects = ['none', 'strobe', 'flicker']
        self._target_group = re.compile(target_group, flags=re.I)

    def reset(self):
        self._command_stack = {}

    @run_once
    def set_colour(self, val):
        logging.info('setting colour')
        self._command_stack['set_colour'] = val

    @run_once
    def set_intensity(self, val):
        logging.info('setting intensity')
        self._command_stack['set_intensity'] = val

    @run_once
    def set_effect(self, val):
        assert val in self._supported_effects
        logging.info('setting effect')
        self._command_stack['set_effect'] = val

    @run_once
    def set_luminance(self, val):
        logging.info('setting luminance')
        self._command_stack['set_luminance'] = val

    def set_power(self, val):
        '''
        Can be called as many times as required but latches off if called with false
        '''
        if 'set_power' in self._command_stack and not self._command_stack['set_power']:
            return

        logging.info('setting power')
        self._command_stack['set_power'] = val

    def apply(self, blubs):
        command_stack = self._command_stack
        target_bulbs = [bulb for bulb in blubs if self._target_group.match(bulb)]
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
                m_colour = Color(command_stack['colour'])

                if m_colour.luminance > self._max_luminance:
                    m_colour.luminance = self._max_luminance

            if 'set_luminance' in command_stack:
                m_colour.luminance = m_colour.luminance * command_stack['set_luminance']

            #  color is [Hue, Saturation, Brightness, Kelvin], duration in ms
            #  def set_color(self, value, callb=None, duration=0, rapid=False):
            bulb.set_color([
                int(round((float(m_colour.hue)*65535.0)/1.0)),
                int(round((float(m_colour.saturation)*65535.0)/1.0)),
                int(round((float(m_colour.luminance)*65535.0)/1.0)),
                3500
            ])
