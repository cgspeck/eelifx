# import re
# from unittest.mock import Mock
#
import pytest


from eelifx.lifx_commander import LifxCommander


@pytest.fixture
def lifx_commander():
    return LifxCommander(poll_interval=20, max_luminance=1.0)


def test_last_call_to_set_colour_takes_preference(lifx_commander):
    lifx_commander.set_colour('red')
    lifx_commander.set_colour('green')
    assert lifx_commander._command_stack['set_colour'] == 'green'


def test_last_call_to_set_luminance_takes_preference(lifx_commander):
    lifx_commander.set_luminance(1.0)
    lifx_commander.set_luminance(0.1)
    assert lifx_commander._command_stack['set_luminance'] == 0.1


def test_last_call_to_set_effect_takes_preference(lifx_commander):
    lifx_commander.set_effect('strobe')
    lifx_commander.set_effect('flicker')
    assert lifx_commander._command_stack['set_effect'] == 'flicker'


def test_set_power_latches_off(lifx_commander):
    lifx_commander.set_power(True)
    lifx_commander.set_power(False)
    lifx_commander.set_power(True)

    assert lifx_commander._command_stack['set_power'] is False


def test_reset_clears_command_stack(lifx_commander):
    lifx_commander.set_colour('green')
    lifx_commander.set_luminance(0.1)
    lifx_commander.set_effect('flicker')
    lifx_commander.set_power(True)

    assert len(lifx_commander._command_stack) == 4

    lifx_commander.reset()
    assert len(lifx_commander._command_stack) == 0
