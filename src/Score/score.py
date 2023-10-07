import pickle
import numpy as np

historic_scores = {
    "into_the_caves": {},
    "the_caves": {},
    "the_catacombs": {},
    "the_maze": {},
}


class ScoreSystem:
    def __init__(self):
        self.levels = ["into_the_caves", "the_caves", "the_catacombs", "the_maze"]
        self.num_of_high_scores: int = 5
        self.historic_scores: dict = None
        self.historic_scores_file: str = (
            "src/Score/historic_scores/historic_scores.pickle"
        )
        self.load_scores()

    def load_scores(self):
        with open(self.historic_scores_file, "rb") as file:
            self.historic_scores = pickle.load(file)

    def save_scores(self):
        with open(self.historic_scores_file, "wb") as file:
            pickle.dump(self.historic_scores, file=file)

    def add_score(self, map_id: str = None, score: int = None, player_name: str = None):
        self.historic_scores[map_id][player_name] = score

    def return_high_scores(self, map_id: str = None):
        if not self.historic_scores:
            self.load_scores()
        scores = self.historic_scores[map_id]

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_scores[: self.num_of_high_scores]

    @staticmethod
    def calculate_score(
        final_health: int = None,
        qghosts_killed: int = None,
        visible_ghosts_killed: int = None,
        max_ghosts_per_state: int = None,
        num_of_fallen_traps: int = None,
        total_level_time: float = None,
        level_difficulty: int = None,
    ):
        score = (
            100
            * level_difficulty
            * (1 + final_health)
            * np.tanh(
                1
                + (
                    qghosts_killed
                    + (visible_ghosts_killed / max_ghosts_per_state)
                    - num_of_fallen_traps
                )
            )
            / total_level_time
        )

        return int(score)
