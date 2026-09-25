import { useState } from "react";
import "./script.css";

function App() {
  const [number, setNumber] = useState("");
  const [limit, setLimit] = useState("");
  const [table, setTable] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedNumber, setGeneratedNumber] = useState(null);

  const generateTable = async (event) => {
    event.preventDefault();

    setError("");
    setTable([]);
    setGeneratedNumber(null);

    // Check empty inputs
    if (number === "" || limit === "") {
      setError("Please enter both the number and the limit.");
      return;
    }

    // Check valid numbers
    if (Number.isNaN(Number(number)) || Number.isNaN(Number(limit))) {
      setError("Please enter valid numbers.");
      return;
    }

    // Check limit
    if (Number(limit) <= 0) {
      setError("Limit must be greater than 0.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/multiplication-table",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            number: number,
            limit: limit,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong.");
        return;
      }

      setTable(data.table);
      setGeneratedNumber(data.number);

    } catch (error) {
      setError(
        "Unable to connect to the Python backend. Please make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const clearForm = () => {
    setNumber("");
    setLimit("");
    setTable([]);
    setError("");
    setGeneratedNumber(null);
  };

  return (
    <div className="app-container">

      <div className="card">

        <div className="header">
          <h1>Multiplication Table Generator</h1>

          <p>
            Enter a number and generate its multiplication table
            up to your specified limit.
          </p>
        </div>

        <form onSubmit={generateTable}>

          <div className="input-group">
            <label htmlFor="number">
              Enter Number
            </label>

            <input
              id="number"
              type="number"
              placeholder="Example: 5"
              value={number}
              onChange={(event) => setNumber(event.target.value)}
            />
          </div>

          <div className="input-group">
            <label htmlFor="limit">
              Enter Limit
            </label>

            <input
              id="limit"
              type="number"
              min="1"
              placeholder="Example: 10"
              value={limit}
              onChange={(event) => setLimit(event.target.value)}
            />
          </div>

          <div className="button-container">

            <button
              type="submit"
              className="generate-button"
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Table"}
            </button>

            <button
              type="button"
              className="clear-button"
              onClick={clearForm}
            >
              Clear
            </button>

          </div>

        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {table.length > 0 && (
          <div className="result-section">

            <h2>
              Multiplication Table of {generatedNumber}
            </h2>

            <p className="limit-text">
              From 1 to {limit}
            </p>

            <div className="table-container">

              <table>

                <thead>
                  <tr>
                    <th>Number</th>
                    <th>×</th>
                    <th>Multiplier</th>
                    <th>=</th>
                    <th>Result</th>
                  </tr>
                </thead>

                <tbody>

                  {table.map((item) => (
                    <tr key={item.multiplier}>

                      <td>{generatedNumber}</td>

                      <td>×</td>

                      <td>{item.multiplier}</td>

                      <td>=</td>

                      <td className="result-value">
                        {item.result}
                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default App;