# QGhostBusters
This is the game of Quantum Enigma team at the Quantum Games Hackaton 2023.

The gameplay video is accessible [here](https://youtu.be/WAo3_sGQMmc).
![background_menu.png](images%2Fbackground_menu.png)

# Story

Welcome to "Qhost Busters"! In this captivating game, you step into the shoes of a fearless ghost buster, tasked with the thrilling mission of tracking down and vanquishing malevolent spirits. Prepare for a spine-tingling journey through a series of haunted locales that demand your supernatural expertise.

As the player, you assume the role of a seasoned ghost buster with a unique background. Your character possesses a deep connection to the supernatural world, perhaps stemming from a family legacy of ghost hunters or a personal encounter with the paranormal at a young age, which allows you to see ghosts without interfering in their existence. Armed with an arsenal of cutting-edge ghost-busting gadgets and unwavering determination, you've dedicated your life to protecting both the living and the departed from the otherworldly threats that lurk in the shadows.

In the world of "Qhost Busters", a group of pioneering scientists known as "Ecto-Physicists" has made astonishing discoveries about the nature of ghosts. Drawing inspiration from the bizarre behavior of unobserved photons in quantum physics, these intrepid researchers have unraveled the enigmatic properties of ghosts. Their groundbreaking work has revealed that these spectral entities exist in multiple states simultaneously, just like particles in quantum superposition. This revelation has forever altered our understanding of the supernatural realm, paving the way for a new era of ghost hunting. Armed with this knowledge, you embark on missions that challenge both your wits and your grasp of quantum reality, making you the last line of defense against the eerie forces that defy explanation.

However, while you embark on your ghost-hunting quests, be prepared for a chilling showdown with these spectral adversaries. These vengeful apparitions are not just lurking in the shadows; they are capable of launching relentless attacks against you. Their ethereal forms can morph into terrifying manifestations, from bone-chilling phantasms to eerie poltergeists, all intent on thwarting your ghost-busting mission.

But the danger doesn't end there. Ghosts have another cunning trick up their ectoplasmic sleeves. As they roam the haunted locations, they can leave behind mysterious and hazardous plasmas scattered across the floor. These ghostly remnants act as sinister traps, lurking in plain sight, waiting for an unsuspecting step. Should you unknowingly tread upon one of these malevolent plasmas, a jolt of spectral energy surges through you, causing significant damage.

Your keen observation and quick reflexes will be your greatest allies as you navigate these treacherous terrains. The eerie battle between the living and the spectral world unfolds with each step you take, creating an intense and heart-pounding experience that will test your courage and ghost-busting skills to the limit. Stay vigilant, for the shadows hold secrets, and the ghosts will stop at nothing to defend their supernatural domain.

This is a world where the line between reality and the supernatural blurs, leaving you to decipher which seemingly ordinary locations harbor these elusive apparitions. Will you be able to unveil the hidden hauntings and put an end to their ethereal mischief?

Some of the mysterious, haunted locations are:

![the_caves.png](images%2Fthe_caves.png)

[![Gameplay video1](https://img.youtube.com/vi/WAo3_sGQMmc/maxresdefault.jpg)](https://youtu.be/WAo3_sGQMmc)

[![Gameplay video2](https://img.youtube.com/vi/NRey1MnxBLY/maxresdefault.jpg)](https://youtu.be/NRey1MnxBLY)

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

On the other hand, ghosts can attack the player and also leave their plasmas on the floor as traps. If the player goes over
such a plasma, he gets damaged. 

# Controls

- Arrows or WASD keys to move.
- Space to bust ghosts with your gun.
- X to measure ghosts' position, but beware: this is a costly operation, and you'll need to wait for your Professor to gather funding for the next measurement.   


# Physical world inspiration

The ghosts as implemented in this game are inspired on photons following different paths. Their spatial superposition is
achieved by passing through beam splitters, and if several ghosts do this at the same time, they interfere similarly to Hong-Ou-Mandel effect.

The ghosts attack the player, so to avoid collapsing superposition from the back-action, we put the attack raduis quite large, so that we 
can't know where the blow is coming from.

# Installation instructions:

## Windows

Prerequisites:
   - Windows does not allow to execute scripts by default. If you haven't enabled this option, you should start by opening PowerShell and executing `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
   - You need git installed for cloning. You can download it [here](https://git-scm.com/download/win).
   - You need Python installed. You can download it [here](https://www.python.org/downloads/windows/).
   - Life will be simpler if you add Python to your `PATH` variable

Install without console:
1. Go to a directory where you want the game installed.
2. Copy `./installers/install_on_windows.exe` into that folder and run it (it replicates contents of the ps1 file in the same folder)
3. Next time to run the game just copy `./installers/play_on_windows.exe` into QGhostBusters folder and run it from there. 

Install with console (if exe file did not work for some reason)
1. Go to a directory where you want the game installed via `cd .\path\to\the\directory`, e.g. `cd ~\games\QGhostBusters>`.
2. Clone the repo: `git clone -b development https://github.com/Lucas-Froguel/QGhostBusters.git`.
3. Get inside the game directory: `cd QGhostBusters`
4. Create virtual environment: `python -m venv venv` (if you don't have path to Python in your enviromnent PATH, instead of `python` type the path to `Python.exe` file including the `exe` itself)
5. Get inside it `.\venv\Scripts\activate`
6. Install the required packages `pip install -r requirements.txt`
7. Run `python main.py` to play.

## Linux

1. Prerequisites:
   - You need git installed for cloning.
   - You need Python installed.
2. Run `./installers/linux_install.sh` to download the necessary packages.
3. Run `./installers/linux_play.sh` to play the game.


# Acknowledgement

Thanks to Szadi art for the free sprites made available online for free use. More of his work can be found [here](https://szadiart.itch.io/).

# License

This game is published under the MIT license. 
