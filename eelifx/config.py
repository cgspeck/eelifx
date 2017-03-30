DEFAULT_CONFIG = {
    'poll_interval': 20,
    'groups': [
    {
        'match': '.*',
        'max_luminance': 1.0,
        'rules': [
        {
            'statement': 'ship.energy > 0.6',
            'effect': [
                'lifx_commander.set_power(True)',
                'lifx_commander.set_luminance(1.0)',
            ]
        },
        {
            'statement': 'ship.energy < 0.6 && ship.energy > 0.15',
            'effect': [
                'lifx_commander.set_power(True)',
                'lifx_commander.set_luminance(0.6)',
            ]
        },
        {
            'statement': 'ship.energy > 0.15 && ship.energy > 0.05',
            'effect': [
                'lifx_commander.set_power(True)',
                'lifx_commander.set_luminance(0.1)',
            ]
        },
        {
            'statement': 'ship.energy > 0.05',
            'effect': [
                'lifx_commander.set_power(False)',
            ]
        },
        {
            'statement': "ship.alert_level == 'normal'",
            'effect': [
                "lifx_commander.set_colour('white')",
            ]
        },
        {
            'statement': "ship.alert_level == 'YELLOW ALERT'",
            'effect': [
                "lifx_commander.set_colour('orange')",
            ]
        },
        {
            'statement': "ship.alert_level == 'RED ALERT'",
            'effect': [
                "lifx_commander.set_colour('red')",
            ]
        },
        {
            'statement': 'ship.health < 0.2 && ship.health > 0.1',
            'effect': [
                'lifx_commander.set_power(True)',
                'lifx_commander.set_effect("flicker")',
            ]
        },
        {
            'statement': 'ship.health < 0.1',
            'effect': [
                'lifx_commander.set_power(False)',
            ]
        },
        ]
    },
    ],
}
