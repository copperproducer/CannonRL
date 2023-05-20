import MLMC
import SchemCode as SC
import fire
from mcrcon import MCRcon as r
import random
import time

import subprocess

import pyautogui
#playerlist = MLMC.getPlayerList()

blockDict = SC.blockDict

def getPlayerList():
    playerlist = MLMC.getPlayerList()
    return playerlist


#run a command
def runCommand(command):
    message = MLMC.runCommand(command)
    return message

#runs a command as a player
def sudo(command, player):
    message = MLMC.runCommand("sudo " + player + " " + command)

    return message



#set block at target position
def setBlock(x, y, z, blockID):
    MLMC.setBlock(x, y, z, blockID)


#set a line of blocks at a target position
def setLineOfBlocks(x1, y1, z1, x2, y2, z2, blockID):
    MLMC.setLineOfBlocks(x1, y1, z1, x2, y2, z2, blockID)

#fill a region with a block
def fillRegion(x1, y1, z1, x2, y2, z2, blockID):
    MLMC.fillRegion(x1, y1, z1, x2, y2, z2, blockID)

#place the target at the position
def placeTarget(player, pos):
    setPos(player, pos[0], pos[1], pos[2])

    with r("localhost", "5") as mcr:
        mcr.command(f"fill {pos[0]} {pos[1]} {pos[2]} {pos[0]+15} {pos[1]+15} {pos[2]+15} red_concrete")


    #behind the target place a wall of blocks from y=-60 to y=n and make it the same width as the target (16 blocks) place the wall 16 blocks behind the target
        n = 160
        mcr.command(f"fill {pos[0]+21} -60 {pos[2]+15} {pos[0]+21} {n} {pos[2]} white_concrete")

#i forgot what this does
def setLine(x1, y1, z1, x2, y2, z2, blockID):
    MLMC.setLine(x1, y1, z1, x2, y2, z2, blockID)

#set the position of a player
def setPos(player, posx, posy, posz):
    MLMC.setPos(player, posx, posy, posz)

#create a data structure of xyz size
def createCube(x, y, z):
    cube = SC.createCube(x, y, z)
    return cube


#create a schem of xyz size
def createSchem(x, y, z):
    schem = SC.createSchem(x, y, z)
    return schem

#make a fractal schem
def fractal(schem):
    SC.fractal(schem)

#changes the block in a schem to a different block
def setSchemBlock(schem, x, y, z, block):
    SC.setSchemBlock(schem, x, y, z, block)

#fills the schem with red concrete
def fillSchem(schem):
    schem = SC.fillSchem(schem)
    return schem

#places the schem at the target position
def placeBlocksTarget(schem, targetPos, player):
    SC.placeBlocksTarget(schem, targetPos, player)

#calculates the distance between two points
def distance(cannonPos, targetPos):
    distance = fire.distance(cannonPos, targetPos)
    return distance

#loads all of the chunks between the cannon and the target
def loadChunks(cannonPos, targetPos, player):
    fire.loadChunks(cannonPos, targetPos, player)

#fills the cannon with tnt. Must be run after setCannon to work due to player not being teleported again
def fillCannon(player, cannonPos):
    fire.fillCannon(player, cannonPos)

#places the cannon at the cannon position
def setCannon(cannonSchem, cannonPos, player):
    fire.setCannon(cannonSchem, cannonPos, player)

#places the target at the target position
def setTarget(targetPos, player, schemTarget):
    fire.setTarget(targetPos, player, schemTarget)

#count the amount of non-air blocks in the schem
def countBlocks(schem):
    fire.countBlocks(schem)

#fires the cannon
def fireCannon(player, cannonpos):
    fire.fireCannon(player, cannonpos)

#randomly determine the distance between the cannon and the target
def setTargetDistance(minTargetDistance, maxTargetDistance):
    targetDistance = random.randint(minTargetDistance, maxTargetDistance)
    return targetDistance



def getMessage(player, pos):
    blocksclearedmessage = ""
    setPos(player, pos[0], pos[1], pos[2])
    with r("localhost", "5") as mcr:
        pos = pos[0], pos[1], pos[2], pos[0]+15, pos[1]+15, pos[2]+15
        #make sure that each pos number is an int
        pos = [int(i) for i in pos]


        blocksclearedmessage = mcr.command(f"fill {pos[0]} {pos[1]} {pos[2]} {pos[3]} {pos[4]} {pos[5]} air")
        #print('++++++++++++++++++++++++++++++++++++++++++++++++++++blocksclearedmessage: ', blocksclearedmessage)
    return blocksclearedmessage



