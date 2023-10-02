import os
from dotenv import load_dotenv

load_dotenv()

MAX_GHOSTS_PER_STATE = int(os.getenv("MAX_GHOSTS_PER_STATE"))
GHOST_SPEED = float(os.getenv("GHOST_SPEED"))
ATTACK_RADIUS = float(os.getenv("ATTACK_RADIUS"))
