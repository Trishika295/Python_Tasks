from flask import Flask, jsonify, request
from flask_cors import CORS

from game import GuessingGame


app = Flask(__name__)

# Allow React frontend to communicate with Flask
CORS(app)


# Create a game
game = GuessingGame(1, 100)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Number Guessing Game API is running!"
    })


@app.route("/api/start", methods=["POST"])
def start_game():

    game.reset()

    return jsonify({
        "success": True,
        "message": "New game started!",
        "minimum": game.minimum,
        "maximum": game.maximum,
        "attempts": game.attempts,
        "guesses": game.guesses,
        "game_over": game.game_over
    })


@app.route("/api/guess", methods=["POST"])
def make_guess():

    data = request.get_json()

    if not data or "guess" not in data:
        return jsonify({
            "success": False,
            "message": "Please enter a guess."
        }), 400

    try:
        guess = int(data["guess"])

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message": "Please enter a valid whole number."
        }), 400

    # Check range
    if guess < game.minimum or guess > game.maximum:

        return jsonify({
            "success": False,
            "message": (
                f"Please enter a number between "
                f"{game.minimum} and {game.maximum}."
            )
        }), 400

    result = game.make_guess(guess)

    return jsonify(result)


@app.route("/api/status", methods=["GET"])
def game_status():

    return jsonify({
        "success": True,
        "minimum": game.minimum,
        "maximum": game.maximum,
        "attempts": game.attempts,
        "guesses": game.guesses,
        "game_over": game.game_over
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )