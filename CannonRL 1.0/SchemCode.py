import MLMC
import time
import numpy
import threading
import multiprocessing
import math

#time the schem code

schemstart = time.time()

#add a buld target position
def addBuildTarget(x, y, z):
    MLMC.addBuildTarget(x, y, z)
    return


#create an x by y by z numpy.ndarray to store the blocks in the schem
def createCube(x, y, z):
    cube = numpy.zeros((x, y, z))
    #print(numpy.shape(cube))
    return cube
createCube(16, 16, 16)


#create a x by y by z data structure with numpy.ndarray and set the blocks to 0
def createSchema(x, y, z):
    schem = numpy.ndarray((x, y, z))
    for i in range(x):
        for j in range(y):
            for k in range(z):
                schem[i][j][k] = 0
    return schem



#make a 16 by 16 by 16 data structure with x, y, z coordinates and set the blocks to 0
def createSchem(x, y, z):

    #print x, y, z
    #print("x: " + str(x) + " y: " + str(y) + " z: " + str(z))
    schem = numpy.ndarray((x, y, z))
    for i in range(x):
        for j in range(y):
            for k in range(z):
                schem[i][j][k] = 0
    return schem






stone = "minecraft:stone"
air = "minecraft:air"
smoothstoneslab = "minecraft:smooth_stone_slab"
redstone = "minecraft:redstone_wire"
dispenserN = "minecraft:dispenser[facing=north]"
dispenserS = "minecraft:dispenser[facing=south]"
dispenserE = "minecraft:dispenser[facing=east]"
dispenserW = "minecraft:dispenser[facing=west]"
redstoneRepeaterN = "minecraft:repeater[facing=north,powered=false]"
redstoneRepeaterS = "minecraft:repeater[facing=south,powered=false]"
redstoneRepeaterE = "minecraft:repeater[facing=east,powered=false]"
redstoneRepeaterW = "minecraft:repeater[facing=west,powered=false]"
redstoneRepeaterDelayedN = "minecraft:repeater[facing=north,powered=false,delay=4]"
redstoneRepeaterDelayedS = "minecraft:repeater[facing=south,powered=false,delay=4]"
redstoneRepeaterDelayedE = "minecraft:repeater[facing=east,powered=false,delay=4]"
redstoneRepeaterDelayedW4 = "minecraft:repeater[facing=west,powered=false,delay=4]"
redstoneRepeaterDelayedW3 = "minecraft:repeater[facing=west,powered=false,delay=3]"
redstoneRepeaterDelayedW2 = "minecraft:repeater[facing=west,powered=false,delay=2]"
redstoneRepeaterDelayedW1 = "minecraft:repeater[facing=west,powered=false,delay=1]"
water = "minecraft:water[level=0]"
redstoneComparatorN = "minecraft:comparator[facing=north,powered=false]"
redstoneComparatorS = "minecraft:comparator[facing=south,powered=false]"
redstoneComparatorE = "minecraft:comparator[facing=east,powered=false]"
redstoneComparatorW = "minecraft:comparator[facing=west,powered=false]"
goldBlock = "minecraft:gold_block"
redstoneBlock = "minecraft:redstone_block"
observerN = "minecraft:observer[facing=north,powered=false]"
observerS = "minecraft:observer[facing=south,powered=false]"
observerE = "minecraft:observer[facing=east,powered=false]"
observerW = "minecraft:observer[facing=west,powered=false]"
observerUp = "minecraft:observer[facing=up,powered=false]"
observerDown = "minecraft:observer[facing=down,powered=false]"
whiteStainedGlass = "minecraft:white_stained_glass"
blueIce = "minecraft:blue_ice"
redstoneWallTorchW = "minecraft:redstone_wall_torch[facing=west]"
redstoneWallTorchE = "minecraft:redstone_wall_torch[facing=east]"
tnt = "minecraft:tnt"
pistonS = "minecraft:piston[facing=south,extended=false]"
soulSand = "minecraft:soul_sand"
ladder = "minecraft:ladder[facing=north]"

