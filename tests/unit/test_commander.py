# import re
# from unittest.mock import Mock
#
import pytest


from eelifx.lifx_commander import LifxCommander


@pytest.fixture
def lifx_commander():
    return LifxCommander()


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


def test_has_members(bulb_container, standard_bulbs):
    lifx_commander = LifxCommander(
        target_group='ship.*'
    )
    bulb_container.bulbs = []
    assert not lifx_commander.has_members(bulb_container)
    bulb_container.bulbs = standard_bulbs[4:2]
    assert not lifx_commander.has_members(bulb_container)
    bulb_container.bulbs = standard_bulbs
    assert lifx_commander.has_members(bulb_container)


testdata_calculate_peroids_and_cycles = [
    (5, 25, 40, 125),
    (20, 25, 40, 500),
    (20, 1, 1000, 20),
    (20, 0.5, 2000, 10),
]


@pytest.mark.parametrize('poll_interval,requested_hz,expected_period,expected_cycles,', testdata_calculate_peroids_and_cycles)
def test_calculate_period_and_cycles(poll_interval, requested_hz, expected_period, expected_cycles):
    lifx_commander = LifxCommander(
        poll_interval=poll_interval,
        target_group='ship.*'
    )

    assert lifx_commander._calculate_peroid_and_cycles(requested_hz)[0] == expected_period
    assert lifx_commander._calculate_peroid_and_cycles(requested_hz)[1] == expected_cycles