def checkWallDamage(player, pos, block_size):
    #fill the position with air going 16 blocks in the z direction and the block size in the y direction
    message = runCommand(f"fill {pos[0]} {pos[1]} {pos[2]} {pos[0]} {pos[1]+block_size-1} {pos[2]+16} air")

    #check the message for the amount of blocks cleared
    blocks_cleared = int(message.split(" ")[2])
    blocks_cleared = (16 * block_size) - blocks_cleared

    #print('-----------------------------blocks_cleared: ', blocks_cleared)
    return blocks_cleared


#returns the amount of blocks cleared
#returns the amount of blocks cleared
def checkDamage(player, pos):
    wall_top = 160
    wall_bottom = -60
    block_size = 10
    targetblocksclearedmessage = getMessage(player, pos)

    #print('targetblocksclearedmessage: ', targetblocksclearedmessage)

    if targetblocksclearedmessage != "Successfully filled 4096 blocks":


        #extract the number of blocks cleared from the message make it work for any size number and use split
        blocks_cleared = int(targetblocksclearedmessage.split(" ")[2])


        blocks_cleared = 4096 - blocks_cleared

        #reward = blocks_cleared + 200
        reward = 200
        return reward


    


    else:

        # check the wall behind the target in block_size intervals

        wall_blocks_cleared = []

        for y in range(wall_bottom, wall_top, block_size):

            # check the damage to the wall at this y-level

            wall_pos = [pos[0] + 21, y, pos[2]]

            time.sleep(0.0005)

            blocks_cleared = checkWallDamage(player, wall_pos, block_size)


            wall_blocks_cleared.append(blocks_cleared)

            # if there is a hole in the wall, calculate the distance to the target to determine the reward

            if blocks_cleared > 0:

                distance_to_target = distance([pos[0]+ 21, pos[1], pos[2]], [wall_pos[0], wall_pos[1], wall_pos[2]])

                if distance_to_target <= block_size:

                    reward = 100

                elif distance_to_target <= block_size * 2:

                    reward = 90

                elif distance_to_target <= block_size * 3:

                    reward = 80

                elif distance_to_target <= block_size * 4:

                    reward = 70

                elif distance_to_target <= block_size * 5:

                    reward = 60

                elif distance_to_target <= block_size * 6:

                    reward = 50

                elif distance_to_target <= block_size * 7:

                    reward = 40

                elif distance_to_target <= block_size * 8:

                    reward = 30

                return reward
            else:
                reward = 0

    return reward







#save the position in a file
def savePos(x, y, z):
    with open('position.txt', 'w') as f:
        f.write(str(x) + ' ' + str(y) + ' ' + str(z))
    return

#read the position from a file
def readPos():
    with open('position.txt', 'r') as f:
        x, y, z = f.read().split()
    return [int(x), int(y), int(z)]

#tickwarp the amount of ticks specified
def tickWarp(ticks):
    runCommand("tick warp " + str(ticks))


import os
import shutil
import pyautogui
def resetWorld():



    destination = "C:\\Users\\zacha\\OneDrive\\Desktop\\MLMC\\Fabric Server\\world"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree("C:\\Users\\zacha\\OneDrive\\Desktop\\MLMC\\world", destination)



import numpy as np










#anatomy of a module
                       #  [[[0, 0, 0], #this layer faces west
                       #  [1, 1, 1], #the first number is the bottom layer of that layer
                       #  [1, 1, 1]],
                       # [[0, 0, 0],
                       #  [1, 1, 1],
                       #  [41, 41, 41]],
                       # [[2, 2, 2],  #this layer faces east
                       #  [2, 2, 2],
                       #  [2, 2, 2]]]

# the target is on the east side of the cannon


#set the 3x3x3 cube of blocks in the schem to be a different list of 27 blocks with numpy and make the first 9 blocks be the top layer



#scan a schem and place only keep the blocks that are selected

