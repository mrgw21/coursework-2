import json
import os

class ScoreTracker:
    def __init__(self, leaderboard_file="data/leaderboard.json"):
        self.score = 0
        self.leaderboard = []
        self.leaderboard_file = leaderboard_file
        self.load_leaderboard()  # Load existing leaderboard from file

    def add_points(self, points):
        """Adds points to the score."""
        self.score += points

    def reset(self):
        """Resets the score to zero."""
        self.score = 0

    def get_score(self):
        """Returns the current score."""
        return self.score

    def add_to_leaderboard(self):
        """Adds the current score to the leaderboard and saves it."""
        if self.score != 0:  # Only add non-zero scores to leaderboard
            self.leaderboard.append(self.score)
            self.leaderboard.sort(reverse=True)
            self.save_leaderboard()

    def get_leaderboard(self):
        """Returns the leaderboard, sorted in descending order."""
        return self.leaderboard

    def save_leaderboard(self):
        """Saves the leaderboard to a file."""
        os.makedirs(os.path.dirname(self.leaderboard_file), exist_ok=True)  # Ensure directory exists
        with open(self.leaderboard_file, "w") as file:
            json.dump(self.leaderboard, file)

    def load_leaderboard(self):
        """Loads the leaderboard from a file."""
        try:
            with open(self.leaderboard_file, "r") as file:
                self.leaderboard = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.leaderboard = []  # Initialize with an empty list if file is not found or corrupted
