import { useState } from "react";


function StudentForm({ onStudentAdded }) {

    const [name, setName] = useState("");

    const [marks, setMarks] = useState("");

    const [error, setError] = useState("");

    const [success, setSuccess] = useState("");


    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");
        setSuccess("");


        if (!name.trim()) {

            setError(
                "Please enter the student name."
            );

            return;
        }


        if (
            marks === "" ||
            Number(marks) < 0 ||
            Number(marks) > 100
        ) {

            setError(
                "Marks must be between 0 and 100."
            );

            return;
        }


        try {

            const response = await fetch(
                "/api/students",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name.trim(),
                        marks: Number(marks)
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Failed to add student."
                );
            }


            setSuccess(
                "Student added successfully!"
            );

            setName("");

            setMarks("");

            onStudentAdded();

        } catch (error) {

            setError(error.message);

        }

    };


    return (

        <section className="form-section">

            <div className="section-heading">

                <p className="section-label">
                    ADD RECORD
                </p>

                <h2>
                    Add New Student
                </h2>

            </div>


            <form
                onSubmit={handleSubmit}
                className="student-form"
            >

                <div className="form-group">

                    <label>
                        Student Name
                    </label>

                    <input
                        type="text"
                        placeholder="Enter student name"
                        value={name}
                        onChange={(event) =>
                            setName(
                                event.target.value
                            )
                        }
                    />

                </div>


                <div className="form-group">

                    <label>
                        Marks
                    </label>

                    <input
                        type="number"
                        min="0"
                        max="100"
                        step="0.01"
                        placeholder="Enter marks (0-100)"
                        value={marks}
                        onChange={(event) =>
                            setMarks(
                                event.target.value
                            )
                        }
                    />

                </div>


                <button
                    type="submit"
                    className="primary-button"
                >
                    + Add Student
                </button>

            </form>


            {error && (

                <div className="message error">
                    {error}
                </div>

            )}


            {success && (

                <div className="message success">
                    {success}
                </div>

            )}

        </section>
    );
}


export default StudentForm;