#place the schem but only place the block that is selected
#clear the schem except for the block that is selected for schems of any size
# def clearSchemExcept(schem, block):
#     for i in range(len(schem)):
#         for j in range(len(schem[0])):
#             for k in range(len(schem[0][0])):
#                 if schem[i][j][k] != block:
#                     setSchemBlock(schem, i, j, k, 0)
# schem = createSchem(9, 9, 9)
# #modify the schem every 3x3x3 cube
# for i in range(3):
#     for j in range(3):
#         for k in range(3):
#             setModule(schem, i*3, j*3, k*3, 5)
#
# import time
# setCannon(schem, [0,0,0], 'CH3ST')
# setCannon(schem, [0,0,0], 'CH3ST')
# print(schem)
#(schem, [0,0,0], 'CH3ST')
#create a function to place the schem at the target position and use threading to make it faster
import psutil
def restartServerAndMC():

    #if the "Sodium 1.18.2" window is open, close it with pyautogui
    time.sleep(1)
    try:
        sodium_window = pyautogui.getWindowsWithTitle("Sodium 1.18.2")[0]
        sodium_window.activate()
        #use alt+f4 to close the window
        pyautogui.hotkey('alt', 'f4')
    except:
        pass
    time.sleep(1)
    #if the "MultiMC 5" window is open, close it with pyautogui
    try:
        multi_mc_window = pyautogui.getWindowsWithTitle("MultiMC 5 - Version 0.7.0-3739 on win32 - MultiMC 5")[0]
        multi_mc_window.activate()
        #use alt+f4 to close the window
        pyautogui.hotkey('alt', 'f4')
    except:
        pass
    time.sleep(1)
    #if the "Fabric Server" window is open, close it with pyautogui
    try:
        fabric_server_window = pyautogui.getWindowsWithTitle("Minecraft server")[0]
        fabric_server_window.activate()
        #use alt+f4 to close the window
        pyautogui.hotkey('alt', 'f4')
    except:
        pass
    time.sleep(1)
    try:
        sodium_window = pyautogui.getWindowsWithTitle("Sodium 1.18.2")[0]
        sodium_window.activate()
        #use alt+f4 to close the window
        pyautogui.hotkey('alt', 'f4')
    except:
        pass
    time.sleep(1)
    #if the "MultiMC 5" window is open, close it with pyautogui
    try:
        multi_mc_window = pyautogui.getWindowsWithTitle("MultiMC 5 - Version 0.7.0-3739 on win32 - MultiMC 5")[0]
        multi_mc_window.activate()
        #use alt+f4 to close the window
        pyautogui.hotkey('alt', 'f4')
    except:
        pass
    time.sleep(1)
    #if the "Fabric Server" window is open, close it with pyautogui
    try:
        fabric_server_window = pyautogui.getWindowsWithTitle("Minecraft server")[0]
        fabric_server_window.activate()
        #use alt+f4 to close the window
        pyautogui.hotkey('alt', 'f4')
    except:
        pass

    time.sleep(60)


    #restart the server fabric-server-launch at C:\Users\zacha\OneDrive\Desktop\Code Stuffs\MLMC\Fabric Server
    os.chdir(r"C:\Users\zacha\OneDrive\Desktop\Code Stuffs\MLMC\Fabric Server")

    os.startfile("fabric-server-launch.jar")




    time.sleep(30)
    #open multimc at C:\Users\zacha\MC\MultiMC
    os.chdir("C:\\Users\\zacha\\MC\\MultiMC")
    os.system("start multimc.exe")

    # Wait for MultiMC to fully load
    time.sleep(5)

    # Find the MultiMC window and bring it into focus
    window_title = "MultiMC 5 - Version 0.7.0-3739 on win32 - MultiMC 5"
    multi_mc_window = pyautogui.getWindowsWithTitle(window_title)[0]
    multi_mc_window.activate()

    # Move the mouse cursor to the center of the window
    pyautogui.moveTo(multi_mc_window.center)

    # click twice
    pyautogui.click()
    time.sleep(.2)
    pyautogui.click()


    time.sleep(20)
    # Select the "Sodium 1.18.2" instance
    sodium_window_title = "Sodium 1.18.2"
    sodium_instance = pyautogui.getWindowsWithTitle(sodium_window_title)[0]
    sodium_instance.activate()


    # Move the mouse cursor slightly below the center of the window
    window_center = sodium_instance.center
    click_point = (window_center[0], window_center[1] + 20)
    pyautogui.moveTo(click_point)

    # Perform three clicks with short delays in between
    pyautogui.click()
    time.sleep(5)
    pyautogui.click()
    pyautogui.click()
    # set the os to the directory of the project C:\Users\zacha\PycharmProjects\Code1.0 - Copy - Copy\position.txt
    os.chdir("C:\\Users\\zacha\\PycharmProjects\\Code1.0 - Copy - Copy")
    time.sleep(5)















