import random


class GuessingGame:
    def __init__(self, minimum=1, maximum=100):
        self.minimum = minimum
        self.maximum = maximum
        self.reset()

    def reset(self):
        self.secret_number = random.randint(
            self.minimum,
            self.maximum
        )
        self.attempts = 0
        self.guesses = []
        self.game_over = False

    def make_guess(self, guess):

        if self.game_over:
            return {
                "success": False,
                "result": "finished",
                "message": "The game is already over. Start a new game.",
                "game_over": True,
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        self.attempts += 1
        self.guesses.append(guess)

        if guess < self.secret_number:

            return {
                "success": True,
                "result": "low",
                "message": "Too low! Try a higher number.",
                "game_over": False,
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        elif guess > self.secret_number:

            return {
                "success": True,
                "result": "high",
                "message": "Too high! Try a lower number.",
                "game_over": False,
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        else:

            self.game_over = True

            return {
                "success": True,
                "result": "correct",
                "message": "Correct! You found the secret number!",
                "game_over": True,
                "attempts": self.attempts,
                "guesses": self.guesses
            }