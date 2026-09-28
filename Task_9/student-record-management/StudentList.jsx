function StudentList({
    students,
    onDelete,
    onSort,
    isSearching,
    sortOrder
}) {


    const getPerformance = (marks) => {

        if (marks >= 75) {

            return (
                <span className="badge good">
                    Good
                </span>
            );

        }

        if (marks >= 50) {

            return (
                <span className="badge average">
                    Average
                </span>
            );

        }

        return (
            <span className="badge low">
                Needs Improvement
            </span>
        );
    };


    return (

        <section className="records-section">

            <div className="records-header">

                <div>

                    <p className="section-label">
                        STUDENT RECORDS
                    </p>

                    <h2>
                        {isSearching
                            ? "Search Results"
                            : "All Students"}
                    </h2>

                </div>


                {!isSearching && (

                    <select
                        value={sortOrder}
                        onChange={(event) =>
                            onSort(
                                event.target.value
                            )
                        }
                    >

                        <option value="default">
                            Default Order
                        </option>

                        <option value="desc">
                            Highest → Lowest
                        </option>

                        <option value="asc">
                            Lowest → Highest
                        </option>

                    </select>

                )}

            </div>


            {students.length === 0 ? (

                <div className="empty-state">

                    <div className="empty-icon">
                        📚
                    </div>

                    <h3>
                        {isSearching
                            ? "No matching students found"
                            : "No student records yet"}
                    </h3>

                    <p>
                        {isSearching
                            ? "Try another student name."
                            : "Add your first student to get started."}
                    </p>

                </div>

            ) : (

                <div className="table-container">

                    <table>

                        <thead>

                            <tr>

                                <th>
                                    #
                                </th>

                                <th>
                                    Student Name
                                </th>

                                <th>
                                    Marks
                                </th>

                                <th>
                                    Performance
                                </th>

                                <th>
                                    Action
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {students.map(
                                (student, index) => (

                                    <tr
                                        key={
                                            student.id
                                        }
                                    >

                                        <td>
                                            {index + 1}
                                        </td>


                                        <td className="student-name">
                                            {student.name}
                                        </td>


                                        <td>

                                            <strong>
                                                {
                                                    student.marks
                                                }
                                            </strong>

                                            <span>
                                                /100
                                            </span>

                                        </td>


                                        <td>
                                            {getPerformance(
                                                Number(
                                                    student.marks
                                                )
                                            )}
                                        </td>


                                        <td>

                                            <button
                                                className="delete-button"
                                                onClick={() =>
                                                    onDelete(
                                                        student.id
                                                    )
                                                }
                                            >
                                                Delete
                                            </button>

                                        </td>

                                    </tr>

                                )
                            )}

                        </tbody>

                    </table>

                </div>

            )}

        </section>
    );
}


export default StudentList;