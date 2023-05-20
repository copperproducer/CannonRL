import gym
import numpy as np

from utils import plot_learning_curve





import MCWrapper as MC
import SchemCode as SC
import numpy as np
import time
import gym
from gym import spaces
import math
import cv2
import fire
import torch as T
player = MC.getPlayerList()[0]
minDistance = 80
maxDistance = 300
schemsize = 200




cannonposnum = 7500

minCannonPosx = -cannonposnum
minCannonPosz = -cannonposnum

maxCannonPosx = cannonposnum
maxCannonPosz = cannonposnum

cannonPosStep = maxDistance+100


#https://www.gymlibrary.dev/



class Cannon:


    def __init__(self):
        player = MC.playerlist[0]
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([8, 300]), dtype=np.float32)
        self.targetDistance = MC.setTargetDistance(minDistance, maxDistance)
        self.cannonPos = MC.readPos()
        if self.cannonPos[2] >= maxCannonPosz:
            self.cannonPos[2] = minCannonPosz
            self.cannonPos[0] = self.cannonPos[0] - cannonPosStep

        self.cannonPos[2] = self.cannonPos[2] + 100
        MC.savePos(self.cannonPos[0], self.cannonPos[1], self.cannonPos[2])
        self.targetPos = [self.cannonPos[0] + self.targetDistance, self.cannonPos[1], self.cannonPos[2]]
        print (f'{self.targetPos} is the target position')
        MC.placeTarget(player, self.targetPos,)
        self.masterSchem = MC.createSchem(schemsize, schemsize, schemsize)
        self.cannonPos = MC.readPos()
        self.currentschempos = [0, 0, 0]


        #the observation space is the distance between the cannon and the target it can be any number between the min and max distance

        self.observation_space = spaces.Box(low=np.array([minDistance]), high=np.array([maxDistance]), dtype=np.float32)





    def reset(self):
        self.targetDistance = MC.setTargetDistance(minDistance, maxDistance)
        self.cannonPos = MC.readPos()
        self.cannonPos[2] = self.cannonPos[2] + 50
        MC.savePos(self.cannonPos[0], self.cannonPos[1], self.cannonPos[2])
        self.targetPos = [self.cannonPos[0] + self.targetDistance, self.cannonPos[1], self.cannonPos[2]]
        print (f'{self.targetPos} is the target position')
        MC.placeTarget(player, self.targetPos,)
        self.masterSchem = MC.createSchem(schemsize, schemsize, schemsize)
        self.cannonPos = MC.readPos()

        reward = 0
        done = False
        info = {}
        #return the observation
        return self.targetDistance







    def action(self, cannonAngle, cannonBarrelPower):

        cannonAngle = cannonAngle
        cannonBarrelPower = cannonBarrelPower

        return cannonAngle, cannonBarrelPower




    def placeSchem(self, schem, pos, player):
        MC.setCannon(schem, pos, player)
        return

    def step(self, action):
        #print (f'{action} is the action')
        #here lies the settings for the cannon. edit these for different cannon configurations
        print(f'{action} is the action')
        cannonAngle, cannonBarrelPower = self.action(action[0], action[1])

        schemsizexz = 25
        cannonProjectilePower = 5
        cannonDelay = 10

        #time how long this takes
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


        #this decides the height of stuff

        if cannonBarrelPower / 16 > cannonProjectilePower:
            cannonSpacer = SC.createCannonSpacer(math.ceil(cannonBarrelPower / 16) + 2)
            schemsizey = cannonBarrelPower + 20
            height = cannonBarrelPower + 10
        else:
            cannonSpacer = SC.createCannonSpacer(cannonProjectilePower + 2)
            schemsizey = cannonProjectilePower + 20
            height = cannonProjectilePower + 10

        schemsizey = int(schemsizey)

        print("schemsizexz: " + str(schemsizexz) + " schemsizey: " + str(schemsizey))

        self.masterSchem = SC.createSchem(schemsizexz, schemsizey, schemsizexz)

        # build the cannon
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

        SC.setSchemBlockLine(self.masterSchem, 5, 5, 1, 5 + cannonDelay, 5, 1, 25)
        SC.setSchemBlockLine(self.masterSchem, 5, 5, 17, 5 + cannonDelay, 5, 17, 25)

        # place the gold block for the cannon to fire
        SC.setSchemBlock(self.masterSchem, 4, 6, 10, 7)


        #end the timer
        end = time.time()
        print("Time to build the cannon schem: " + str(end - start))

        # time how long it takes to place the schematic
        start = time.time()

        SC.placeBlocksTarget(self.masterSchem, [self.cannonPos[0], self.cannonPos[1]-5, self.cannonPos[2]-4], 'CH3ST')

        #end the timer
        end = time.time()
        print("Time to place the cannon schem in the world: " + str(end - start))

        #some blocks need to be placed again because they are not placed correctly the first time for some reason
        #it is random which blocks need to be placed again but it's always the same type of blocks
        #placing them again fixes the problem


        #clear the master schematic except for the redstone components and the snow layers
        for x in range(0, schemsizexz):
            for y in range(0, schemsizey):
                for z in range(0, schemsizexz):
                    if self.masterSchem[x][y][z] != 3 and self.masterSchem[x][y][z] != 8 and self.masterSchem[x][y][z] != 9 and self.masterSchem[x][y][z] != 25 and self.masterSchem[x][y][z] != 24 and self.masterSchem[x][y][z] != 15 and self.masterSchem[x][y][z] != 16 and self.masterSchem[x][y][z] != 17 and self.masterSchem[x][y][z] != 18 and self.masterSchem[x][y][z] != 19 and self.masterSchem[x][y][z] != 20 and self.masterSchem[x][y][z] != 21 and self.masterSchem[x][y][z] != 22:
                        self.masterSchem[x][y][z] = 0


        #time to replace the redstone components
        redstonestart = time.time()
        SC.placeBlocksTarget(self.masterSchem, [self.cannonPos[0], self.cannonPos[1]-5, self.cannonPos[2]-4], 'CH3ST')
        redstoneend = time.time()
        print("Time to replace the redstone: " + str(redstoneend - redstonestart))


        #you you need to wait for the observers to quit giving out a signal before filling the cannon
        #otherwise the cannon will fire prematurely and the cannon will be destroyed
        MC.tickWarp(1000)
        time.sleep(.2)
        height = int(height)

        fire.fillCannon(player, self.cannonPos, height)

        fire.fireCannon(player, self.cannonPos)

        MC.tickWarp(1000)
        time.sleep(.3)

        #MC.setPos(player, self.targetPos[0]-20, self.targetPos[1], self.targetPos[2]-20)


        #the chunks need to be loaded for the tnt to fly to the target
        #if the distance between the cannon and the target is greater than 100 blocks, load the chunks
        if abs(self.cannonPos[0] - self.targetPos[0]) > 100 or abs(self.cannonPos[2] - self.targetPos[2]) > 100:
            MC.loadChunks(self.cannonPos, self.targetPos, player)




        end = time.time()
        print(end - start)





        time.sleep(.1)
        # print(f' action {action} taken at {self.currentschempos}')

        # print(self.cannonPos)

        reward = 4096 - MC.checkDamage(player, self.targetPos)

        Done = True
        info = {}

        return self.targetDistance, reward, Done, info






