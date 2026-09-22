import React, { useState } from "react";

function App() {
  const [number, setNumber] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Check whether the number is even or odd
  const checkNumber = async () => {
    setError("");
    setResult(null);

    // Check for empty input
    if (number.trim() === "") {
      setError("Please enter a number.");
      return;
    }

    // Allow only integers, including negative numbers
    if (!/^-?\d+$/.test(number.trim())) {
      setError("Please enter a valid integer.");
      return;
    }

    setLoading(true);

    try {
      // Send number directly to Flask backend
      const response = await fetch(
        "http://127.0.0.1:5000/api/check-number",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            number: number.trim(),
          }),
        }
      );

      const data = await response.json();

      // Handle backend errors
      if (!response.ok) {
        setError(data.message || "Something went wrong.");
        return;
      }

      // Display backend result
      setResult(data);
    } catch (error) {
      setError(
        "Unable to connect to the backend. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // Clear input and result
  const clearResult = () => {
    setNumber("");
    setResult(null);
    setError("");
  };

  // Allow Enter key to check the number
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      checkNumber();
    }
  };

  return (
    <div className="app">
      <div className="card">

        {/* Application Icon */}
        <div className="icon">
          🟰
        </div>

        {/* Application Title */}
        <h1>Even or Odd</h1>

        <p className="subtitle">
          Number Checker
        </p>

        {/* Number Input */}
        <div className="input-section">

          <label htmlFor="number">
            Enter an integer
          </label>

          <input
            id="number"
            type="text"
            value={number}
            onChange={(event) => {
              setNumber(event.target.value);
              setError("");
              setResult(null);
            }}
            onKeyDown={handleKeyDown}
            placeholder="e.g. 24 or -7"
          />

        </div>

        {/* Buttons */}
        <div className="buttons">

          <button
            className="check-btn"
            onClick={checkNumber}
            disabled={loading}
          >
            {loading ? "Checking..." : "Check Number"}
          </button>

          <button
            className="clear-btn"
            onClick={clearResult}
          >
            Clear
          </button>

        </div>

        {/* Error Message */}
        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {/* Result */}
        {result && (
          <div
            className={`result ${
              result.result.toLowerCase()
            }`}
          >

            {/* Result Icon */}
            <div className="result-icon">
              {result.result === "Even" ? "✓" : "!"}
            </div>

            {/* Result Details */}
            <div>

              <h2>
                {result.result} Number
              </h2>

              <p>
                {result.message}
              </p>

            </div>

          </div>
        )}

        {/* Quick Examples */}
        <div className="examples">

          <span>Try:</span>

          <button
            onClick={() => {
              setNumber("24");
              setResult(null);
              setError("");
            }}
          >
            24
          </button>

          <button
            onClick={() => {
              setNumber("15");
              setResult(null);
              setError("");
            }}
          >
            15
          </button>

          <button
            onClick={() => {
              setNumber("-8");
              setResult(null);
              setError("");
            }}
          >
            -8
          </button>

          <button
            onClick={() => {
              setNumber("-7");
              setResult(null);
              setError("");
            }}
          >
            -7
          </button>

          <button
            onClick={() => {
              setNumber("0");
              setResult(null);
              setError("");
            }}
          >
            0
          </button>

        </div>

      </div>
    </div>
  );
}

export default App;