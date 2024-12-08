import json
from datetime import datetime

class LeaderboardManager:
    def __init__(self, filepath="data/leaderboard.json"):
        self.filepath = filepath

    def get_leaderboard(self, level):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                return data.get(level, [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def update_leaderboard(self, level, score):
        # Load existing leaderboard
        leaderboard = self.get_leaderboard(level)

        # If there are already 10 scores, only save if better than the 10th
        if len(leaderboard) >= 10 and score <= leaderboard[-1]["score"]:
            return False  # Do not update if the score is not better

        # Add the new score with timestamp
        new_entry = {
            "score": score,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y")
        }
        leaderboard.append(new_entry)

        # Sort by score (descending) and trim to top 10
        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

        # Save the updated leaderboard
        self._save_to_file(level, leaderboard)

        return True  # Indicate the leaderboard was updated

    def _save_to_file(self, level, leaderboard):
        """Helper method to save leaderboard data to the JSON file."""
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[level] = leaderboard
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)