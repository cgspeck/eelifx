import re


def test_filter_group(bulb_container, standard_bulbs):
    '''
    Filter is an iterator that takes a compiled regex and returns only bulbs that match
    '''
    bulb_container.bulbs = standard_bulbs
    compiled_regex = re.compile('ship.*', flags=re.I)
    expected_bulbs = standard_bulbs[0:4]
    assert list(bulb_container.filter_group(compiled_regex)) == expected_bulbs
