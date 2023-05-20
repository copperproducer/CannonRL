import MCWrapper
import MLMC
import SchemCode
import time
import math

fireStart = time.time()



#this file has all the code to place the cannon and target and fire the cannon


#calculate distance between MLMC.cannonPos and MLMC.targetPos
def distance(cannonPos, targetPos):
    x1, y1, z1 = cannonPos
    x2, y2, z2 = targetPos
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return (dx**2 + dy**2 + dz**2)**0.5


#player = MLMC.getPlayerList()[0]
#generate a line from SchemCode.cannonPos to SchemCode.targetPos and MLMC.setPos to every 100th block
def loadChunks(cannonPos, targetPos, player):
    x1, y1, z1 = cannonPos
    x2, y2, z2 = targetPos
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    # every 100th block set the player to that block
    for i in range(100, int(dx), 100):
        x = x1 + i
        y = y1 + dy * i / dx
        z = z1 + dz * i / dx
        MLMC.setPos(player, x, y, z)
        MCWrapper.tickWarp(50)
        time.sleep(.025)
    # finally, set the player to the target position
    MLMC.setPos(player, x2, y2, z2)
    return



#setPos to SchemCode.cannonPos and use the tntfill command to fill the area around the cannon
def fillCannon(player, cannonPos, height):
    #print the variables for debugging
    height = int(math.ceil(height/10))
    for i in range(0, height, 10):
        MLMC.setPos(player, cannonPos[0]+8, cannonPos[1]+i, cannonPos[2]+8)
        MLMC.runCommand('sudo -u Ch3st tntfill 10')




#time this
def setCannon(cannonSchem, cannonPos, player):
    start = time.time()
    MLMC.setPos(player, cannonPos[0], cannonPos[1], cannonPos[2])
    time.sleep(.01)
    #print(f'fire setcannon cannonPos is: {cannonPos}')
    SchemCode.placeBlocksTarget(cannonSchem, cannonPos, player)
    fillCannon(player, cannonPos)
    stop = time.time()
    #print("Time to place cannon: " + str(stop - start))



#count the amount of non-air blocks in the schem
def countBlocks(schem):
    count = 0
    for x in range(len(schem)):
        for y in range(len(schem[x])):
            for z in range(len(schem[x][y])):
                if schem[x][y][z] != 0:
                    count += 1
    return count







#replace the gold blocks in the schem with redstone blocks with fill command
def replaceGold(player, cannonPos):
    MLMC.runCommand(f"fill {cannonPos[0]-5} {cannonPos[1]-1} {cannonPos[2]-5} {cannonPos[0]+20} {cannonPos[1]+20} {cannonPos[2]+20} redstone_block replace gold_block")

    return

#replace the redstone blocks in the schem with gold blocks with fill command
def replaceRedstone(cannonPos):
    MLMC.runCommand(f"fill {cannonPos[0]-5} {cannonPos[1]-1} {cannonPos[2]-5} {cannonPos[0]+20} {cannonPos[1]+20} {cannonPos[2]+20} gold_block replace redstone_block")

    return

def fireCannon(player, cannonPos):
    MLMC.setPos(player, cannonPos[0], cannonPos[1], cannonPos[2])

    #time.sleep(1)
    replaceGold(player, cannonPos)
    #time.sleep(.5)
    #replaceRedstone(player)


#make a player class to run the functions


#use the fill command to replace any gold blocks with


#build the cannon schem using the DQN
#build the target
#build the cannon
#fire the cannon
#calculate how much self damage the cannon did
#load the chunks
#calculate how much damage the cannon did
#calculate the reward
#update the DQN
#repeat

fireEnd = time.time()
print("Fire file time: " + str(fireEnd - fireStart))

