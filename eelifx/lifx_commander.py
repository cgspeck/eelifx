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
    def __init__(self, ee_poll_interval, max_luminance, target_group='.*'):
        self._ee_poll_interval = ee_poll_interval
        self._max_luminance = max_luminance
        self._command_stack = {}
        self._supported_effects = ['none', 'breathe', 'flicker']
        self._target_group = re.compile(target_group, flags=re.I)

    def reset(self):
        self._command_stack = {}

    @run_once
    def set_hue(self, val):
        print('setting hue')
        self._command_stack['set_hue'] = val

    @run_once
    def set_intensity(self, val):
        print('setting intensity')
        self._command_stack['set_intensity'] = val

    @run_once
    def set_effect(self, val):
        assert val in self._supported_effects
        print('setting effect')
        self._command_stack['set_effect'] = val

    def apply(self, blubs):
        for bulb in bulbs:
            if re.match(bulb.group):
                if 'set_hue' in self._command_stack:
                    pass
