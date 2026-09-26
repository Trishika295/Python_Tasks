import React, { useState } from "react";
import "./style.css";

function App() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const validatePassword = async () => {
    if (!password) {
      setResult({
        valid: false,
        requirements: {},
        messages: ["Please enter a password."]
      });

      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/validate-password",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            password: password
          })
        }
      );

      const data = await response.json();

      setResult(data);

    } catch (error) {

      setResult({
        valid: false,
        requirements: {},
        messages: [
          "Unable to connect to the backend. Please make sure Flask is running."
        ]
      });

    } finally {
      setLoading(false);
    }
  };


  const clearPassword = () => {
    setPassword("");
    setResult(null);
  };


  const getRequirementClass = (condition) => {

    if (condition === true) {
      return "requirement passed";
    }

    if (condition === false) {
      return "requirement failed";
    }

    return "requirement";
  };


  return (
    <div className="app-container">

      <div className="validator-card">

        {/* Header */}
        <div className="header">

          <h1>
            Simple Password Validator
          </h1>

          <p>
            Check whether your password satisfies the required
            security requirements.
          </p>

        </div>


        {/* Password Input */}
        <div className="input-section">

          <label htmlFor="password">
            Enter Password
          </label>

          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) => {
              setPassword(event.target.value);
              setResult(null);
            }}
          />

        </div>


        {/* Requirements */}
        <div className="requirements">

          <h2>
            Password Requirements
          </h2>


          <div
            className={getRequirementClass(
              result?.requirements?.minimum_length
            )}
          >
            <span>
              {result?.requirements?.minimum_length
                ? "✓"
                : "○"}
            </span>

            Minimum 8 characters
          </div>


          <div
            className={getRequirementClass(
              result?.requirements?.uppercase
            )}
          >
            <span>
              {result?.requirements?.uppercase
                ? "✓"
                : "○"}
            </span>

            At least one uppercase letter
          </div>


          <div
            className={getRequirementClass(
              result?.requirements?.lowercase
            )}
          >
            <span>
              {result?.requirements?.lowercase
                ? "✓"
                : "○"}
            </span>

            At least one lowercase letter
          </div>


          <div
            className={getRequirementClass(
              result?.requirements?.number
            )}
          >
            <span>
              {result?.requirements?.number
                ? "✓"
                : "○"}
            </span>

            At least one number
          </div>


          <div
            className={getRequirementClass(
              result?.requirements?.special_character
            )}
          >
            <span>
              {result?.requirements?.special_character
                ? "✓"
                : "○"}
            </span>

            At least one special character
          </div>

        </div>


        {/* Buttons */}
        <div className="button-section">

          <button
            className="validate-button"
            onClick={validatePassword}
            disabled={loading}
          >
            {loading
              ? "Checking..."
              : "Validate Password"}
          </button>


          <button
            className="clear-button"
            onClick={clearPassword}
          >
            Clear
          </button>

        </div>


        {/* Result */}
        {result && (

          <div
            className={
              result.valid
                ? "result-box success"
                : "result-box error"
            }
          >

            <h2>

              {result.valid
                ? "✓ Password is Valid"
                : "✕ Password is Invalid"}

            </h2>


            {result.valid ? (

              <p>
                Your password satisfies all the required
                validation rules.
              </p>

            ) : (

              <div className="error-list">

                <p>
                  Please fix the following:
                </p>

                <ul>

                  {result.messages.map(
                    (message, index) => (
                      <li key={index}>
                        {message}
                      </li>
                    )
                  )}

                </ul>

              </div>

            )}

          </div>

        )}


        {/* Security Message */}
        <div className="security-note">

           Your password is only used for validation
          and is not stored.

        </div>

      </div>

    </div>
  );
}

export default App;