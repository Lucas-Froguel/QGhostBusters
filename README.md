# QGhostBusters
This is the game of Quantum Enigma team at the Quantum Games Hackaton 2023

# Installation instructions:

## Windows

1. Prerequisites:
   - Windows does not allow to execute scripts by default. If you haven't enabled this option, you should start by opening PowerShell and executing `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
   - You need git installed for cloning. You can download it [here](https://git-scm.com/download/win).
   - You need Python installed. You can download it [here](https://www.python.org/downloads/windows/).
   - Life will be simpler if you add Python to your `PATH` variable
2. Go to a directory where you want the game installed via `cd .\path\to\the\directory`, e.g. `cd ~\games\QGhostBusters>`.
3. Clone the repo: `git clone -b development https://github.com/Lucas-Froguel/QGhostBusters.git`.
4. Get inside the game directory: `cd QGhostBusters`
5. Create virtual environment: `python -m venv venv` (if you don't have path to Python in your enviromnent PATH, instead of `python` type the path to `Python.exe` file including the `exe` itself)
6. Get inside it `.\venv\Scripts\activate`
7. Install the required packages `pip install -r requirements.txt`
8. Launch the game `python main.py`

## Linux

1. Prerequisites:
   - You need git installed for cloning.
   - You need Python installed.
2. Go to a directory where you want the game installed via `cd .\path\to\the\directory`, e.g. `cd ~\games\QGhostBusters>`.
3. Clone the repo: `git clone -b development https://github.com/Lucas-Froguel/QGhostBusters.git`.
4. Get inside the game directory: `cd QGhostBusters`
5. Create virtual environment: `python -m venv venv` (if you don't have path to Python in your enviromnent PATH, instead of `python` type the path to `Python.exe` file including the `exe` itself)
6. Get inside it `source venv/bin/activate`
7. Install the required packages `pip install -r requirements.txt`
8. Launch the game `python main.py`

# Story

Welcome to Qhost Busters! This game makes the player live the role of ghost buster, a person whose job is to find and
destroy ghosts. Though, being of a thinner nature than our own, ghosts exhibit quantum properties. And you can never
deterministically predict, which of the places where the ghost can be, is actually haunted.

# Rules

Ghosts are quantum mechanical entities and, therefore, follow odd rules. They can move through surfaces (quantum tunneling) and
exist in superposition of states.

The vortexes on the map allow the ghosts to manifest bi-location (and multi-location) by splitting them into superpositions of different visible forms.
If two ghosts of the same kind meet in such a spot, something incredible happens: they bunch into groups of two.
But the ghosts try to not disperse their powers too much, so they never allow to be splitted into too large superpositions, fearing that their thin form
becomes vanishing...

The objective of the ghost buster is to kill all ghosts in the map. In order to achieve that, the player must approach a ghost
and use its raygun to kill it. However, beware of the quantum mechanics!
The ghost-buster's life is complicated by the multi-location of the ghosts, as well as by their full indistinguishibility.
If the ghost were in a superposition, it will 
remain alive - though one of its parts will die - which means the player has to kill all parts of the ghost. Alternatively,
the player can choose to measure the ghost, which will cause they ghost to collapse to a single position again (with the 
probability to be in each previous space depending on how the ghosts interfered with each other previously).

The player can also leave traps behind, which will also measure anything that goes over them and thus help the player. 

On the other hand, ghosts can attack the player and also leave their plasmas on the floor as traps. If the player goes over
such a plasma, he gets stuck for a couple seconds. 

# Physical world inspiration

The ghosts as implemented in this game are inspired on photons following different paths. Their spatial superposition is
achieved by passing through beam splitters, and if several ghosts do this at the same time, they interfere similarly to Hon-Ou-Mandel effect.

The ghosts attack the player, so to avoid collapsing superposition from the back-action, we put the attack raduis quite large, so that we 
can't know where the blow is coming from.

# Meta progression

We are planning to add meta-progression, but it will depend on our progress on the other aspects of the game. 

# Documentation

Our world is a grid of squares of fixed size. The size of the squares is determined by `cellSize` variable. The amount
of squares is determined by `worldSize` variable. Naturally, the product `cellSize * worldSize` (has to!) yields the size of the 
map. 

Each unit has a `position`, which holds the information of the cell they are in. The variable `rect` contains their
actual position in the map.

# Acknowledgement

Thanks to Szadi art for the free sprites made available online for free use. More of his work can be found (here)[https://szadiart.itch.io/].

