import { useEffect, useState } from "react";

import StudentForm from "./StudentForm";

import StudentList from "./StudentList";

import SearchStudent from "./SearchStudent";

import Statistics from "./Statistics";

import "./style.css";


function App() {

    const [students, setStudents] = useState([]);

    const [statistics, setStatistics] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    const [isSearching, setIsSearching] =
        useState(false);

    const [sortOrder, setSortOrder] =
        useState("default");


    // ==========================================
    // Load Students
    // ==========================================

    const loadStudents = async () => {

        try {

            setLoading(true);

            const response = await fetch(
                "/api/students"
            );


            if (!response.ok) {

                throw new Error(
                    "Unable to connect to backend."
                );
            }


            const data =
                await response.json();

            setStudents(data);

            setError("");

        } catch (error) {

            setError(
                "Backend connection failed. "
                + "Make sure Flask is running."
            );

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // Load Statistics
    // ==========================================

    const loadStatistics = async () => {

        try {

            const response = await fetch(
                "/api/students/statistics"
            );


            const data =
                await response.json();

            setStatistics(data);

        } catch (error) {

            console.error(error);

        }
    };


    // ==========================================
    // Refresh Everything
    // ==========================================

    const refreshData = async () => {

        await loadStudents();

        await loadStatistics();

    };


    // ==========================================
    // Initial Load
    // ==========================================

    useEffect(() => {

        refreshData();

    }, []);


    // ==========================================
    // Search
    // ==========================================

    const handleSearch = async (name) => {

        if (!name) {

            setIsSearching(false);

            await loadStudents();

            return;
        }


        try {

            setLoading(true);

            const response = await fetch(
                `/api/students/search?name=${encodeURIComponent(name)}`
            );


            const data =
                await response.json();

            setStudents(data);

            setIsSearching(true);

            setSortOrder("default");

        } catch (error) {

            setError(
                "Unable to search students."
            );

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // Sort
    // ==========================================

    const handleSort = async (order) => {

        setSortOrder(order);

        setIsSearching(false);


        if (order === "default") {

            await loadStudents();

            return;
        }


        try {

            setLoading(true);

            const response = await fetch(
                `/api/students/sort?order=${order}`
            );


            const data =
                await response.json();

            setStudents(data);

        } catch (error) {

            setError(
                "Unable to sort students."
            );

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // Delete
    // ==========================================

    const handleDelete = async (id) => {

        const confirmDelete =
            window.confirm(
                "Are you sure you want to delete this student?"
            );


        if (!confirmDelete) {
            return;
        }


        try {

            const response = await fetch(
                `/api/students/${id}`,
                {
                    method: "DELETE"
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Unable to delete student."
                );
            }


            await refreshData();


            setIsSearching(false);

            setSortOrder("default");

        } catch (error) {

            setError(error.message);

        }
    };


    // ==========================================
    // Student Added
    // ==========================================

    const handleStudentAdded = async () => {

        await refreshData();

        setIsSearching(false);

        setSortOrder("default");

    };


    return (

        <div className="app-container">

            {/* Header */}

            <header className="app-header">

                <div>

                    <p className="header-label">
                        PYTHON + REACT
                    </p>

                    <h1>
                        Student Records
                        <span>
                            Management
                        </span>
                    </h1>

                    <p className="header-description">
                        Manage student records,
                        search performance,
                        and analyze marks.
                    </p>

                </div>

            </header>


            {/* Backend Error */}

            {error && (

                <div className="global-error">

                    ⚠️ {error}

                </div>

            )}


            {/* Add Student */}

            <StudentForm
                onStudentAdded={
                    handleStudentAdded
                }
            />


            {/* Search */}

            <SearchStudent
                onSearch={handleSearch}
            />


            {/* Statistics */}

            <Statistics
                statistics={statistics}
            />


            {/* Refresh Button */}

            <div className="refresh-container">

                <button
                    className="secondary-button"
                    onClick={refreshData}
                >
                    ↻ Refresh Records
                </button>

            </div>


            {/* Student List */}

            {loading ? (

                <div className="loading">
                    Loading student records...
                </div>

            ) : (

                <StudentList

                    students={students}

                    onDelete={handleDelete}

                    onSort={handleSort}

                    isSearching={isSearching}

                    sortOrder={sortOrder}

                />

            )}


            {/* Footer */}

            <footer>

                <p>
                    Student Records Management System
                </p>

                <span>
                    React • Flask • Python REST API
                </span>

            </footer>

        </div>
    );
}


export default App;