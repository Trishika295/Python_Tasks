import React, { useState } from "react";

function App() {
  const [text, setText] = useState("");

  const [statistics, setStatistics] = useState({
    characters: 0,
    words: 0,
    sentences: 0,
    spaces: 0
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    if (!text.trim()) {
      setError("Please enter a paragraph before analyzing.");

      setStatistics({
        characters: 0,
        words: 0,
        sentences: 0,
        spaces: 0
      });

      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            text: text
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message);
      }

      setStatistics(data.statistics);

    } catch (error) {
      setError(
        "Unable to connect to Flask. Make sure the Python backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const clearText = () => {
    setText("");
    setError("");

    setStatistics({
      characters: 0,
      words: 0,
      sentences: 0,
      spaces: 0
    });
  };

  return (
    <div className="page-container">

      <header className="header">

        <div className="header-icon">
          Aa
        </div>

        <div>
          <h1>Word & Character Counter</h1>

          <p>
            Analyze your paragraph quickly and accurately
          </p>
        </div>

      </header>


      <main className="main-card">

        <section className="input-section">

          <div className="section-heading">

            <h2>Enter Your Text</h2>

            <span>
              {text.length} characters
            </span>

          </div>


          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Type or paste your paragraph here..."
          />


          {error && (
            <div className="error-message">
              {error}
            </div>
          )}


          <div className="button-container">

            <button
              className="analyze-button"
              onClick={analyzeText}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze Text"}
            </button>

            <button
              className="clear-button"
              onClick={clearText}
            >
              Clear
            </button>

          </div>

        </section>


        <section className="results-section">

          <div className="results-title">

            <h2>Text Statistics</h2>

            <span>Results</span>

          </div>


          <div className="statistics-grid">

            <div className="stat-card">

              <div className="stat-icon">
                Aa
              </div>

              <div>
                <p>Characters</p>

                <h3>
                  {statistics.characters}
                </h3>
              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon">
                W
              </div>

              <div>
                <p>Words</p>

                <h3>
                  {statistics.words}
                </h3>
              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon">
                S
              </div>

              <div>
                <p>Sentences</p>

                <h3>
                  {statistics.sentences}
                </h3>
              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon">
                ␠
              </div>

              <div>
                <p>Spaces</p>

                <h3>
                  {statistics.spaces}
                </h3>
              </div>

            </div>

          </div>

        </section>


        <section className="info-section">

          <div className="info-item">
            <strong>Characters</strong>
            <span>
              Includes letters, numbers, punctuation and spaces.
            </span>
          </div>

          <div className="info-item">
            <strong>Words</strong>
            <span>
              Calculated using Python's split() method.
            </span>
          </div>

          <div className="info-item">
            <strong>Sentences</strong>
            <span>
              Detected using ., ! and ? punctuation.
            </span>
          </div>

          <div className="info-item">
            <strong>Spaces</strong>
            <span>
              Counts normal space characters in the paragraph.
            </span>
          </div>

        </section>

      </main>


      <footer>
        <p>
          Word & Character Counter • Python + Flask + React
        </p>
      </footer>

    </div>
  );
}

export default App;