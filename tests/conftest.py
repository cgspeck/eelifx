from unittest.mock import Mock
import pytest


def mock_bulb_factory(group_name):
    mock_bulb = Mock()
    mock_bulb.get_group = Mock(return_value=group_name)
    return mock_bulb


@pytest.fixture
def standard_bulbs():
    return [
        mock_bulb_factory('ship-main'),
        mock_bulb_factory('ship-alert'),
        mock_bulb_factory('ship-main'),
        mock_bulb_factory('ship-alert'),
        mock_bulb_factory('lounge room'),
        mock_bulb_factory('hall way'),
    ]


@pytest.fixture
def bulb_container():
    from eelifx import bulbs
    mbulbs = bulbs.Bulbs()

    return mbulbs
