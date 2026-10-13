import streamlit as st

from quiz_logic import (
    load_questions,
    shuffle_questions,
    calculate_results,
)

st.set_page_config(
    page_title="QuizMaster | Python Quiz",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -------------------- CUSTOM STYLING --------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f5ff 0%, #f4f7fb 100%);
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #4338ca, #7c3aed);
        padding: 2rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(67, 56, 202, 0.15);
    }

    .hero h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.3rem;
    }

    .hero p {
        color: #ede9fe;
        font-size: 1.05rem;
    }

    .metric-card {
        background: white;
        padding: 1.1rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        text-align: center;
        min-height: 110px;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
    }

    .metric-value {
        color: #4338ca;
        font-size: 1.8rem;
        font-weight: 750;
        margin-top: 0.25rem;
    }

    .question-card {
        background: white;
        padding: 1.3rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin: 0.7rem 0;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 2.8rem;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #4338ca;
        border-color: #4338ca;
        color: white;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- SESSION STATE --------------------

def initialize_state():
    defaults = {
        "started": False,
        "questions": [],
        "results": None,
        "quiz_error": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def restart_quiz():
    """Reset quiz state and remove saved answers."""
    for key in list(st.session_state.keys()):
        if key.startswith("answer_"):
            del st.session_state[key]

    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.results = None
    st.session_state.quiz_error = None


initialize_state()


# -------------------- HEADER --------------------

st.markdown(
    """
    <div class="hero">
        <h1>QuizMaster</h1>
        <p>Challenge your Python knowledge, track your score,
        and discover how much you know.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- LOAD QUESTIONS --------------------

if st.session_state.quiz_error:
    st.error(st.session_state.quiz_error)

if not st.session_state.started and st.session_state.results is None:
    st.markdown("### Welcome to the Python Quiz")
    st.write(
        "Test your knowledge with multiple-choice questions "
        "covering Python fundamentals."
    )

    try:
        available_questions = load_questions()
    except ValueError as error:
        available_questions = []
        st.error(f"Unable to load quiz: {error}")

    if available_questions:
        st.markdown("#### Your quiz")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Available Questions</div>
                    <div class="metric-value">
                        {len(available_questions)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-label">Question Format</div>
                    <div class="metric-value">MCQ</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")

        shuffle_choice = st.checkbox(
            "Randomize question order",
            value=True,
        )

        if st.button(
            "Start Quiz →",
            type="primary",
            use_container_width=True,
        ):
            questions = (
                shuffle_questions(available_questions)
                if shuffle_choice
                else list(available_questions)
            )

            st.session_state.questions = questions
            st.session_state.started = True
            st.session_state.results = None
            st.rerun()


# -------------------- QUIZ FORM --------------------

if st.session_state.started and st.session_state.results is None:
    questions = st.session_state.questions
    total = len(questions)

    st.markdown("### Answer the questions")
    st.caption(
        "Choose one option for every question, then submit your answers."
    )

    st.progress(0.0, text=f"0 of {total} questions answered")

    with st.form("quiz_form"):
        for index, question in enumerate(questions):
            st.markdown(
                f'<div class="question-card">'
                f'<strong>Question {index + 1} of {total}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown(f"**{question['question']}**")

            st.radio(
                "Select your answer:",
                options=["A", "B", "C", "D"],
                index=None,
                format_func=lambda key, opts=question["options"]: (
                    f"{key}. {opts[key]}"
                ),
                key=f"answer_{index}",
                label_visibility="collapsed",
            )

            st.divider()

        submitted = st.form_submit_button(
            "Submit Quiz",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        answers = {}
        unanswered = []

        for index in range(total):
            selected = st.session_state.get(f"answer_{index}")

            if selected not in {"A", "B", "C", "D"}:
                unanswered.append(index + 1)
            else:
                answers[index] = selected

        if unanswered:
            st.warning(
                f"Please answer all questions before submitting. "
                f"Unanswered questions: {', '.join(map(str, unanswered))}"
            )
        else:
            st.session_state.results = calculate_results(
                questions,
                answers,
            )
            st.rerun()


# -------------------- RESULTS PAGE --------------------

if st.session_state.results is not None:
    results = st.session_state.results

    st.balloons()
    st.markdown("##Quiz Completed!")
    st.write("Here is your final performance summary.")

    col1, col2, col3 = st.columns(3)

    metrics = [
        (col1, "Correct Answers", results["score"]),
        (col2, "Incorrect Answers", results["wrong"]),
        (col3, "Percentage", f'{results["percentage"]:.1f}%'),
    ]

    for column, label, value in metrics:
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.progress(
        results["percentage"] / 100,
        text=f'Final score: {results["score"]}/{results["total"]}',
    )

    percentage = results["percentage"]

    if percentage >= 90:
        st.success(f'🌟 {results["grade"]}! Outstanding performance.')
    elif percentage >= 60:
        st.success(f'👏 {results["grade"]}! Keep up the good work.')
    else:
        st.info(
            f'📚 {results["grade"]}. Review the answers and try again.'
        )

    st.markdown("### Review your answers")

    for index, detail in enumerate(results["details"], start=1):
        with st.expander(
            f"Question {index}: "
            f"{'✅ Correct' if detail['is_correct'] else '❌ Incorrect'}"
        ):
            st.write(detail["question"])

            selected = detail["selected"]
            correct = detail["correct"]

            if selected == correct:
                st.success(
                    f"Your answer: {selected}. "
                    f"{detail['options'][selected]}"
                )
            else:
                st.error(
                    f"Your answer: {selected}. "
                    f"{detail['options'][selected]}"
                )
                st.success(
                    f"Correct answer: {correct}. "
                    f"{detail['options'][correct]}"
                )

    st.write("")

    if st.button(
        "🔄 Restart Quiz",
        type="primary",
        use_container_width=True,
    ):
        restart_quiz()
        st.rerun()


# -------------------- FOOTER --------------------

st.markdown(
    """
    <div class="footer">
        Task 23 · Python + Streamlit + JSON
        <br>
        Built for learning and practicing Python fundamentals.
    </div>
    """,
    unsafe_allow_html=True,
)
