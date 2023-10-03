import os
from dotenv import load_dotenv

load_dotenv()
# player stats
INITIAL_HEALTH = int(os.getenv("INITIAL_HEALTH"))
PLAYER_MEASURE_RADIUS = float(os.getenv("PLAYER_MEASURE_RADIUS"))
PLAYER_ATTACK_RADIUS = float(os.getenv("PLAYER_ATTACK_RADIUS"))
# ghost stats
MAX_GHOSTS_PER_STATE = int(os.getenv("MAX_GHOSTS_PER_STATE"))
GHOST_SPEED = float(os.getenv("GHOST_SPEED"))
GHOST_ATTACK_RADIUS = float(os.getenv("GHOST_ATTACK_RADIUS"))
PROB_GHOST_ATTACK = float(os.getenv("PROB_GHOST_ATTACK"))
