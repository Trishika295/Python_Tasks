import { useState } from "react";
import "./script.css";

const subjects = [
  "Mathematics",
  "Science",
  "English",
  "Computer Science",
  "Social Science"
];

function App() {
  const [studentName, setStudentName] = useState("");

  const [marks, setMarks] = useState({
    Mathematics: "",
    Science: "",
    English: "",
    "Computer Science": "",
    "Social Science": ""
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleMarkChange = (subject, value) => {
    setMarks((previousMarks) => ({
      ...previousMarks,
      [subject]: value
    }));

    setError("");
  };

  const calculateGrade = async (event) => {
    event.preventDefault();

    setError("");
    setResult(null);

    if (!studentName.trim()) {
      setError("Please enter the student's name.");
      return;
    }

    for (const subject of subjects) {
      const value = marks[subject];

      if (value === "") {
        setError(`Please enter marks for ${subject}.`);
        return;
      }

      const numericValue = Number(value);

      if (Number.isNaN(numericValue)) {
        setError(`Please enter a valid mark for ${subject}.`);
        return;
      }

      if (numericValue < 0 || numericValue > 100) {
        setError(`${subject} marks must be between 0 and 100.`);
        return;
      }
    }

    const formattedMarks = {};

    subjects.forEach((subject) => {
      formattedMarks[subject] = Number(marks[subject]);
    });

    try {
      setLoading(true);

      const response = await fetch("/api/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          student_name: studentName.trim(),
          marks: formattedMarks
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "Unable to calculate the result.");
        return;
      }

      setResult(data);
    } catch (connectionError) {
      setError(
        "Backend connection failed. Please start the Flask server using: python app.py"
      );
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setStudentName("");

    setMarks({
      Mathematics: "",
      Science: "",
      English: "",
      "Computer Science": "",
      "Social Science": ""
    });

    setResult(null);
    setError("");
  };

  return (
    <div className="page">
      <div className="container">

        {/* Header */}
        <header className="header">
          <div className="logo">
            <span>SG</span>
          </div>

          <div>
            <p className="eyebrow">ACADEMIC TOOL</p>

            <h1>Student Grade Calculator</h1>

            <p className="subtitle">
              Enter subject marks and instantly calculate the total,
              percentage, and final grade.
            </p>
          </div>
        </header>

        {/* Main Card */}
        <div className="main-card">

          <form onSubmit={calculateGrade}>

            {/* Student Information */}
            <div className="section-heading">
              <div className="section-number">01</div>

              <div>
                <h2>Student Information</h2>
                <p>Enter the student's basic information.</p>
              </div>
            </div>

            <div className="student-input">
              <label htmlFor="studentName">
                Student Name
              </label>

              <input
                id="studentName"
                type="text"
                placeholder="e.g. Alex Johnson"
                value={studentName}
                onChange={(event) => {
                  setStudentName(event.target.value);
                  setError("");
                }}
              />
            </div>

            {/* Subject Marks */}
            <div className="section-heading marks-heading">
              <div className="section-number">02</div>

              <div>
                <h2>Subject Marks</h2>
                <p>Enter marks between 0 and 100 for each subject.</p>
              </div>
            </div>

            <div className="subjects-grid">
              {subjects.map((subject, index) => (
                <div className="subject-card" key={subject}>
                  <div className="subject-top">
                    <span className="subject-index">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <label htmlFor={`subject-${index}`}>
                      {subject}
                    </label>
                  </div>

                  <div className="mark-wrapper">
                    <input
                      id={`subject-${index}`}
                      type="number"
                      min="0"
                      max="100"
                      step="0.01"
                      placeholder="00"
                      value={marks[subject]}
                      onChange={(event) =>
                        handleMarkChange(
                          subject,
                          event.target.value
                        )
                      }
                    />

                    <span>/ 100</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Error */}
            {error && (
              <div className="error-message">
                <span className="error-icon">!</span>

                <div>
                  <strong>Unable to calculate</strong>
                  <p>{error}</p>
                </div>
              </div>
            )}

            {/* Buttons */}
            <div className="action-buttons">
              <button
                type="submit"
                className="calculate-button"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Calculating...
                  </>
                ) : (
                  <>
                    Calculate Grade
                    <span className="arrow">→</span>
                  </>
                )}
              </button>

              <button
                type="button"
                className="reset-button"
                onClick={resetForm}
              >
                Reset
              </button>
            </div>
          </form>

          {/* Result */}
          {result && (
            <div className="result-section">

              <div className="result-header">
                <div>
                  <p className="result-label">FINAL RESULT</p>

                  <h2>{result.student_name}</h2>
                </div>

                <div className="result-status">
                  <span>✓</span>
                  Calculated
                </div>
              </div>

              <div className="result-cards">

                <div className="result-card">
                  <span className="result-card-label">
                    TOTAL MARKS
                  </span>

                  <strong>
                    {result.result.total}
                    <small>
                      /{result.result.maximum_marks}
                    </small>
                  </strong>
                </div>

                <div className="result-card">
                  <span className="result-card-label">
                    PERCENTAGE
                  </span>

                  <strong>
                    {result.result.percentage}
                    <small>%</small>
                  </strong>
                </div>

                <div className="result-card grade-result">
                  <span className="result-card-label">
                    FINAL GRADE
                  </span>

                  <strong>
                    {result.result.grade}
                  </strong>
                </div>

              </div>

              <div className="subject-summary">
                <div className="summary-title">
                  <h3>Subject-wise Performance</h3>
                  <span>5 Subjects</span>
                </div>

                {Object.entries(result.subjects).map(
                  ([subject, mark]) => (
                    <div
                      className="summary-row"
                      key={subject}
                    >
                      <span>{subject}</span>

                      <div className="summary-mark">
                        <div className="progress-track">
                          <div
                            className="progress-bar"
                            style={{
                              width: `${mark}%`
                            }}
                          ></div>
                        </div>

                        <strong>{mark}</strong>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
        </div>

        {/* Grade Criteria */}
        <section className="criteria-section">
          <div className="criteria-header">
            <div>
              <p className="eyebrow">GRADING SYSTEM</p>

              <h2>Grade Criteria</h2>
            </div>

            <p>
              Grades are assigned automatically based on
              the calculated percentage.
            </p>
          </div>

          <div className="criteria-grid">

            <div className="criteria-item">
              <span className="criteria-grade">A+</span>
              <span className="criteria-range">90 – 100%</span>
            </div>

            <div className="criteria-item">
              <span className="criteria-grade">A</span>
              <span className="criteria-range">80 – 89%</span>
            </div>

            <div className="criteria-item">
              <span className="criteria-grade">B</span>
              <span className="criteria-range">70 – 79%</span>
            </div>

            <div className="criteria-item">
              <span className="criteria-grade">C</span>
              <span className="criteria-range">60 – 69%</span>
            </div>

            <div className="criteria-item">
              <span className="criteria-grade">D</span>
              <span className="criteria-range">50 – 59%</span>
            </div>

            <div className="criteria-item">
              <span className="criteria-grade fail">F</span>
              <span className="criteria-range">Below 50%</span>
            </div>

          </div>
        </section>

        <footer>
          <span>Student Grade Calculator</span>
          <span>•</span>
          <span>React + Python Flask</span>
        </footer>

      </div>
    </div>
  );
}

export default App;