import React, { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:5000/api/tasks";


function App() {

    const [tasks, setTasks] = useState([]);

    const [newTask, setNewTask] = useState("");

    const [editingId, setEditingId] = useState(null);

    const [editingText, setEditingText] = useState("");

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [showCelebration, setShowCelebration] = useState(false);


    // =====================================================
    // LOAD TASKS
    // =====================================================

    const loadTasks = async () => {

        try {

            setError("");

            const response = await fetch(API_URL);

            if (!response.ok) {
                throw new Error("Unable to load tasks.");
            }

            const data = await response.json();

            setTasks(data);

        } catch (err) {

            setError(
                "Cannot connect to the Python backend. "
                + "Please make sure app.py is running."
            );

        } finally {

            setLoading(false);

        }
    };


    useEffect(() => {

        loadTasks();

    }, []);


    // =====================================================
    // ADD TASK
    // =====================================================

    const addTask = async () => {

        const title = newTask.trim();

        if (!title) {
            return;
        }

        try {

            setError("");

            const response = await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        title: title
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to add task."
                );
            }

            setTasks(previous => [
                ...previous,
                data.task
            ]);

            setNewTask("");

        } catch (err) {

            setError(err.message);

        }
    };


    // =====================================================
    // TOGGLE COMPLETION
    // =====================================================

    const toggleTask = async (task) => {

        try {

            setError("");

            const response = await fetch(
                `${API_URL}/${task.id}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        completed: !task.completed
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to update task."
                );
            }

            setTasks(previous =>
                previous.map(item =>
                    item.id === task.id
                        ? data.task
                        : item
                )
            );

        } catch (err) {

            setError(err.message);

        }
    };


    // =====================================================
    // START EDIT
    // =====================================================

    const startEdit = (task) => {

        setEditingId(task.id);

        setEditingText(task.title);

    };


    // =====================================================
    // SAVE EDIT
    // =====================================================

    const saveEdit = async (taskId) => {

        const title = editingText.trim();

        if (!title) {
            return;
        }

        try {

            setError("");

            const response = await fetch(
                `${API_URL}/${taskId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        title: title
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to update task."
                );
            }

            setTasks(previous =>
                previous.map(task =>
                    task.id === taskId
                        ? data.task
                        : task
                )
            );

            setEditingId(null);

            setEditingText("");

        } catch (err) {

            setError(err.message);

        }
    };


    // =====================================================
    // DELETE TASK
    // =====================================================

    const deleteTask = async (taskId) => {

        try {

            setError("");

            const response = await fetch(
                `${API_URL}/${taskId}`,
                {
                    method: "DELETE"
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to delete task."
                );
            }

            setTasks(previous =>
                previous.filter(
                    task => task.id !== taskId
                )
            );

        } catch (err) {

            setError(err.message);

        }
    };


    // =====================================================
    // KEYBOARD
    // =====================================================

    const handleAddKey = (event) => {

        if (event.key === "Enter") {
            addTask();
        }

    };


    const handleEditKey = (event, taskId) => {

        if (event.key === "Enter") {
            saveEdit(taskId);
        }

        if (event.key === "Escape") {

            setEditingId(null);

            setEditingText("");

        }

    };


    // =====================================================
    // STATISTICS
    // =====================================================

    const totalTasks = tasks.length;

    const completedTasks = tasks.filter(
        task => task.completed
    ).length;

    const pendingTasks =
        totalTasks - completedTasks;

    const progress =
        totalTasks === 0
            ? 0
            : Math.round(
                (completedTasks / totalTasks) * 100
            );


    // =====================================================
    // CELEBRATION
    // =====================================================

    useEffect(() => {

        if (
            totalTasks > 0 &&
            completedTasks === totalTasks
        ) {

            setShowCelebration(true);

            const timer = setTimeout(() => {

                setShowCelebration(false);

            }, 4500);

            return () => clearTimeout(timer);

        }

    }, [completedTasks, totalTasks]);


    // =====================================================
    // RENDER
    // =====================================================

    return (

        <div className="app">

            {showCelebration && (

                <div className="celebration">

                    {Array.from({
                        length: 45
                    }).map((_, index) => (

                        <span
                            key={index}
                            className="confetti"
                            style={{
                                left:
                                    `${Math.random() * 100}%`,
                                animationDelay:
                                    `${Math.random() * 0.7}s`
                            }}
                        />

                    ))}

                    <div className="success-card">

                        <div className="success-icon">
                            ✓
                        </div>

                        <h2>
                            All Tasks Completed!
                        </h2>

                        <p>
                            Great work! You successfully
                            completed your entire to-do list.
                        </p>

                    </div>

                </div>

            )}


            {/* HEADER */}

            <header className="header">

                <div className="header-content">

                    <div>

                        <p className="eyebrow">
                            PRODUCTIVITY PLANNER
                        </p>

                        <h1>
                            My To-Do List
                        </h1>

                        <p className="subtitle">
                            Organize your tasks.
                            Track your progress.
                            Achieve your goals.
                        </p>

                    </div>


                    <div className="progress-circle">

                        <strong>
                            {progress}%
                        </strong>

                        <span>
                            Complete
                        </span>

                    </div>

                </div>

            </header>


            <main className="container">


                {/* ERROR */}

                {error && (

                    <div className="error-box">

                        <span>
                            {error}
                        </span>

                        <button
                            onClick={() => {
                                setError("");
                                loadTasks();
                            }}
                        >
                            Retry
                        </button>

                    </div>

                )}


                {/* ADD TASK */}

                <section className="add-section">

                    <input
                        type="text"
                        value={newTask}
                        placeholder="Enter a new task..."
                        onChange={event =>
                            setNewTask(
                                event.target.value
                            )
                        }
                        onKeyDown={handleAddKey}
                    />

                    <button
                        className="add-button"
                        onClick={addTask}
                    >
                        + Add Task
                    </button>

                </section>


                {/* STATISTICS */}

                <section className="stats">

                    <div className="stat-card">

                        <span>
                            Total Tasks
                        </span>

                        <strong>
                            {totalTasks}
                        </strong>

                    </div>


                    <div className="stat-card">

                        <span>
                            Pending
                        </span>

                        <strong>
                            {pendingTasks}
                        </strong>

                    </div>


                    <div className="stat-card completed-stat">

                        <span>
                            Completed
                        </span>

                        <strong>
                            {completedTasks}
                        </strong>

                    </div>

                </section>


                {/* TASK LIST */}

                <section className="tasks-section">

                    <div className="section-title">

                        <div>

                            <h2>
                                My Tasks
                            </h2>

                            <p>
                                Keep your daily work organized.
                            </p>

                        </div>

                        <button
                            className="refresh-button"
                            onClick={loadTasks}
                        >
                            Refresh
                        </button>

                    </div>


                    {loading ? (

                        <div className="empty-state">
                            Loading tasks...
                        </div>

                    ) : tasks.length === 0 ? (

                        <div className="empty-state">

                            <div className="empty-icon">
                                ✓
                            </div>

                            <h3>
                                No tasks yet
                            </h3>

                            <p>
                                Add your first task to get started.
                            </p>

                        </div>

                    ) : (

                        <div className="task-list">

                            {tasks.map(task => (

                                <div
                                    key={task.id}
                                    className={
                                        task.completed
                                            ? "task completed"
                                            : "task"
                                    }
                                >

                                    <button
                                        className={
                                            task.completed
                                                ? "checkbox checked"
                                                : "checkbox"
                                        }
                                        onClick={() =>
                                            toggleTask(task)
                                        }
                                    >
                                        {task.completed
                                            ? "✓"
                                            : ""}
                                    </button>


                                    <div className="task-content">

                                        {editingId === task.id ? (

                                            <input
                                                className="edit-input"
                                                value={editingText}
                                                autoFocus
                                                onChange={event =>
                                                    setEditingText(
                                                        event.target.value
                                                    )
                                                }
                                                onKeyDown={event =>
                                                    handleEditKey(
                                                        event,
                                                        task.id
                                                    )
                                                }
                                            />

                                        ) : (

                                            <span>
                                                {task.title}
                                            </span>

                                        )}

                                        <small>
                                            Task #{task.id}
                                        </small>

                                    </div>


                                    <div className="actions">

                                        {editingId === task.id ? (

                                            <button
                                                className="save"
                                                onClick={() =>
                                                    saveEdit(
                                                        task.id
                                                    )
                                                }
                                            >
                                                Save
                                            </button>

                                        ) : (

                                            <button
                                                className="edit"
                                                onClick={() =>
                                                    startEdit(task)
                                                }
                                            >
                                                Edit
                                            </button>

                                        )}


                                        <button
                                            className="delete"
                                            onClick={() =>
                                                deleteTask(
                                                    task.id
                                                )
                                            }
                                        >
                                            Delete
                                        </button>

                                    </div>

                                </div>

                            ))}

                        </div>

                    )}

                </section>

            </main>


            <footer>

                <p>
                    Python Flask Backend
                    &nbsp;•&nbsp;
                    React Frontend
                    &nbsp;•&nbsp;
                    REST API
                </p>

            </footer>

        </div>
    );
}


export default App;