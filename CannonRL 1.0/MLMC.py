from mcrcon import MCRcon as r
import time

MLMCstart = time.time()


def getPlayerListMessage():
    playerListmessage = ()
    with r("localhost", "5") as mcr:
        playerListmessage = mcr.command("list")


    return playerListmessage


#remove extra part of the message


#Convert the player list message string into a list
def Convert(string):
    li = list(string.split(" "))
    return li




#remove comma from player usernames in list
def removeCommaFromUsername(playerlist):
    for i in range(len(playerlist)):
        playerlist[i] = playerlist[i].replace(",", "")
    return playerlist



def getPlayerList():
    playerlistmessage = getPlayerListMessage()
    print(playerlistmessage)

    playerlistmessage = playerlistmessage[43:]
    print(playerlistmessage)

    playerlist = Convert(playerlistmessage)
    print(playerlist)
    playerlist = removeCommaFromUsername(playerlist)
    return playerlist


def runCommand(command):
    with r("localhost", "5") as mcr:
        message = mcr.command(command)
        return message


def setBlock(x, y, z, blockID):
    with r("localhost", "5") as mcr:
        mcr.command("fill " + str(x) + " " + str(y) + " " + str(z) + " " + str(x) + " " + str(y) + " " + str(z) + " "+ str(blockID))

#in the schem, place the the longest line of blocks with the same id, with a single command to save time
def setLineOfBlocks(x1, y1, z1, x2, y2, z2, blockID):
    with r("localhost", "5") as mcr:
        mcr.command("fill " + str(x1) + " " + str(y1) + " " + str(z1) + " " + str(x2) + " " + str(y2) + " " + str(z2) + " "+ str(blockID))

#define a function to fill a region with a block with the same id
def fillRegion(x1, y1, z1, x2, y2, z2, blockID):
    with r("localhost", "5") as mcr:
        mcr.command("fill " + str(x1) + " " + str(y1) + " " + str(z1) + " " + str(x2) + " " + str(y2) + " " + str(z2) + " "+ str(blockID))




def setPos(player, posx, posy, posz):
    x, y, z = posx, posy, posz
    #print('setting position of player ' + player + ' to ' + str(x) + ' ' + str(y) + ' ' + str(z))
    with r("localhost", "5") as mcr:
        mcr.command("tp " + player + " " + str(x) + " " + str(y) + " " + str(z))




#set a line of blocks from x1, y1, z1 to x2, y2, z2
def setLine(x1, y1, z1, x2, y2, z2, blockID):
    with r("localhost", "5") as mcr:
        mcr.command("fill " + str(x1) + " " + str(y1) + " " + str(z1) + " " + str(x2) + " " + str(y2) + " " + str(z2) + " "+ str(blockID))

#define a wait function
def wait(seconds):
    time.sleep(seconds)


MLMCend = time.time()
MLMCtime = MLMCend - MLMCstart
#print('MLMC time: ' + str(MLMCtime))