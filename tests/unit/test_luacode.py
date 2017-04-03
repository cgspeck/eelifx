import pytest

from eelifx.luacode import luacode, statement_for

testdata_statement_for = [
    ('hull', 10, 'playerShip:setHull(10)\n'),
    ('energy', 999, 'playerShip:setEnergyLevel(999)\n')
]

standard_lua_code = '''
playerShip = getPlayerShip(-1)
energyLevel = playerShip:getEnergyLevel()
energyLevelMax = playerShip:getEnergyLevelMax()
alertLevel = playerShip:getAlertLevel()
shieldsActive = playerShip:getShieldsActive()
hull = playerShip:getHull()
hullMax = playerShip:getHullMax()

return {
    energyLevel=energyLevel,
    energyLevelMax=energyLevelMax,
    hull = hull,
    hullMax = hullMax,
    shieldsActive=shieldsActive,
    alertLevel=alertLevel,
}
'''

modified_lua_code = '''
playerShip = getPlayerShip(-1)
some modification
some other mod
energyLevel = playerShip:getEnergyLevel()
energyLevelMax = playerShip:getEnergyLevelMax()
alertLevel = playerShip:getAlertLevel()
shieldsActive = playerShip:getShieldsActive()
hull = playerShip:getHull()
hullMax = playerShip:getHullMax()

return {
    energyLevel=energyLevel,
    energyLevelMax=energyLevelMax,
    hull = hull,
    hullMax = hullMax,
    shieldsActive=shieldsActive,
    alertLevel=alertLevel,
}
'''

testdata_luacode = [
    (None, standard_lua_code),
    ('', standard_lua_code),
    ('some modification\nsome other mod', modified_lua_code)
]


@pytest.mark.parametrize('action,value,expected', testdata_statement_for)
def test_statement_for(action, value, expected):
    assert statement_for(action, value) == expected


def test_statement_for_unexpected():
    with pytest.raises(ValueError):
        statement_for('not an action', False)


@pytest.mark.parametrize('insert,expected', testdata_luacode)
def test_luacode(insert, expected):
    assert luacode(insert) == expected
