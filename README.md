# CannonRL
Minecraft cannons controlled by AI.


To try this for yourself do this...

Open the fabric server folder

Double click fabric-server-launch

Open Minecraft 1.18.2
Minecraft with Sodium is highly preferred. I didn't test this without it.

Go to multiplayer and add a server
Input "localhost" as the server ip

Connect to the server

Open Pycharm or VS Code and run the test.py file


If you run train.py it will crash the program due to the path in MC.restartServerAndMC not being usuable for your PC
Running train.py will also overwrite the checkpoint in the checkpoint folder
train.py will also take control of your mouse and it might do something it shouldn't because of how MC.restartServerAndMC works


If your PC is slow, the program might not work because the program is meant to run MC at 50-300 times normal speed during certain times
The program might move on and do something it shouldn't if your PC is too slow



