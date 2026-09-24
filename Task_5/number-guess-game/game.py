import random


class GuessingGame:
    def __init__(self, minimum=1, maximum=100):
        self.minimum = minimum
        self.maximum = maximum
        self.reset()

    def reset(self):
        """Start a new game."""
        self.secret_number = random.randint(
            self.minimum,
            self.maximum
        )
        self.attempts = 0
        self.guesses = []
        self.game_over = False

    def make_guess(self, guess):
        """Process a player's guess."""

        # Prevent guesses after the game is completed
        if self.game_over:
            return {
                "result": "finished",
                "message": "The game is already over. Please start a new game.",
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        # Validate that the guess is an integer
        if not isinstance(guess, int):
            return {
                "result": "invalid",
                "message": "Please enter a valid integer.",
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        # Validate range
        if guess < self.minimum or guess > self.maximum:
            return {
                "result": "invalid",
                "message": (
                    f"Please enter a number between "
                    f"{self.minimum} and {self.maximum}."
                ),
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        # Record the guess
        self.attempts += 1
        self.guesses.append(guess)

        # Compare the guess
        if guess < self.secret_number:
            return {
                "result": "low",
                "message": "Too Low! Try a higher number.",
                "guess": guess,
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        elif guess > self.secret_number:
            return {
                "result": "high",
                "message": "Too High! Try a lower number.",
                "guess": guess,
                "attempts": self.attempts,
                "guesses": self.guesses
            }

        else:
            self.game_over = True

            return {
                "result": "correct",
                "message": (
                    f"Correct! You guessed the number "
                    f"in {self.attempts} attempts."
                ),
                "guess": guess,
                "attempts": self.attempts,
                "guesses": self.guesses
            }


# --------------------------------------------------
# Terminal Version
# --------------------------------------------------

if __name__ == "__main__":

    game = GuessingGame(1, 100)

    print("\n" + "=" * 45)
    print("       NUMBER GUESSING GAME")
    print("=" * 45)
    print("I have selected a number between 1 and 100.")
    print("Try to guess it!")
    print("Type 'q' to quit the game.")
    print("=" * 45)

    while not game.game_over:

        user_input = input("\nEnter your guess: ").strip()

        # Exit option
        if user_input.lower() == "q":
            print("\n Thanks for playing!")
            break

        # Check whether input is a number
        try:
            guess = int(user_input)

        except ValueError:
            print(" Invalid input!")
            print("Please enter a whole number between 1 and 100.")
            continue

        # Check range
        if guess < game.minimum or guess > game.maximum:
            print(
                f" Please enter a number between "
                f"{game.minimum} and {game.maximum}."
            )
            continue

        # Process guess
        result = game.make_guess(guess)

        # Display result
        if result["result"] == "low":
            print("⬇  Too Low! Try a higher number.")

        elif result["result"] == "high":
            print("⬆  Too High! Try a lower number.")

        elif result["result"] == "correct":
            print("\n Congratulations!")
            print(
                f" You guessed the correct number: "
                f"{game.secret_number}"
            )
            print(f" Total Attempts: {game.attempts}")
            print(f" Guess History: {game.guesses}")

    print("\n" + "=" * 45)
    print("              GAME OVER")
    print("=" * 45)