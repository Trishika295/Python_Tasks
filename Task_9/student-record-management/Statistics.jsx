function Statistics({ statistics }) {

    if (!statistics) {
        return null;
    }


    return (

        <section className="statistics-section">

            <div className="section-heading">

                <p className="section-label">
                    OVERVIEW
                </p>

                <h2>
                    Student Statistics
                </h2>

            </div>


            <div className="statistics">

                <div className="stat-card">

                    <span>
                        Total Students
                    </span>

                    <strong>
                        {statistics.total_students}
                    </strong>

                </div>


                <div className="stat-card">

                    <span>
                        Highest Score
                    </span>

                    <strong>
                        {statistics.highest
                            ? statistics.highest.marks
                            : "—"}
                    </strong>

                    {statistics.highest && (

                        <small>
                            {
                                statistics.highest.name
                            }
                        </small>

                    )}

                </div>


                <div className="stat-card">

                    <span>
                        Lowest Score
                    </span>

                    <strong>
                        {statistics.lowest
                            ? statistics.lowest.marks
                            : "—"}
                    </strong>

                    {statistics.lowest && (

                        <small>
                            {
                                statistics.lowest.name
                            }
                        </small>

                    )}

                </div>


                <div className="stat-card">

                    <span>
                        Average Score
                    </span>

                    <strong>
                        {statistics.total_students > 0
                            ? statistics.average
                            : "—"}
                    </strong>

                </div>

            </div>

        </section>
    );
}


export default Statistics;