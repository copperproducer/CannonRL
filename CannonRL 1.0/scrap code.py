blockDict = {
    0: air,
    1: stone,
    2: smoothstoneslab,
    3: redstone,
    4: dispenserN,
    5: dispenserS,
    6: dispenserE,
    7: dispenserW,
    8: redstoneRepeaterN,
    9: redstoneRepeaterS,
    10: redstoneRepeaterE,
    11: redstoneRepeaterW,
    12: water,
    13: redstoneComparatorN,
    14: redstoneComparatorS,
    15: redstoneComparatorE,
    16: redstoneComparatorW,
    95: "minecraft:red_concrete",
    41: goldBlock,
    152: redstoneBlock

elif action == 1:
block = 1
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 2:
block = 2
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 3:
block = 3
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 4:
block = 4
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 5:
block = 5
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 6:
block = 6
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 7:
block = 7
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 8:
block = 8
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 9:
block = 9
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 10:
block = 10
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 11:
block = 41
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 12:
if self.usedwater == False:
    block = 12
    schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
    self.usedwater = True
    print('used water')
    return schem
elif self.usedwater == True:
    block = 0
    schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
    print('water already used')
    return schem
# print('water used')
# block = 12
# schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
# return schem
elif action == 13:
    block = 13
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 14:
block = 14
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 15:
block = 15
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 16:
block = 16
schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
return schem
elif action == 17:
if self.usedgoldblock == False:
    block = 41
    schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
    self.usedgoldblock = True
    print('used gold block')
    return schem
elif self.usedgoldblock == True:
    block = 0
    schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
    print('gold block already used')
    return schem
# print('used gold block')
# block = 41
# schem = MC.setSchemBlock(self.cannonSchem, currentschempos[0], currentschempos[1], currentschempos[2], block)
# return schem





schemsizexz = 25
cannonAngle = 4
cannonBarrelPower = 20
cannonProjectilePower = 5
cannonDelay = 6




barrelIce = createCannonBarrelIce()

cannonBarrel = createCannonBarrel(cannonBarrelPower)

cannonProjectileWiringRight = createCannonProjectileWiring(cannonProjectilePower, True)
cannonProjectileWiringLeft = createCannonProjectileWiring(cannonProjectilePower, False)

cannonProjectile = createCannonProjectile(cannonProjectilePower, cannonAngle)

verticleWiringBack = createVerticalWiring(math.ceil(cannonBarrelPower/16))
verticleWiringFront = createVerticalWiring(math.ceil(cannonProjectilePower) + 3)

cannonBarrelWiringLeft = createBarrelWiring(math.ceil(cannonBarrelPower/16), False)
cannonBarrelWiringRight = createBarrelWiring(math.ceil(cannonBarrelPower/16), True)

if cannonBarrelPower/16 > cannonProjectilePower:
    cannonSpacer = createCannonSpacer(math.ceil(cannonBarrelPower/16) + 2)
    schemsizey = cannonBarrelPower+20
else:
    cannonSpacer = createCannonSpacer(cannonProjectilePower + 2)
    schemsizey = cannonProjectilePower+20



masterSchem = createSchem(schemsizexz, schemsizey, schemsizexz)


#build the cannon
setModule(masterSchem, barrelIce, 11, 5, 11)
setModule(masterSchem, cannonBarrel, 10, 6, 10)
setModule(masterSchem, cannonSpacer, 19, 6, 10)
setModule(masterSchem, cannonProjectile, 20, 6, 10)
setModule(masterSchem, cannonBarrelWiringRight, 10, 6, 13)
setModule(masterSchem, cannonBarrelWiringLeft, 10, 6, 8)
setModule(masterSchem, cannonProjectileWiringRight, 20, 6, 13)
setModule(masterSchem, cannonProjectileWiringLeft, 20, 6, 3)
setModule(masterSchem, verticleWiringBack, 7, 4, 13)
setModule(masterSchem, verticleWiringBack, 7, 4, 7)
setModule(masterSchem, verticleWiringFront, 17, 4, 18)
setModule(masterSchem, verticleWiringFront, 17, 4, 2)

#connect the cannon wiring to the power source


#place the stone for the redstone to sit on
setSchemBlock(masterSchem, 8, 4, 12, 1)
setSchemBlockLine(masterSchem, 8, 4, 11, 4, 4, 11, 1)
setSchemBlockLine(masterSchem, 4, 4, 11, 4, 4, 0, 1)
setSchemBlockLine(masterSchem, 4, 4, 0, 18, 4, 1, 1)
setSchemBlock(masterSchem, 18, 5, 1, 1)

setSchemBlockLine(masterSchem, 4, 4, 11, 4, 4, 18, 1)
setSchemBlockLine(masterSchem, 4, 4, 17, 18, 4, 17, 1)
setSchemBlock(masterSchem, 18, 5, 17, 1)

setSchemBlockLine(masterSchem, 4, 4, 6, 8, 4, 6, 1)
setSchemBlock(masterSchem, 8, 5, 6, 1)


#place the redstone

setSchemBlockLine(masterSchem, 8, 5, 11, 3, 5, 11, 3)
setSchemBlockLine(masterSchem, 4, 5, 11, 4, 5, 0, 3)
setSchemBlockLine(masterSchem, 4, 5, 0, 18, 5, 1, 3)

setSchemBlockLine(masterSchem, 4, 5, 11, 4, 5, 18, 3)
setSchemBlockLine(masterSchem, 4, 5, 17, 18, 5, 17, 3)

setSchemBlockLine(masterSchem, 4, 5, 6, 8, 5, 6, 3)

#place the redstone repeaters for the verticle wiring

setSchemBlock(masterSchem, 7, 5, 6, 25)
setSchemBlock(masterSchem, 8, 5, 12, 8)
setSchemBlock(masterSchem, 17, 5, 17, 25)
setSchemBlock(masterSchem, 17, 5, 1, 25)

#place the redstone repeaters for the delay

setSchemBlockLine(masterSchem, 5, 5, 1, 5+cannonDelay, 5, 1, 25)
setSchemBlockLine(masterSchem, 5, 5, 17, 5+cannonDelay, 5, 17, 25)





#time how long it takes to place the schematic
start = time.time()


placeBlocksTarget(masterSchem, [0,0,0], 'CH3ST')



end = time.time()
print(end - start)
