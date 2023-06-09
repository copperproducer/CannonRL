import os
import time
from datetime import datetime
import torch
import numpy as np
from PPO import PPO
from gym import spaces
import MCWrapper as MC
import math
import SchemCode as SC
import fire
import random

demomode = True

#MC.restartServerAndMC()
player = MC.getPlayerList()[0]
minDistance = 80
maxDistance = 300
minHeight = 0
maxHeight = 40
schemsize = 200
maxCannonPower = 100

cannonposnum = 7500

minCannonPosx = -cannonposnum
minCannonPosz = -cannonposnum

maxCannonPosx = cannonposnum
maxCannonPosz = cannonposnum

cannonPosStep = maxDistance + 100

averageRewardRequiredForLevelUp = 200
# this is how many episodes back the average reward for the level up is calculated
averageRewardBin = 5

# set the episode interval for restarting the server and MC client
restart_interval = 1000


class Cannon:

    def __init__(self):
        self.action_space = spaces.Box(low=np.array([0, 20, 0]), high=np.array([8, maxCannonPower, 29]), shape=(3,),
                                       dtype=np.float32)

        self.cannonPosStep = cannonPosStep

        self.averageReward = 0
        self.averageRewardBin = averageRewardBin
        self.prestigeDistance = 0
        self.prestigeHeight = 0

        self.currentHeightLevel = 30
        self.currentDistanceLevel = 30

        self.distanceAdded = self.currentDistanceLevel * 10
        self.heightAdded = self.currentHeightLevel * 2

        self.episode_rewards_level = []

        self.targetDistance = random.uniform(minDistance, minDistance + self.distanceAdded)
        if self.targetDistance > maxDistance:
            self.targetDistance = maxDistance
            # self.currentDistanceLevel = 0
            # self.prestigeDistance = self.prestigeDistance + 1

        self.targetHeight = random.uniform(minHeight, minHeight + self.heightAdded)
        if self.targetHeight > maxHeight:
            self.targetHeight = maxHeight
            # self.currentHeightLevel = 0
            # self.prestigeHeight = self.prestigeHeight + 1

        if self.averageReward > averageRewardRequiredForLevelUp:
            self.currentDistanceLevel = self.currentDistanceLevel + 1
            self.currentHeightLevel = self.currentHeightLevel + 1
            self.averageReward = 0

        self.cannonPos = MC.readPos()
        # if self.cannonPos[2] >= maxCannonPosz:
        # self.cannonPos[2] = minCannonPosz
        # self.cannonPos[0] = self.cannonPos[0] - cannonPosStep
        # if self.cannonPos[0] <= minCannonPosx:
        # self.cannonPos[0] = maxCannonPosx


        self.cannonPos[2] = self.cannonPos[2] + 100
        MC.savePos(self.cannonPos[0], self.cannonPos[1], self.cannonPos[2])
        self.targetPos = [self.cannonPos[0] + self.targetDistance, self.cannonPos[1] + self.targetHeight,
                          self.cannonPos[2]]
        # (f'{self.targetPos} is the target position')
        MC.placeTarget(player, self.targetPos, )
        self.masterSchem = MC.createSchem(schemsize, schemsize, schemsize)
        self.cannonPos = MC.readPos()
        self.currentschempos = [0, 0, 0]

        # the observation space is the distance between the cannon and the target it can be any number between the min and max distance

        self.observation_space = spaces.Box(low=np.array([minDistance, minHeight]),
                                            high=np.array([maxDistance, maxHeight]), shape=(2,), dtype=np.float32)

    def reset(self):

        self.distanceAdded = self.currentDistanceLevel * 10
        self.heightAdded = self.currentHeightLevel * 2

        self.targetDistance = random.uniform(minDistance, minDistance + self.distanceAdded)
        if self.targetDistance > maxDistance:
            self.targetDistance = maxDistance

        self.targetHeight = random.uniform(minHeight, minHeight + self.heightAdded)
        if self.targetHeight > maxHeight:
            self.targetHeight = maxHeight

        if demomode == True:
            #select to have the target at a random distance and height or a selected distance and height
            demo = input("Do you want to select the target distance and height? (y/n) inputting anything besides y will select a random distance and height")
            if demo == "y":
                self.targetDistance = int(input("Enter the target distance: "))
                self.targetHeight = int(input("Enter the target height: "))
            else:
                self.targetDistance = random.uniform(minDistance, maxDistance)
                if self.targetDistance > maxDistance:
                    self.targetDistance = maxDistance

                self.targetHeight = random.uniform(minHeight, minHeight + maxHeight)
                if self.targetHeight > maxHeight:
                    self.targetHeight = maxHeight

        # round the distance and height to the nearest integer
        self.targetDistance = round(self.targetDistance)
        self.targetHeight = round(self.targetHeight)
        self.targetDistance = int(self.targetDistance)
        self.targetHeight = int(self.targetHeight)

        if self.averageReward >= averageRewardRequiredForLevelUp:
            self.currentDistanceLevel = self.currentDistanceLevel + 1
            self.currentHeightLevel = self.currentHeightLevel + 1
            self.episode_rewards_level = []

        self.cannonPos = MC.readPos()
        # if self.cannonPos[2] >= maxCannonPosz:
        # self.cannonPos[2] = minCannonPosz
        # self.cannonPos[0] = self.cannonPos[0] - cannonPosStep
        # if self.cannonPos[0] <= minCannonPosx:
        # self.cannonPos[0] = maxCannonPosx

        self.cannonPos = MC.readPos()
        self.cannonPos[2] = self.cannonPos[2] + 50
        MC.savePos(self.cannonPos[0], self.cannonPos[1], self.cannonPos[2])

        self.targetPos = [self.cannonPos[0] + self.targetDistance, self.cannonPos[1] + self.targetHeight,
                          self.cannonPos[2]]
        # print (f'{self.targetPos} is the target position')
        MC.placeTarget(player, self.targetPos, )
        self.masterSchem = MC.createSchem(schemsize, schemsize, schemsize)
        self.cannonPos = MC.readPos()

        # print(f'\n\n\ntarget distance is {self.distanceAdded}')
        # print(f'target height is {self.heightAdded}')
        # print(f'current distance level is {self.currentDistanceLevel}')
        # print(f'current height level is {self.currentHeightLevel}')
        # print(f'prestige distance is {self.prestigeDistance}')
        # print(f'prestige height is {self.prestigeHeight}\n\n\n')

        reward = 0
        done = False
        info = {}
        # return the observation
        return [self.targetDistance, self.targetHeight]

    def action(self, cannonAngle, cannonBarrelPower, cannonDelay):

        cannonAngle = cannonAngle
        cannonBarrelPower = cannonBarrelPower
        cannonDelay = cannonDelay

        return cannonAngle, cannonBarrelPower, cannonDelay

    def placeSchem(self, schem, pos, player):
        MC.setCannon(schem, pos, player)
        return

    def step(self, action):
        # print (f'{action} is the action')
        # here lies the settings for the cannon. edit these for different cannon configurations
        # print(f'{action} is the action')
        cannonAngle, cannonBarrelPower, cannonDelay = self.action(action[0], action[1], action[2])

        schemsizexz = 25
        cannonProjectilePower = 5
        # cannonDelay = 28

        # time how long this takes
        start = time.time()

        barrelIce = SC.createCannonBarrelIce()

        cannonBarrel = SC.createCannonBarrel(cannonBarrelPower)

        cannonProjectileWiringRight = SC.createCannonProjectileWiring(cannonProjectilePower, True)
        cannonProjectileWiringLeft = SC.createCannonProjectileWiring(cannonProjectilePower, False)

        cannonProjectile = SC.createCannonProjectile(cannonProjectilePower, cannonAngle)

        verticleWiringBack = SC.createVerticalWiring(math.ceil(cannonBarrelPower / 16))
        verticleWiringFront = SC.createVerticalWiring(math.ceil(cannonProjectilePower) + 3)

        cannonBarrelWiringLeft = SC.createBarrelWiring(math.ceil(cannonBarrelPower / 16), False)
        cannonBarrelWiringRight = SC.createBarrelWiring(math.ceil(cannonBarrelPower / 16), True)

        # this decides the height of stuff

        if cannonBarrelPower / 16 > cannonProjectilePower:
            cannonSpacer = SC.createCannonSpacer(math.ceil(cannonBarrelPower / 16) + 2)
            schemsizey = cannonBarrelPower + 20
            height = cannonBarrelPower + 10
        else:
            cannonSpacer = SC.createCannonSpacer(cannonProjectilePower + 2)
            schemsizey = cannonProjectilePower + 20
            height = cannonProjectilePower + 10

        schemsizey = int(schemsizey)

        # print("schemsizexz: " + str(schemsizexz) + " schemsizey: " + str(schemsizey))

        self.masterSchem = SC.createSchem(schemsizexz, schemsizey, schemsizexz)

        # set the modules of the cannon in the schematic
        SC.setModule(self.masterSchem, barrelIce, 11, 5, 11)
        SC.setModule(self.masterSchem, cannonBarrel, 10, 6, 10)
        SC.setModule(self.masterSchem, cannonSpacer, 19, 6, 10)
        SC.setModule(self.masterSchem, cannonProjectile, 20, 6, 10)
        SC.setModule(self.masterSchem, cannonBarrelWiringRight, 10, 6, 13)
        SC.setModule(self.masterSchem, cannonBarrelWiringLeft, 10, 6, 8)
        SC.setModule(self.masterSchem, cannonProjectileWiringRight, 20, 6, 13)
        SC.setModule(self.masterSchem, cannonProjectileWiringLeft, 20, 6, 3)
        SC.setModule(self.masterSchem, verticleWiringBack, 7, 4, 13)
        SC.setModule(self.masterSchem, verticleWiringBack, 7, 4, 7)
        SC.setModule(self.masterSchem, verticleWiringFront, 17, 4, 18)
        SC.setModule(self.masterSchem, verticleWiringFront, 17, 4, 2)

        # connect the cannon wiring to the power source

        # place the stone for the redstone to sit on
        SC.setSchemBlock(self.masterSchem, 8, 4, 12, 1)
        SC.setSchemBlockLine(self.masterSchem, 8, 4, 11, 4, 4, 11, 1)
        SC.setSchemBlockLine(self.masterSchem, 4, 4, 11, 4, 4, 0, 1)
        SC.setSchemBlockLine(self.masterSchem, 4, 4, 0, 18, 4, 1, 1)
        SC.setSchemBlock(self.masterSchem, 18, 5, 1, 1)

        SC.setSchemBlockLine(self.masterSchem, 4, 4, 11, 4, 4, 18, 1)
        SC.setSchemBlockLine(self.masterSchem, 4, 4, 17, 18, 4, 17, 1)
        SC.setSchemBlock(self.masterSchem, 18, 5, 17, 1)

        SC.setSchemBlockLine(self.masterSchem, 4, 4, 6, 8, 4, 6, 1)
        SC.setSchemBlock(self.masterSchem, 8, 5, 6, 1)

        # place the redstone

        SC.setSchemBlockLine(self.masterSchem, 8, 5, 11, 3, 5, 11, 3)
        SC.setSchemBlockLine(self.masterSchem, 4, 5, 11, 4, 5, 0, 3)
        SC.setSchemBlockLine(self.masterSchem, 4, 5, 0, 18, 5, 1, 3)

        SC.setSchemBlockLine(self.masterSchem, 4, 5, 11, 4, 5, 18, 3)
        SC.setSchemBlockLine(self.masterSchem, 4, 5, 17, 18, 5, 17, 3)

        SC.setSchemBlockLine(self.masterSchem, 4, 5, 6, 8, 5, 6, 3)

        # place the redstone repeaters for the verticle wiring

        SC.setSchemBlock(self.masterSchem, 7, 5, 6, 25)
        SC.setSchemBlock(self.masterSchem, 8, 5, 12, 8)
        SC.setSchemBlock(self.masterSchem, 17, 5, 17, 25)
        SC.setSchemBlock(self.masterSchem, 17, 5, 1, 25)

        # place the redstone repeaters for the delay
        # place the redstone repeaters for the delay
        delayLeft = cannonDelay
        delay4 = 0
        delay3 = 0
        delay2 = 0
        delay1 = 0
        # print('delayLeft: ' + str(delayLeft))
        if delayLeft >= 4:
            delay4 += delayLeft // 4
            delayLeft = delayLeft % 4
        if delayLeft >= 3:
            delay3 += delayLeft // 3
            delayLeft = delayLeft % 3
        if delayLeft >= 2:
            delay2 += delayLeft // 2
            delayLeft = delayLeft % 2
        if delayLeft >= 1:
            delay1 += delayLeft

        delayxoffset = 0
        # print('delayLeft: ' + str(delayLeft))
        # ('delay4: ' + str(delay4), 'delay3: ' + str(delay3), 'delay2: ' + str(delay2), 'delay1: ' + str(delay1))
        # for 10 times
        for i in range(0, 10):
            while delay4 > 0:
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 1, 26)
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 17, 26)
                delayxoffset += 1
                delay4 -= 1
            while delay3 > 0:
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 1, 27)
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 17, 27)
                delayxoffset += 1
                delay3 -= 1
            while delay2 > 0:
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 1, 28)
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 17, 28)
                delayxoffset += 1
                delay2 -= 1
            while delay1 > 0:
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 1, 29)
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 17, 29)
                delayxoffset += 1
                delay1 -= 1
            if delay1 and delay2 and delay3 and delay4 == 0 and delayxoffset < 10:
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 1, 3)
                SC.setSchemBlock(self.masterSchem, 5 + delayxoffset, 5, 17, 3)
                delayxoffset += 1

        # place the gold block for the cannon to fire
        SC.setSchemBlock(self.masterSchem, 4, 6, 10, 7)

        # end the timer
        end = time.time()
        # print("Time to build the cannon schem: " + str(end - start))

        # time how long it takes to place the schematic
        start = time.time()

        SC.placeBlocksTarget(self.masterSchem, [self.cannonPos[0], self.cannonPos[1] - 5, self.cannonPos[2] - 4],
                             'CH3ST')

        # end the timer
        end = time.time()
        print("Time to place the cannon schem in the world: " + str(end - start))

        # some blocks need to be placed again because they are not placed correctly the first time for some reason
        # it is random which blocks need to be placed again but it's always the same type of blocks
        # placing them again fixes the problem

        # clear the master schematic except for the redstone components and the snow layers
        for x in range(0, schemsizexz):
            for y in range(0, schemsizey):
                for z in range(0, schemsizexz):
                    if self.masterSchem[x][y][z] != 3 and self.masterSchem[x][y][z] != 8 and self.masterSchem[x][y][
                        z] != 9 and self.masterSchem[x][y][z] != 25 and self.masterSchem[x][y][z] != 24 and \
                            self.masterSchem[x][y][z] != 15 and self.masterSchem[x][y][z] != 16 and \
                            self.masterSchem[x][y][z] != 17 and self.masterSchem[x][y][z] != 18 and \
                            self.masterSchem[x][y][z] != 19 and self.masterSchem[x][y][z] != 20 and \
                            self.masterSchem[x][y][z] != 21 and self.masterSchem[x][y][z] != 22:
                        self.masterSchem[x][y][z] = 0

        # time to replace the redstone components
        redstonestart = time.time()
        SC.placeBlocksTarget(self.masterSchem, [self.cannonPos[0], self.cannonPos[1] - 5, self.cannonPos[2] - 4],
                             'CH3ST')
        redstoneend = time.time()
        print("Time to replace the redstone: " + str(redstoneend - redstonestart))

        # you you need to wait for the observers to quit giving out a signal before filling the cannon
        # otherwise the cannon will fire prematurely and the cannon will be destroyed
        MC.tickWarp(40)
        time.sleep(.2)
        height = int(height)

        fire.fillCannon(player, self.cannonPos, height)
        print('cannon filled')
        time.sleep(.2)

        fire.fireCannon(player, self.cannonPos)

        MC.tickWarp(200)
        time.sleep(.15)

        # MC.setPos(player, self.targetPos[0]-20, self.targetPos[1], self.targetPos[2]-20)

        # the chunks need to be loaded for the tnt to fly to the target
        # if the distance between the cannon and the target is greater than 100 blocks, load the chunks

        MC.loadChunks(self.cannonPos, self.targetPos, player)

        #MC.tickWarp(160)
        time.sleep(.3)
        # print(f' action {action} taken at {self.currentschempos}')
        time.sleep(7)
        # print(self.cannonPos)
        try:
            reward = MC.checkDamage(player, self.targetPos)
        except:
            reward = 0
        end = time.time()
        print(end - start)

        Done = True
        info = {}

        self.episode_rewards_level.append(reward)

        avg_reward = 0
        # print(f'episode_reward: {episode_rewards}, average_reward: {self.averageReward}')
        # calculate the average reward for the last 20 episodes
        if len(self.episode_rewards_level) > self.averageRewardBin:
            if sum(self.episode_rewards_level[-self.averageRewardBin:]) != 0:
                avg_reward = sum(self.episode_rewards_level[-self.averageRewardBin:]) / self.averageRewardBin
                # clear the episode rewards
                self.episode_rewards_level = []
        # fix division by zero error
        else:
            avg_reward = 0

        # if the length of the episode rewards is greater than the average reward bin, remove the oldest reward
        if len(self.episode_rewards_level) > self.averageRewardBin:
            self.episode_rewards_level.pop(0)

        # round avg_reward to nearest integer
        avg_reward = round(avg_reward)

        self.averageReward = avg_reward
        print(f'episode_reward: {reward}, average_reward: {self.averageReward}')
        print(f'episode rewards for level: {self.episode_rewards_level}')

        state = self.targetDistance, self.targetHeight

        return state, reward, Done, info


