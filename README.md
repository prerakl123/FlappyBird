# Flappy Bird
The famous Flappy Bird game developed by **Prerak Lodha**

# DESCRIPTION
The main game file is in the **game** folder.
Code has been provided in the **source** folder.

# How to play
  - If you don't have [Python](https://www.python.org/downloads/) or [Pygame](http://www.pygame.org/download.shtml) installed, you can simply double click the .exe file to play 
  the game.
  - If you have the correct version of Python and Pygame installed, you can run the program in the command prompt / terminal.

For Windows - 

`cd FlappyBird\source`

`python Flappy_Bird.py`

For Linux - 

`bash`
 
`cd FlappyBird\source`

`python Flappy_Bird.py`

This will work fine with most Python3 users, if not try `python3 Flappy_Bird.py`


# How to make into a _.exe_ file
First you should copy the _.py_ file to the game folder and install pyinstaller from cmd `pip install pyinstaller`.
In the _[game](https://github.com/prerakl123/FlappyBird/tree/master/FlappyBird/game)_ folder, while holding Shift key right click anywhere in the explorer and open Windows Power 
Shell.
Now type `pyinstaller .\Flappy_Bird.py --onefile -i .\sprites\bird.ico` in the Power Shell Window and wait until the _.exe_ file is created.
After the process is done you will see _dist_ and _build_ folders and a _.spec_ file, you may remove the _build_ folder and _.spec_ file but not the _dist_ folder, from that 
first cut-paste the _.exe_ file to **game** folder and now you may remove the _dist_ folder as well as the _.py_ file (if copied only else it is totally your choice).

