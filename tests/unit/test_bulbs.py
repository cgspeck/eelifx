import re
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


def test_filter_group(bulb_container, standard_bulbs):
    '''
    Filter is an iterator that takes a compiled regex and returns only bulbs that match
    '''
    bulb_container.bulbs = standard_bulbs
    compiled_regex = re.compile('ship.*', flags=re.I)
    expected_bulbs = standard_bulbs[0:4]
    assert list(bulb_container.filter_group(compiled_regex)) == expected_bulbs