import matplotlib.pyplot as plt

episode_rewards = []




#create a demo function to run the trained model. Make it so that I can input the target distance and height.
#Also add an option to run 10 episodes with random distances and heights
#You can use the train function as a template for this function
def demo():
    # create environment
    env_name = "CannonEnv-v0"

    has_continuous_action_space = True  # continuous action space; else discrete

    env = Cannon()

    # state space dimension
    state_dim = env.observation_space.shape[0]

    # action space dimension
    if has_continuous_action_space:
        action_dim = env.action_space.shape[0]
    else:
        action_dim = env.action_space.n


    #load in PPO_CannonEnv-v0_0_0.pth from PPO_preTrained>CannonEnv-v0
    checkpoint_path = "PPO_preTrained/CannonEnv-v0/PPO_CannonEnv-v0_0_0.pth"

    # create agent

    # Create agent
    lr_actor = 0.009  # Learning rate for actor network
    lr_critic = 0.013  # Learning rate for critic network
    gamma = 0.99  # Discount factor
    K_epochs = 2  # Update policy for K epochs in one PPO update
    eps_clip = 0.9  # Clip parameter for PPO

    ppo_agent = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip, has_continuous_action_space)
    ppo_agent.load(checkpoint_path)

    state = env.reset()
    done = False
    episode_reward = 0

    print("distance: ", env.targetDistance)
    print("height: ", env.targetHeight)

    action = ppo_agent.select_action(state)
    actionmultiplier = 16
    # ('raw action: ', action)
    action[0] = action[0] * actionmultiplier
    action[1] = action[1] * actionmultiplier
    action[2] = action[2] * actionmultiplier

    # normalize action[0]
    # action[0] = (action[0] - 0) / 8

    # normalize action[1]
    # action[1] = (action[1] - 0) / maxCannonPower

    # normalize action[2]
    # action[2] = (action[2] - 0) / 29

    # reverse normalization of action[0]
    # action[0] = action[0] * 8

    # reverse normalization of action[1]
    # action[1] = action[1] * maxCannonPower

    # reverse normalization of action[2]
    # action[2] = action[2] * 29

    # reduce the action values to prevent unstable training

    # action[0] = action[0] / 4

    # action[1] = action[1] / 4

    # action[2] = action[2] / 4

    for i in range(len(action)):
        action[i] = math.ceil(action[i])
        action[i] = abs(action[i])

    if action[0] > 8:
        action[0] = 8
    if action[1] > maxCannonPower:
        action[1] = maxCannonPower
    if action[2] > 29:
        action[2] = 29
    if action[2] <= 1:
        action[2] = 1

    print("action going to env : ", action)

    state, reward, done, _ = env.step(action)
    episode_reward += reward
    if reward > 101:
        print("Directly hit target!")
    if reward < 101:
        print("Near miss!")
    if reward < 1:
        print("Complete miss!")


demo()