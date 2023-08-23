# <p align=center>AstroDestroyer</p>
# <p align=center> ![Title](https://github.com/EMobilio/AstroDestroyer/assets/109104115/983060f9-c930-4f28-968c-8b4aa8354214) </p>


## About
AstroDestroyer is a classic space shooter game with an educational twist. The original version of this game was my final project for the first coding class I ever took in
my freshman year of high school. The assignment was to create a game that included some sort of educational element. I came up with the idea of creating a mix of Space Invaders and Asteroids with the catch that players would need to answer simple math problems to reload their ammunition. Thus, AstroDestroyer was born. 

The original version was written in JavaScript and functioned fine, but due to my lack of experience, the source code was extremely inefficient and required over 7,000 repetitive lines of code. I no longer have access to that original version, so I decided to re-create the game in Python using Pygame and generally enhance it using all the programming knowledge I have acquired since that first class. 7,000+ lines of code turned into a few hundred, and the final product is much smoother and more polished and even contains many extra features including sound effects, high score tracking, and specially designed graphics done by myself.

There are still some potential improvements to be made. In the future I may add a pause feature, menus to display or possibly change the controls and toggle sounds, and more complex animations for asteroid destruction and ship explosion. I also may add some in-game power-ups.

![Gameplay](https://github.com/EMobilio/AstroDestroyer/assets/109104115/7c581b69-4f6b-4c76-8efb-8b31ee2a7218)

## How to Run
Before running, make sure you have Python installed.

Run the following to install dependencies:
```
pip install -r requirements.txt 
```
Then run it using
```
python main.py
```

## How to Play
Shoot the falling asteroids before they hit or pass your ship! Getting hit causes you to take damage and letting an asteroid pass you causes you to lose points. Be sure to use your ammo sparingly! The game will pause and a math problem will appear every 45 seconds. Answer correctly to get extra ammo. You have 3 lives. If you run out of lives or ammo, you lose! As you gain points, the difficulty will increase. Asteroids will start spawning more frequently and travel at higher speeds, and the math problems will get more difficult.

### Controls
- 'space' to shoot
- 'left' to move left
- 'right' to move right
- '0'-'9' and '-' to type answers
- 'return' to enter an answer

