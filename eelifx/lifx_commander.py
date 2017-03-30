import re
from functools import wraps


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
        print('setting colour')
        self._command_stack['set_colour'] = val

    @run_once
    def set_intensity(self, val):
        print('setting intensity')
        self._command_stack['set_intensity'] = val

    @run_once
    def set_effect(self, val):
        assert val in self._supported_effects
        print('setting effect')
        self._command_stack['set_effect'] = val

    @run_once
    def set_luminance(self, val):
        print('setting luminance')
        self._command_stack['set_luminance'] = val

    def set_power(self, val):
        '''
        Can be called as many times as required but latches off if called with false
        '''
        print('setting power', val)

        if 'set_power' in self._command_stack and self._command_stack['set_power'] == False:
            return

        self._command_stack['set_power'] = val

    def apply(self, blubs):
        target_bulbs = [bulb for bulb in blubs if self._target_group.match(bulb)]

        for bulb in target_bulbs:
            if 'set_power' in self._command_stack:
                # change bulb's power if it differs
                if not self._command_stack['set_power']:
                    next

            if 'set_colour' in self._command_stack:
                pass

            if 'set_luminance' in self._command_stack:
                pass
