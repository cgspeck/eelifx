import logging

import yaml

DEFAULT_CONFIG = {
    'poll_interval': 20,
    'wait_for_members': True,
    'groups': [
        {
            'match': '.*',
            'max_luminance': 0.29,
            'colour_temp': 3500,
            'base_state': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_colour("white")
lifx_commanders[lc_index].set_luminance(1.0)
''',
            'rules': [
                {
                    'statement': 'ship.energy > 0.6',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_luminance(1.0)
''',
                },
                {
                    'statement': 'ship.energy < 0.6 and ship.energy > 0.15',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_luminance(0.6)
''',
                },
                {
                    'statement': 'ship.energy > 0.15 and ship.energy > 0.05',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_luminance(0.1)
''',
                },
                {
                    'statement': 'ship.energy > 0.05',
                    'effect': 'lifx_commanders[lc_index].set_power(False)',
                },
                {
                    'statement': "ship.alert_level == 'normal'",
                    'effect': "lifx_commanders[lc_index].set_colour('white')",
                },
                {
                    'statement': "ship.alert_level == 'YELLOW ALERT'",
                    'effect': "lifx_commanders[lc_index].set_colour('yellow')",
                },
                {
                    'statement': "ship.alert_level == 'RED ALERT'",
                    'effect': "lifx_commanders[lc_index].set_colour('red')",
                },
                {
                    'statement': 'ship.health < 0.2 and ship.health > 0.1',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_effect("flicker")
''',
                },
                {
                    'statement': 'ship.health < 0.1',
                    'effect': 'lifx_commanders[lc_index].set_power(False)',
                },
            ]
        },
    ],
}


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter('%(asctime)s:%(name)s:[%(levelname)s]: %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


def display_config():
    print(yaml.dump(DEFAULT_CONFIG, default_flow_style=False))
