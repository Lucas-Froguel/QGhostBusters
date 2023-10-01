import os
from dotenv import load_dotenv

load_dotenv(".env.template")

GHOST_SPEED = float(os.getenv("GHOST_SPEED"))
ATTACK_RADIUS = float(os.getenv("ATTACK_RADIUS"))

