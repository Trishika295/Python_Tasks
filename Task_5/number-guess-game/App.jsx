import React, { useState } from "react";
import "./style.css";

const API_URL = "http://127.0.0.1:5000/api";

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [guess, setGuess] = useState("");
  const [attempts, setAttempts] = useState(0);
  const [guesses, setGuesses] = useState([]);
  const [message, setMessage] = useState("");
  const [result, setResult] = useState("");
  const [gameOver, setGameOver] = useState(false);
  const [loading, setLoading] = useState(false);

  // Start or restart the game
  const startGame = async () => {
    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/start`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage("Unable to start the game.");
        return;
      }

      setGameStarted(true);
      setGuess("");
      setAttempts(0);
      setGuesses([]);
      setMessage(data.message);
      setResult("");
      setGameOver(false);

    } catch (error) {
      setMessage(
        "Unable to connect to the Python server. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };


  // Submit user's guess
  const submitGuess = async (event) => {
    event.preventDefault();

    if (!gameStarted) {
      setMessage("Please start the game first.");
      return;
    }

    if (guess.trim() === "") {
      setMessage("Please enter a number.");
      return;
    }

    const numericGuess = Number(guess);

    if (!Number.isInteger(numericGuess)) {
      setMessage("Please enter a whole number.");
      return;
    }

    if (numericGuess < 1 || numericGuess > 100) {
      setMessage("Please enter a number between 1 and 100.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/guess`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          guess: numericGuess,
        }),
      });

      const data = await response.json();

      setMessage(data.message);

      if (!response.ok) {
        return;
      }

      setResult(data.result || "");
      setAttempts(data.attempts);
      setGuesses(data.guesses);
      setGameOver(data.game_over);

      setGuess("");

    } catch (error) {
      setMessage(
        "Unable to connect to the Python server."
      );
    } finally {
      setLoading(false);
    }
  };


  // Get message style
  const getMessageClass = () => {
    if (result === "correct") {
      return "message correct";
    }

    if (result === "high") {
      return "message high";
    }

    if (result === "low") {
      return "message low";
    }

    return "message";
  };


  return (
    <div className="app">

      <div className="game-card">

        {/* Header */}
        <div className="header">

          <h1>
            Number Guessing Game
          </h1>

          <p>
            Guess the secret number between{" "}
            <strong>1</strong> and{" "}
            <strong>100</strong>
          </p>

        </div>


        {/* Start Screen */}
        {!gameStarted ? (

          <div className="start-section">

            <div className="number-icon">
              ?
            </div>

            <h2>
              Ready to Play?
            </h2>

            <p>
              I have selected a secret number between
              1 and 100. Can you find it?
            </p>

            <button
              className="primary-btn"
              onClick={startGame}
              disabled={loading}
            >
              {loading ? "Starting..." : "Start Game"}
            </button>

          </div>

        ) : (

          <>

            {/* Statistics */}
            <div className="stats">

              <div className="stat-box">
                <span>
                  Attempts
                </span>

                <strong>
                  {attempts}
                </strong>
              </div>


              <div className="stat-box">
                <span>
                  Number Range
                </span>

                <strong>
                  1 - 100
                </strong>
              </div>


              <div className="stat-box">
                <span>
                  Total Guesses
                </span>

                <strong>
                  {guesses.length}
                </strong>
              </div>

            </div>


            {/* Guess Form */}
            <form
              onSubmit={submitGuess}
              className="guess-form"
            >

              <label htmlFor="guess">
                Enter your guess
              </label>

              <input
                id="guess"
                type="number"
                min="1"
                max="100"
                value={guess}
                onChange={(event) =>
                  setGuess(event.target.value)
                }
                placeholder="Enter a number..."
                disabled={gameOver || loading}
              />

              <button
                type="submit"
                className="primary-btn"
                disabled={gameOver || loading}
              >
                {loading
                  ? "Checking..."
                  : "Check Guess"}
              </button>

            </form>


            {/* Result Message */}
            {message && (
              <div className={getMessageClass()}>
                {message}
              </div>
            )}


            {/* Guess History */}
            {guesses.length > 0 && (

              <div className="history">

                <h3>
                  Your Guesses
                </h3>

                <div className="guess-list">

                  {guesses.map((item, index) => (

                    <span
                      className="guess-item"
                      key={index}
                    >
                      {item}
                    </span>

                  ))}

                </div>

              </div>

            )}


            {/* Game Complete */}
            {gameOver && (

              <div className="game-complete">

                <div className="success-icon">
                  ✓
                </div>

                <h2>
                  Congratulations!
                </h2>

                <p>
                  You found the correct number in{" "}
                  <strong>
                    {attempts}
                  </strong>{" "}
                  attempts.
                </p>

                <button
                  className="secondary-btn"
                  onClick={startGame}
                >
                  Play Again
                </button>

              </div>

            )}

          </>

        )}


        {/* Footer */}
        <div className="footer">
          Keep guessing until you find it!
        </div>

      </div>

    </div>
  );
}

export default App;