snowLayer1 = "minecraft:snow[layers=1]"
snowLayer2 = "minecraft:snow[layers=2]"
snowLayer3 = "minecraft:snow[layers=3]"
snowLayer4 = "minecraft:snow[layers=4]"
snowLayer5 = "minecraft:snow[layers=5]"
snowLayer6 = "minecraft:snow[layers=6]"
snowLayer7 = "minecraft:snow[layers=7]"
snowLayer8 = "minecraft:snow[layers=8]"



#put the variables into a dictionary
blockDict = {
    0: air,
    1: stone,
    2: smoothstoneslab,
    3: redstone,
    4: observerW,
    5: dispenserN,
    6: dispenserS,
    7: goldBlock,
    8: redstoneRepeaterN,
    9: redstoneRepeaterS,
    10: whiteStainedGlass,
    11: pistonS,
    12: soulSand,
    13: water,
    14: ladder,
    15: snowLayer1,
    16: snowLayer2,
    17: snowLayer3,
    18: snowLayer4,
    19: snowLayer5,
    20: snowLayer6,
    21: snowLayer7,
    22: snowLayer8,
    23: blueIce,
    24: redstoneRepeaterE,
    25: redstoneRepeaterW,
    26: redstoneRepeaterDelayedW4,
    27: redstoneRepeaterDelayedW3,
    28: redstoneRepeaterDelayedW2,
    29: redstoneRepeaterDelayedW1,



}
#make schem a fractal
def fractal(schem):
    for i in range(16):
        for j in range(16):
            for k in range(16):
                if i % 2 == 0 and j % 2 == 0 and k % 2 == 0:
                    schem[i],[j],[k] = 1
                else:
                    schem[i],[j],[k] = 0
    return schem

#select a block in the schem with x, y, z coordinates and change it to a different block
def setSchemBlock(schem, x, y, z, block):
    schem[x][y][z] = block
    return schem





#make a schem of any size a solid block of concrete
def fillSchem(schem):
    block = 95
    for i in range(16):
        for j in range(16):
            for k in range(16):
                schem[i][j][k] = block
    return schem





#place the schematic in the world at the target position. The top of the schematic is towards the positive y direction. place the schem from the smallest x value to the bottom to top. And don't use the setlineofblocks command
def placeBlocksTarget(schem, targetPos, player):
    MLMC.setPos(player, targetPos[0]+10, targetPos[1]+10, targetPos[2]+10)
    blockList = []
    for i in range(len(schem)):
        for j in range(len(schem[i])):
            for k in range(len(schem[i][j])):
                if schem[i][j][k] != 0:
                    blockList.append([targetPos[0] + i, targetPos[1] + j, targetPos[2] + k, blockDict[schem[i][j][k]]])
    #place the block list with the fewest amount of setLineOfBlocks commands
    def placeBlocks7Helper(blockList):
        for i in range(len(blockList)):
            MLMC.setBlock(*blockList[i])

        return
    threads = []
    for i in range(16):
        t = threading.Thread(target=placeBlocks7Helper, args=(blockList[i::16],))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return

def setSchemBlockLine(schem, x1, y1, z1, x2, y2, z2, block):
    x = x1
    y = y1
    z = z1
    while x != x2 or y != y2 or z != z2:
        #print("schem debug")
        #print (x, y, z)
        #print(block)
        schem[x][y][z] = block
        if x < x2:
            x += 1
        elif x > x2:
            x -= 1
        if y < y2:
            y += 1
        elif y > y2:
            y -= 1
        if z < z2:
            z += 1
        elif z > z2:
            z -= 1
    return schem





class Module:
    def __init__(self, schemsizex, schemsizey, schemsizez):
        self.schemsizex = schemsizex
        self.schemsizey = schemsizey
        self.schemsizez = schemsizez
        self.schem = createSchem(schemsizex, schemsizey, schemsizez)

        #positive x is towards east
        #positive y is towards up
        #positive z is towards south
        #target is in the east direction






#this function creates the cannon barrel module
#it takes the number of dispensers and creates a module that contains that many dispensers
#this will allow the ai to create a cannon with an adjustable range
def createCannonBarrel(numDispensers):

    #layers equals numDispensers divided by 16 rounded up

    layers = math.ceil(numDispensers / 16)
    #round layers up to the nearest whole number
    #print ('layers', layers)

    if layers < 1:
        layers = 1


    #print("layers", layers)

    cannonWallHeight = layers + 1




    cannonBarrel = Module(9, layers+2, 3)
    schem = cannonBarrel.schem

    if layers > 1:
        numDispensersleft = numDispensers - layers * 16 + 16
    else:
        numDispensersleft = numDispensers

    #make numDispensersleft an integer
    numDispensersleft = int(numDispensersleft)



    #make the barrel
    for i in range(layers):
        if layers > 1:
            setSchemBlockLine(schem, 1, i, 0, 9, i, 0, 6)
            setSchemBlockLine(schem, 1, i, 2, 9, i, 2, 5)
            setSchemBlockLine(schem, 0, i, 0, 0, i, 3, 1)
        else:
            break

    #print("numDispensersleft", numDispensersleft)

    #this makes the top of the barrel
    if numDispensersleft > 8:

        #print("numDispensersleft", numDispensersleft)


        setSchemBlockLine(schem, 1, layers, 0, 9, layers, 0, 6)
        setSchemBlockLine(schem, 1, layers, 2, numDispensersleft-7, layers, 2 , 5)
        setSchemBlockLine(schem, 0, layers, 0, 0, layers, 3, 1)
        setSchemBlockLine(schem, numDispensersleft-7, layers, 2, 9, layers, 2, 1)
    else:

        #print("numDispensersleft", numDispensersleft)


        setSchemBlockLine(schem, 1, layers, 0, numDispensersleft+1, layers, 0, 6)
        setSchemBlockLine(schem, numDispensersleft+1, layers, 0, 9, layers, 0, 1)
        setSchemBlockLine(schem, 1, layers, 2, 9, layers, 2, 1)
        setSchemBlockLine(schem, 0, layers, 0, 0, layers, 3, 1)



    #fill the top layer with stone so that redstone can travel through the stone and into the dispenser below it
    setSchemBlockLine(schem, 1, -1, 0, 9, -1, 0, 1)
    setSchemBlockLine(schem, 1, -1, 2, 9, -1, 2, 1)
    setSchemBlockLine(schem, 0, -1, 0, 0, -1, 3, 1)

    setSchemBlock(schem, 1, 0, 1, 13)


    #comment later


    cannonBarrel.schem = schem


    #this fills the bottom layer of the cannon barrel so that water doesn't pour out of the bottom
    for x in range(len(schem)):
        for y in range(len(schem[x])):
            for z in range(len(schem[x][y])):
                if y == 0 and schem[x][y][z] == 0:
                    if z == len(schem[x][y]) // 2:  # check for center of the barrel
                        schem[x][y][z] = 0
                    else:
                        schem[x][y][z] = 1

    #this plugs a hole in the bottom of the cannon barrel
    setSchemBlock(schem, 0, 0, 1, 1)
    return cannonBarrel


#create the wiring for the cannon barrel
def createBarrelWiring(height, rightSide):
    layers = height / 2
    if layers < 1:
        layers = 1
    #round layers up to the nearest whole number
    layers = math.ceil(layers)
    cannonBarrelWiring = Module(9, layers*3, 2)
    schem = cannonBarrelWiring.schem
    if rightSide == False:
        for i in range(layers):

            i *= 2
            setSchemBlockLine(schem, 0, i, 0, 9, i, 0, 1)
            setSchemBlockLine(schem, 0, i, 1, 9, i, 1, 1)
            setSchemBlockLine(schem, 0, i+1, 0, 9, i+1, 0, 3)
            setSchemBlockLine(schem, 0, i+1, 1, 9, i+1, 1, 8)

    else:
        for i in range(layers):

            i *= 2
            setSchemBlockLine(schem, 0, i, 0, 9, i, 0, 1)
            setSchemBlockLine(schem, 0, i, 1, 9, i, 1, 1)
            setSchemBlockLine(schem, 0, i+1, 1, 9, i+1, 1, 3)
            setSchemBlockLine(schem, 0, i+1, 0, 9, i+1, 0, 9)

    cannonBarrelWiring.schem = schem
    return cannonBarrelWiring



