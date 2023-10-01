# QGhostBusters
This is the game of Quantum Enigma team at the Quantum Games Hackaton 2023

# Story

Welcome to Qhost Busters! This game makes the player live the role of ghost buster, a person whose job is to find and
destroy ghosts. 

# Rules

Ghosts are quantum mechanical entities and, therefore, follow odd rules. They can move through surfaces (quantum tunneling) and
exist in superposition of states. 

The objective of the ghost buster is to kill all ghosts in the map. In order to achieve that, the player must approach a ghost
and use its raygun to kill it. However, beware of the quantum mechanics! If the ghost were in a superposition, it will 
remain alive - though one of its parts will die - which means the player has to kill all parts of the ghost. Alternatively,
the player can choose to measure the ghost, which will cause they ghost to collapse to a single position again ($1/N$ 
probability to be in each previous space). 

The player can also leave traps behind, which will also measure anything that goes over them and thus help the player. 

On the other hand, ghosts can attack the player and also leave their plasmas on the floor as traps. If the player goes over
such a plasma, he gets stuck for a couple seconds. 

# Meta progression

We are planning to add meta-progression, but it will depend on our progress on the other aspects of the game. 

# Documentation

Our world is a grid of squares of fixed size. The size of the squares is determined by `cellSize` variable. The amount
of squares is determined by `worldSize` variable. Naturally, the product `cellSize * worldSize` (has to!) yields the size of the 
map. 

Each unit has a `position`, which holds the information of the cell they are in. The variable `rect` contains their
actual position in the map. 

