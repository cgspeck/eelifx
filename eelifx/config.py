import logging

DEFAULT_CONFIG = {
    'poll_interval': 20,
    'groups': [
        {
            'match': '.*',
            'max_luminance': 1.0,
            'base_state': '''
lifx_commander.set_power(True)
lifx_commander.set_colour("white")
lifx_commander.set_luminance(1.0)
''',
            'rules': [
                {
                    'statement': 'ship.energy > 0.6',
                    'effect': '''
lifx_commander.set_power(True)
lifx_commander.set_luminance(1.0)
''',
                },
                {
                    'statement': 'ship.energy < 0.6 and ship.energy > 0.15',
                    'effect': '''
lifx_commander.set_power(True)
lifx_commander.set_luminance(0.6)
''',
                },
                {
                    'statement': 'ship.energy > 0.15 and ship.energy > 0.05',
                    'effect': '''
lifx_commander.set_power(True)
lifx_commander.set_luminance(0.1)
''',
                },
                {
                    'statement': 'ship.energy > 0.05',
                    'effect': 'lifx_commander.set_power(False)',
                },
                {
                    'statement': "ship.alert_level == 'normal'",
                    'effect': "lifx_commander.set_colour('white')",
                },
                {
                    'statement': "ship.alert_level == 'YELLOW ALERT'",
                    'effect': "lifx_commander.set_colour('orange')",
                },
                {
                    'statement': "ship.alert_level == 'RED ALERT'",
                    'effect': "lifx_commander.set_colour('red')",
                },
                {
                    'statement': 'ship.health < 0.2 and ship.health > 0.1',
                    'effect': '''
lifx_commander.set_power(True)
lifx_commander.set_effect("flicker")
''',
                },
                {
                    'statement': 'ship.health < 0.1',
                    'effect': 'lifx_commander.set_power(False)',
                },
            ]
        },
    ],
}


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s:%(name)s:[%(levelname)s]: %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