def createVerticalWiring(height):
    layers = height
    verticleWiring = Module(3, layers+5, 3)

    schem = verticleWiring.schem

    setSchemBlockLine(schem, 0, 0, 0, 0, 0, 3, 10)
    setSchemBlockLine(schem, 1, 0, 0, 1, 0, 3, 10)
    setSchemBlockLine(schem, 2, 0, 0, 2, 0, 3, 10)

    setSchemBlockLine(schem, 0, 1, 0, 0, 1, 3, 10)
    setSchemBlockLine(schem, 2, 1, 0, 2, 1, 3, 10)
    setSchemBlock(schem, 1, 1, 0, 11)
    setSchemBlock(schem, 1, 1, 1, 12)



    for i in range(layers):
        setSchemBlockLine(schem, 0, i+2, 0, 3, i+2, 0, 10)
        setSchemBlockLine(schem, 0, i+2, 2, 3, i+2, 2, 10)
        setSchemBlock(schem, 0, i+2, 1, 10)
        setSchemBlock(schem, 2, i+2, 1, 4)
        setSchemBlock(schem, 1, i+2, 1, 13)




    verticleWiring.schem = schem
    return verticleWiring



def createCannonSpacer(height):
    layers = height
    cannonSpacer = Module(1, layers+5, 3)

    schem = cannonSpacer.schem

    for i in range(layers):
        setSchemBlock(schem, 0, i, 0, 10)
        setSchemBlock(schem, 0, i, 1, 14)
        setSchemBlock(schem, 0, i, 2, 10)

    cannonSpacer.schem = schem
    return cannonSpacer

def createCannonProjectile(numDispensers, snowLayers):
    layers = numDispensers
    #print('snowLayers', snowLayers)
    cannonProjectile = Module(1, layers+5, 3)
    schem = cannonProjectile.schem
    setSchemBlock(schem, 0, 0, 0, 1)
    setSchemBlock(schem, 0, 0, 2, 1)

    if snowLayers == 0:
        snowLayers = 0
    else:
        snowLayers = snowLayers + 14


    if snowLayers > 22:
        snowLayers = 22

    setSchemBlock(schem, 0, 0, 1, snowLayers)
    #print('snowLayers', snowLayers)
    for i in range(layers):
        setSchemBlock(schem, 0, i+1, 0, 6)
        setSchemBlock(schem, 0, i+1, 2, 5)

    for i in range(5):
        setSchemBlock(schem, 0, -i, 2, 1)
        setSchemBlock(schem, 0, -i, 0, 1)

    cannonProjectile.schem = schem
    return cannonProjectile


def createCannonProjectileWiring(height, rightSide):
    layers = height / 2
    if layers < 1:
        layers = 1
    #round layers up to the nearest whole number
    layers = math.ceil(layers)

    cannonProjectileWiring = Module(1, height+10, 7)
    schem = cannonProjectileWiring.schem

    if rightSide == False:
        for i in range(layers):

            i *= 2

            setSchemBlockLine(schem, 0, i+1, 0, 0, i+1, 7, 1)

            setSchemBlockLine(schem, 0, i+2, 0, 0, i+2, 6, 3)
            setSchemBlock(schem, 0, i+2, 6, 8)
    else:
        for i in range(layers):

            i *= 2

            setSchemBlockLine(schem, 0, i+1, 0, 0, i+1, 7, 1)

            setSchemBlockLine(schem, 0, i+2, 1, 0, i+2, 7, 3)
            setSchemBlock(schem, 0, i+2, 0, 9)

    cannonProjectileWiring.schem = schem
    return cannonProjectileWiring


def createCannonBarrelIce():
    cannonBarrelIce = Module(10, 1, 1)

    schem = cannonBarrelIce.schem
    setSchemBlockLine(schem, 0, 0, 0, 10, 0, 0, 23)

    cannonBarrelIce.schem = schem
    return cannonBarrelIce



def setModule(schem, module, x, y, z):
    for i in range(module.schemsizex):
        for j in range(module.schemsizey):
            for k in range(module.schemsizez):
                setSchemBlock(schem, x+i, y+j, z+k, module.schem[i][j][k])


schemend = time.time()
#print('schem time', schemend - schemstart)
