import os
from dotenv import load_dotenv

load_dotenv()
# player stats
PLAYER_INITIAL_HEALTH = int(os.getenv("PLAYER_INITIAL_HEALTH"))
PLAYER_MEASURE_RADIUS = float(os.getenv("PLAYER_MEASURE_RADIUS"))
PLAYER_ATTACK_RADIUS = float(os.getenv("PLAYER_ATTACK_RADIUS"))
PLAYER_MEASURE_TIME = int(os.getenv("PLAYER_MEASURE_TIME"))
# ghost stats
MAX_GHOSTS_PER_STATE = int(os.getenv("MAX_GHOSTS_PER_STATE"))
GHOST_SPEED = float(os.getenv("GHOST_SPEED"))
GHOST_ATTACK_RADIUS = float(os.getenv("GHOST_ATTACK_RADIUS"))
PROB_GHOST_ATTACK = float(os.getenv("PROB_GHOST_ATTACK"))
PROB_GHOST_TRAP = float(os.getenv("PROB_GHOST_TRAP"))
# the difficulty impacts attack and trap laying probability,
# multiplying them my difficulty/max_difficulty
MAX_DIFFICULTY = int(os.getenv("MAX_DIFFICULTY"))
