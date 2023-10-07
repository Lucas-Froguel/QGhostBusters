import dataclasses

import numpy as np
from numpy import sign
from pygame import Vector2
from pygame.image import load
from pygame.mixer import Channel
from pygame.sprite import RenderUpdates
from pygame.transform import scale
from src.Units.base_unit import Unit
from src.Units.splitter import GhostSplitter
from src.Units.trap import Trap
from src.Units.utils import (
    two_ghost_coming_from_different_sides_of_splitter,
    beam_splitter,
    is_in_given_radius,
    find_tensored_components,
)
from src.settings import (
    GHOST_ATTACK_RADIUS,
    PROB_GHOST_ATTACK,
    PROB_GHOST_TRAP,
    MAX_DIFFICULTY,
)
from src.settings import GHOST_SPEED, MAX_GHOSTS_PER_STATE
from src.SoundEffects.sound_manager import GhostSoundManager

from qutip import ket, tensor, qeye

DIR_DICT = {"L": (-1, 0), "R": (1, 0), "D": (0, -1), "U": (0, 1)}


class Ghost(Unit):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        last_move: Vector2 = None,
        channel: Channel = None,
        splitters: GhostSplitter = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        """

        super().__init__(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )
        self.image = load("src/Units/sprites/ghost.png")
        self.image = scale(self.image, self.cellSize)
        self.splitters = splitters
        self.waypoint = None
        self.random_generator = np.random.default_rng()

        self.sound_manager = GhostSoundManager(channel=self.channel)
        self.last_move = last_move if last_move else Vector2(-1, 0)
        self.follow_player_chance = 0.5  # 0 <= agg <= 1 (1 is more aggressive)
        self.attack_radius = GHOST_ATTACK_RADIUS
        self.prob_ghost_attack = 0.5
        self.follow_waypoint_chance = 0.5
        self.detect_player_radius = self.attack_radius + 3
        self.is_alive = True

    def set_waypoint(self):
        self.waypoint = np.random.choice(self.splitters).position

    def choose_move_vector(self, direction: Vector2) -> Vector2:
        moveVector = self.random_generator.choice(
            [(sign(direction.x), 0), (0, sign(direction.y))],
            p=[abs(direction.x) ** 2, abs(direction.y) ** 2],
        )
        moveVector = Vector2(moveVector[0], moveVector[1])
        return moveVector

    def walk_to_waypoint(self) -> Vector2:
        direction = (self.waypoint - self.position).normalize()
        return self.choose_move_vector(direction)

    def walk_to_player(self, player_position: Vector2 = None) -> Vector2:
        direction = (player_position - self.position).normalize()
        return self.choose_move_vector(direction)

    def calculate_move_vector(self, player=None) -> Vector2:
        if np.random.random() < GHOST_SPEED:
            return Vector2(0, 0)

        if (
            is_in_given_radius(
                player.position, self.position, radius=self.detect_player_radius
            )
            and np.random.random() < self.follow_player_chance
            and not np.allclose(player.position, self.position)
        ):
            moveVector = self.walk_to_player(player_position=player.position)
        elif np.random.random() > self.follow_waypoint_chance and not np.allclose(
            self.position, self.waypoint
        ):
            moveVector = self.walk_to_waypoint()
        else:
            x, y = DIR_DICT[np.random.choice(list(DIR_DICT.keys()))]
            moveVector = Vector2(x, y)

        return moveVector

    def check_if_hit_by_shot(self, shots=None):
        for shot in shots:
            if (shot.position - self.position).length() <= 0.5:
                self.is_alive = False
                shot.is_alive = False
                break

    def update(self, player):
        if not self.waypoint or np.allclose(self.position, self.waypoint):
            self.set_waypoint()  # make sure it is a different waypoint

        self.check_if_hit_by_shot(shots=player.weapon.shots)
        moveVector = self.calculate_move_vector(player=player)
        super().update(moveVector=moveVector)
        self.last_move = moveVector


class AggressiveGhost(Ghost):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        last_move: Vector2 = None,
        channel: Channel = None,
        splitters: GhostSplitter = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            position=position,
            last_move=last_move,
            channel=channel,
            splitters=splitters,
        )
        self.follow_player_chance = 0.9
        self.follow_waypoint_chance = 0.3
        self.attack_radius = GHOST_ATTACK_RADIUS + 2
        self.prob_ghost_attack = 0.8
        self.detect_player_radius = self.attack_radius + 2


class PassiveGhost(Ghost):
    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        last_move: Vector2 = None,
        channel: Channel = None,
        splitters: GhostSplitter = None,
    ):
        super().__init__(
            cellSize=cellSize,
            worldSize=worldSize,
            position=position,
            last_move=last_move,
            channel=channel,
            splitters=splitters,
        )
        self.follow_player_chance = 0.8
        self.follow_waypoint_chance = 0.8
        self.attack_radius = GHOST_ATTACK_RADIUS - 2
        self.prob_ghost_attack = 0.5
        self.detect_player_radius = GHOST_ATTACK_RADIUS + 4

    def walk_to_player(self, player_position: Vector2 = None) -> Vector2:
        moveVector = super().walk_to_player(player_position=player_position)
        return -moveVector


@dataclasses.dataclass
class GhostParameters:
    attack_probability: float = PROB_GHOST_ATTACK
    trap_probability: float = PROB_GHOST_TRAP
    max_difficulty: int = MAX_DIFFICULTY
    difficulty: int = 3

    def change_difficulty(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.trap_probability = PROB_GHOST_TRAP * (
            self.difficulty / self.max_difficulty
        )
        self.attack_probability = PROB_GHOST_ATTACK * (
            self.difficulty / self.max_difficulty
        )


class QGhost(Ghost):
    """
    A quantum ghost that may be in a superposition.
    Parts of the superposition are implemented as Ghost instances
    """

    def __init__(
        self,
        cellSize: Vector2 = None,
        worldSize: Vector2 = None,
        position: Vector2 = None,
        splitters: list[GhostSplitter] = None,
        render_group: RenderUpdates = None,
        channel: Channel = None,
        ghost_parameters: GhostParameters = None,
    ):
        """
        :param cellSize: cellSize is the size of each cell/block in the game
        :param worldSize: size of the map
        :param position: position on the map (in units of cells)
        :param render_group: a pointer to the visualisation parameters
        """
        super().__init__(
            cellSize=cellSize, worldSize=worldSize, position=position, channel=channel
        )
        # initialize it in |1>. Allow maximum MAX_GHOSTS_PER_STATE ghosts in one state
        self.quantum_state = ket([1], MAX_GHOSTS_PER_STATE)
        self.visible_parts: [Ghost] = []
        self.dead_ghosts: [Ghost] = []
        self.cellSize = cellSize
        self.splitters = splitters
        self.render_group = render_group
        self.possible_ghosts = [AggressiveGhost, PassiveGhost]
        self.random_generator = np.random.default_rng()
        self.add_visible_ghost(start_position=position)
        self.options = (
            GhostParameters() if ghost_parameters is None else ghost_parameters
        )

    def collapse_wave_function(self, player=None):
        n_ghosts = len(self.visible_parts)
        if n_ghosts == 1:
            return False
        for i, ghost in enumerate(self.visible_parts):
            if is_in_given_radius(
                player.position, ghost.position, player.measure_radius
            ):
                probs = np.abs(self.quantum_state.full()[:, 0]) ** 2
                # choose one vector to survive based on its probability
                surviving_state_idx = np.random.choice(
                    list(range(MAX_GHOSTS_PER_STATE**n_ghosts)),
                    p=probs / np.sum(probs),
                )
                numbers_of_ghosts_here = find_tensored_components(
                    surviving_state_idx, n_ghosts
                )

                self.quantum_state = ket(
                    numbers_of_ghosts_here[numbers_of_ghosts_here > 0],
                    MAX_GHOSTS_PER_STATE,
                )
                surviving_state_index = set(np.where(numbers_of_ghosts_here > 0)[0])
                for k in range(n_ghosts - 1, -1, -1):
                    if k not in surviving_state_index:
                        self.visible_parts[k].is_alive = False

                self.remove_visible_ghosts(is_measurement=True)
                return True
        return False

    def remove_visible_ghosts(self, is_measurement: bool = False):
        initially_alive_ghosts = self.visible_parts
        alive_ghosts = []
        dead_ghosts = []
        for ghost in self.visible_parts:
            if ghost.is_alive:
                self.render_group.add(ghost)
                alive_ghosts.append(ghost)
            else:
                dead_ghosts.append(ghost)
                self.render_group.remove(ghost)

        self.dead_ghosts = dead_ghosts
        if not is_measurement:
            self.destroy_dead_ghosts_quantum_state(initially_alive_ghosts)
        self.visible_parts = alive_ghosts

    def add_visible_ghost(
        self, start_position: Vector2 = None, last_move: Vector2 = None
    ):
        ghost_type = self.random_generator.choice(self.possible_ghosts)
        ghost = ghost_type(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            position=start_position,
            last_move=last_move,
            splitters=self.splitters,
            channel=self.channel,
        )
        self.visible_parts.append(ghost)
        self.render_group.add(ghost)

    def attack(self, player) -> None:
        """
        If a ghost is near the player, it attacks.
        All the parts of the superposition attack equally.
        """
        attack_prob = 0
        for i, ghost in enumerate(self.visible_parts):
            if is_in_given_radius(player.position, ghost.position, ghost.attack_radius):
                p_not_here = (
                    tensor(
                        [
                            ket([0], MAX_GHOSTS_PER_STATE).dag()
                            if g == i
                            else qeye(MAX_GHOSTS_PER_STATE)
                            for g in range(len(self.visible_parts))
                        ]
                    )
                    * self.quantum_state
                ).norm()
                attack_prob += (1 - p_not_here) * ghost.prob_ghost_attack
        if np.random.random() <= attack_prob:
            player.health -= 1
            self.sound_manager.play_attack_sound()

    def lay_trap(self, traps: list[Trap]) -> None:
        trap_laying_ghost = np.random.choice(self.visible_parts)
        for trap in traps:
            # check if position already taken
            if trap.position == trap_laying_ghost.position:
                return
        trap = Trap(
            cellSize=self.cellSize,
            worldSize=self.worldSize,
            position=trap_laying_ghost.position,
            channel=self.channel,
        )
        traps.append(trap)

    def destroy_dead_ghosts_quantum_state(self, old_visible):
        if not self.dead_ghosts:
            return
        new_state = (
            tensor(
                [
                    ket([0], MAX_GHOSTS_PER_STATE).dag()
                    if ghost in self.dead_ghosts
                    else qeye(MAX_GHOSTS_PER_STATE)
                    for ghost in old_visible
                ]
            )
            * self.quantum_state
        )

        if new_state.norm():
            self.quantum_state = new_state.unit()
        else:
            self.is_alive = False

    def interact_with_splitter(self) -> None:
        seen = set()
        for splitter in self.splitters:
            for i, this_ghost in enumerate(self.visible_parts[:]):
                if i in seen:
                    continue
                if np.allclose(splitter.position, this_ghost.position, 1e-2):
                    is_coincidence = False
                    for j, other_ghost in enumerate(self.visible_parts[i:]):
                        # check 2 ghosts at the same tile case
                        if two_ghost_coming_from_different_sides_of_splitter(
                            this_ghost, other_ghost, splitter.splitterType
                        ):
                            is_coincidence = True
                            self.quantum_state = beam_splitter(self.quantum_state, i, j)
                            seen |= {i, i + j}
                    if not is_coincidence:
                        last_move = (-1) ** (splitter.splitterType == "45") * Vector2(
                            this_ghost.last_move.y, this_ghost.last_move.x
                        )

                        self.add_visible_ghost(
                            start_position=this_ghost.position, last_move=last_move
                        )
                        self.quantum_state = beam_splitter(self.quantum_state, i)

    def update(self, player, traps) -> None:
        """
        After all the ghosts are in position, we can:
            1. change their state if they hit the splitter
            2. let them attack the player

        :param player: instance of the Player class carrying information about player's position & health
        """
        if len(self.visible_parts) < MAX_GHOSTS_PER_STATE:
            self.interact_with_splitter()

        self.remove_visible_ghosts()

        if np.random.random() <= self.options.attack_probability:
            self.attack(player)
        elif np.random.random() <= self.options.trap_probability:
            self.lay_trap(traps)

        if not self.visible_parts:
            self.is_alive = False
