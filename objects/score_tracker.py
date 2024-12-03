class ScoreTracker:
    def __init__(self):
        self.score = 0

    def add_points(self, points):
        """Adds the specified number of points to the score."""
        self.score += points

    def reset(self):
        """Resets the score to zero."""
        self.score = 0

    def get_score(self):
        """Returns the current score."""
        return self.score
