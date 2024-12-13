import re
import csv
import random
import time
#Library for Game Logic
class Mole:
    def __init__(self, position):
        self.position = position
        self.visible = False

    def pop_up(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def __str__(self):
        return f"Mole at {self.position}, Visible: {self.visible}"
#Inheriting Mole for additional functionality
class TimedMole(Mole):
    def __init__(self, position, timer):
        super().__init__(position)
        self.timer = timer

    def countdown(self):
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            self.hide()
#File I/O Handling Library
def read_high_scores(file_name="high_scores.csv"):
    """Reads high scores from a CSV file"""
    try:
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def write_high_scores(scores, file_name="high_scores.csv"):
    """Writes high scores to a CSV file"""
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(scores)
#Regex Utilities
def validate_username(username):
    """Validates username using regex"""
    pattern = r"^[a-zA-Z0-9_]{3,15}$"
    return bool(re.match(pattern, username))

def filter_invalid_usernames(usernames):
    """Filters a list of usernames to remove invalid ones"""
    pattern = r"^[a-zA-Z0-9_]{3,15}$"
    return [username for username in usernames if re.match(pattern, username)]
#Whack-a-Mole Game Class
class WhackAMole:
    def __init__(self, grid_size=3):
        self.grid_size = grid_size
        self.moles = [TimedMole(i, random.randint(3, 6)) for i in range(grid_size)]
        self.score = 0
        self.time_remaining = 30

    def display_grid(self):
        """Displays the grid with moles"""
        grid = ""
        for mole in self.moles:
            grid += "[O]" if mole.visible else "[ ]"
        print(grid)

    def pop_random_mole(self):
        """Pops up a random mole"""
        mole = random.choice(self.moles)
        mole.pop_up()

    def whack(self, position):
        """Attempts to whack a mole at the given position"""
        if position < 0 or position >= len(self.moles):
            print("Invalid position! Please enter a number between 0 and {}.".format(len(self.moles) - 1))
            return

        mole = self.moles[position]
        if mole.visible:
            mole.hide()
            self.score += 1
            print("Hit!")
        else:
            print("Miss! There was no mole at position {}.".format(position))

    def update_moles(self):
        """Updates the state of all moles"""
        for mole in self.moles:
            mole.countdown()

    def get_valid_position(self):
        """Prompts the user to enter a valid position and handles errors"""
        while True:
            user_input = input("Enter position to whack (0-indexed or (x,y)): ").strip()
            # Check for single number
            if re.fullmatch(r"\d+", user_input):
                position = int(user_input)
                if 0 <= position < len(self.moles):
                    return position
                else:
                    print("Invalid position! Please enter a number between 0 and {}.".format(len(self.moles) - 1))
            # Check for coordinates in the form (x,y)
            elif re.fullmatch(r"\(\d+,\d+\)", user_input):
                x, y = map(int, user_input.strip("() ").split(","))
                position = x * self.grid_size + y
                if 0 <= position < len(self.moles):
                    return position
                else:
                    print("Invalid coordinates! Please enter valid (x,y) within the grid.")
            else:
                print("Invalid input! Please enter a valid number or coordinates in the format (x,y).")

    def play(self):
        """Main game loop"""
        print("Starting Whack-a-Mole! Press Ctrl+C to quit.")
        print("Instructions:")
        print("- You will see a grid representing mole positions.")
        print("- Enter the position (0-indexed) where you want to whack.")
        print("- Alternatively, you can enter coordinates in the format (x,y).")
        print("- Try to hit the moles when they pop up (indicated by [O]).")
        try:
            while self.time_remaining > 0:
                self.time_remaining -= 1
                self.update_moles()
                if random.random() < 0.5:
                    self.pop_random_mole()

                self.display_grid()
                position = self.get_valid_position()
                self.whack(position)
                time.sleep(1)

            print(f"Game over! Your score: {self.score}")
        except KeyboardInterrupt:
            print("Game interrupted!")
#Testing Section
import unittest

class TestRegexFunctions(unittest.TestCase):
#Check for invalid usernames.
    def test_validate_username(self):
        self.assertTrue(validate_username("Player1"))
        self.assertFalse(validate_username("Invalid Username"))

    def test_filter_invalid_usernames(self):
        usernames = ["ValidUser", "Invalid Username", "123"]
        filtered = filter_invalid_usernames(usernames)
        self.assertEqual(filtered, ["ValidUser"])

class TestFileIO(unittest.TestCase):
#Leaderboard mechanism for competing with another user.
    def test_read_write_high_scores(self):
        scores = [["Player1", "10"], ["Player2", "15"]]
        write_high_scores(scores, "test_scores.csv")
        read_scores = read_high_scores("test_scores.csv")
        self.assertEqual(scores, read_scores)

if __name__ == "__main__":
#Run tests
    unittest.main(exit=False)
#Start game
    game = WhackAMole()
    game.play()