#
# if __name__ == '__main__':
#     env = Cannon()
#     N = 1
#     batch_size = 5
#     n_epochs = 4
#     alpha = 0.0003
#     device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
#     agent = Agent(n_actions=env.action_space.shape[0], action_space_shape=env.action_space.shape, batch_size=batch_size,
#                   alpha=alpha, n_epochs=n_epochs,
#                   input_dims=env.observation_space.shape, device=device)
#
#     n_games = 300
#
#     figure_file = 'plots/cartpole.png'
#
#     best_score = 4096
#     score_history = []
#
#     learn_iters = 0
#     avg_score = 0
#     n_steps = 0
#
#     for i in range(n_games):
#         observation = env.reset()
#         done = False
#         score = 0
#         while not done:
#             action, prob, val = agent.choose_action(observation)
#             observation_, reward, done, info = env.step(action)
#             n_steps += 1
#             score += reward
#             agent.remember(observation, action, prob, val, reward, done)
#             if n_steps % N == 0:
#                 agent.learn()
#                 learn_iters += 1
#             observation = observation_
#         score_history.append(score)
#         avg_score = np.mean(score_history[-100:])
#
#         if avg_score > best_score:
#             best_score = avg_score
#             agent.save_models()
#
#         print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score,
#                 'time_steps', n_steps, 'learning_steps', learn_iters)
#     x = [i+1 for i in range(len(score_history))]
#     plot_learning_curve(x, score_history, figure_file)
#

import optuna
import PPO
from PPO import PPO as Agent
def objective(trial):
    # Define the hyperparameters to tune
    learning_rate = trial.suggest_loguniform('learning_rate', 1e-5, 1e-1)
    gamma = trial.suggest_uniform('gamma', 0.1, 0.999)
    batch_size = trial.suggest_int('batch_size', 16, 128)

    # ... define other hyperparameters to tune ...

    # Create the environment and the agent using the hyperparameters
    env = gym.make('Cannon-v0')
    agent = Agent(env.observation_space.shape[0], env.action_space.shape[0], learning_rate, gamma, batch_size)

    # Train the agent for a certain number of episodes
    num_episodes = 100
    rewards = []
    for i in range(num_episodes):
        # ... run an episode and record the reward obtained ...
        rewards.append(reward)

    # Compute the mean reward obtained over the episodes
    mean_reward = np.mean(rewards)

    # Return the negative mean reward, as Optuna tries to minimize the objective
    return -mean_reward

objective(trial)
