def luacode():
    return '''
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
