import streamlit as st
from datetime import datetime, date

from database import (
    create_database,
    add_goal,
    get_goals,
    add_note,
    get_notes,
    add_quiz_score,
    get_quiz_scores,
    add_study_session,
    get_study_sessions,
    get_dashboard_stats,
    update_goal_status
)

from ai_planner import generate_study_plan

create_database()

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Study Assistant",
    page_icon="≡ƒÄô",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "scores" not in st.session_state:
    st.session_state.scores = []

if "notes" not in st.session_state:
    st.session_state.notes = []

if "goals" not in st.session_state:
    st.session_state.goals = []

if "study_sessions" not in st.session_state:
    st.session_state.study_sessions = 0

if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = 0

if "plan" not in st.session_state:
    st.session_state.plan = []

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("≡ƒÄô Study Assistant")

page = st.sidebar.radio(
    "Navigation",
    [
        "≡ƒÅá Dashboard",
        "≡ƒôÜ Study Planner",
        "≡ƒô¥ Quiz",
        "≡ƒôè Progress",
        "≡ƒÄ» Goals",
        "ΓÅ▒∩╕Å Study Timer",
        "≡ƒùÆ∩╕Å Notes"
    ],
    key="page"
)

st.sidebar.divider()

st.sidebar.info(
    "Study smarter. Practice regularly. Track your progress. ≡ƒÜÇ"
)

# =========================================================
# DASHBOARD
# =========================================================
if page == "≡ƒÅá Dashboard":

    st.title("≡ƒÄô Student Study Assistant")

    st.subheader("Welcome back! ≡ƒæï")

    st.write(
        "Your personal study space to plan, practice and track your learning."
    )

    # Get real data from database
    completed_goals, quizzes, average_score, total_minutes = (
        get_dashboard_stats()
    )

    st.divider()

    # Dashboard statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "≡ƒÄ» Goals Completed",
            completed_goals
        )

    with col2:

        st.metric(
            "≡ƒô¥ Quizzes Taken",
            quizzes
        )

    with col3:

        st.metric(
            "≡ƒôê Average Score",
            f"{average_score:.0f}%"
        )

    with col4:

        st.metric(
            "ΓÅ▒∩╕Å Study Time",
            f"{total_minutes} min"
        )

    st.divider()

    # Quick start
    st.subheader("≡ƒÜÇ Quick Start")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "≡ƒôÜ Study Planner",
            use_container_width=True
        ):
            st.session_state.quick_action = "planner"

        st.caption("Create a personalized study plan.")

    with col2:
        if st.button(
            "≡ƒôè Study Summary",
            use_container_width=True
        ):
            st.session_state.quick_action = "summary"

        st.caption("View your study progress.")

    with col3:
        if st.button(
            "≡ƒÆí Study Tip",
            use_container_width=True
        ):
            st.session_state.quick_action = "tip"

        st.caption("Get a useful study tip.")

    st.divider()

    if st.session_state.get("quick_action") == "planner":
        st.subheader("≡ƒôÜ Study Planner")
        st.info(
            "Go to **≡ƒôÜ Study Planner** from the sidebar "
            "to create your AI-powered study plan."
        )

    elif st.session_state.get("quick_action") == "summary":
        st.subheader("≡ƒôè Study Summary")

        if total_minutes == 0:
            st.info(
                "Start your first study session "
                "to see your progress here! ≡ƒÜÇ"
            )
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60

            st.success(
                f"You have studied for **{hours} hours "
                f"and {minutes} minutes** in total. ≡ƒÄë"
            )

    elif st.session_state.get("quick_action") == "tip":
        st.subheader("≡ƒÆí Study Tip")

        st.success(
            "Don't just read the solution. "
            "Close it and try to write the code yourself. ≡ƒÆ╗"
        )

# =========================================================
# STUDY PLANNER
# =========================================================

elif page == "≡ƒôÜ Study Planner":

    st.title("≡ƒñû AI Study Planner")

    st.write(
        "Create a personalized study plan using AI."
    )

    subject = st.text_input(
        "≡ƒôÜ What do you want to study?",
        placeholder="Example: Python, DSA, DBMS"
    )

    exam_date = st.date_input(
        "≡ƒôà When is your exam?"
    )

    difficulty = st.selectbox(
        "≡ƒÄ» Difficulty level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    minutes = st.slider(
        "ΓÅ▒∩╕Å Study time per day",
        15,
        180,
        45
    )

    if st.button("Γ£¿ Generate AI Study Plan"):

        if not subject.strip():

            st.warning(
                "Please enter a subject first."
            )

        else:

            with st.spinner(
                "≡ƒñû AI is creating your study plan..."
            ):

                try:

                    plan = generate_study_plan(
                        subject,
                        exam_date,
                        minutes,
                        difficulty
                    )

                    st.session_state.ai_plan = plan

                except Exception:
                   st.error(
        "Unable to generate the study plan. "
        "Please check your API key and try again."
    )

    if "ai_plan" in st.session_state:

        st.divider()

        st.subheader("≡ƒùô∩╕Å Your AI Study Plan")

        st.markdown(
            st.session_state.ai_plan
        )


# =========================================================
# QUIZ
# =========================================================
elif page == "≡ƒô¥ Quiz":

    st.title("≡ƒô¥ Practice Quiz")

    st.write(
        "Test your basic programming knowledge."
    )

    questions = [
        {
            "question": "What is a variable?",
            "options": [
                "A place to store data",
                "A computer",
                "An operating system",
                "A network"
            ],
            "answer": "A place to store data"
        },

        {
            "question": "Which keyword is used for a condition in Python?",
            "options": [
                "if",
                "loop",
                "check",
                "condition"
            ],
            "answer": "if"
        },

        {
            "question": "Which data structure follows LIFO?",
            "options": [
                "Queue",
                "Stack",
                "Array",
                "Graph"
            ],
            "answer": "Stack"
        },

        {
            "question": "Which language uses indentation to define blocks?",
            "options": [
                "Python",
                "C",
                "Java",
                "SQL"
            ],
            "answer": "Python"
        },

        {
            "question": "Which of these can store multiple values?",
            "options": [
                "List",
                "Integer",
                "Boolean",
                "Character"
            ],
            "answer": "List"
        }
    ]

    answers = []

    for i, q in enumerate(questions):

        st.subheader(
            f"Question {i + 1}"
        )

        answer = st.radio(
            q["question"],
            q["options"],
            key=f"quiz_question_{i}"
        )

        answers.append(answer)

    if st.button("≡ƒÄ» Submit Quiz"):

        score = 0

        for i in range(len(questions)):

            if answers[i] == questions[i]["answer"]:
                score += 1

        percentage = (
            score / len(questions)
        ) * 100

        # Save score to SQLite
        quiz_date = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        add_quiz_score(
            percentage,
            quiz_date
        )

        st.divider()

        st.subheader(
            f"≡ƒÄë Your Score: {score}/{len(questions)}"
        )

        st.progress(
            percentage / 100
        )

        st.write(
            f"You scored **{percentage:.0f}%**"
        )

        if percentage >= 80:

            st.success(
                "Excellent work! ≡ƒîƒ"
            )

        elif percentage >= 50:

            st.warning(
                "Good effort! Keep practicing. ≡ƒÆ¬"
            )

        else:

            st.error(
                "Revise the concepts and try again. ≡ƒôÜ"
            )

# =========================================================
# PROGRESS
# =========================================================
elif page == "≡ƒôè Progress":

    st.title("≡ƒôè My Progress")

    st.write(
        "Track your learning performance with visual analytics."
    )

    # Get data from database
    scores = get_quiz_scores()
    sessions = get_study_sessions()
    goals = get_goals()

    # =====================================================
    # SUMMARY
    # =====================================================

    total_quizzes = len(scores)

    if total_quizzes > 0:

        average_score = sum(
            score[1] for score in scores
        ) / total_quizzes

        best_score = max(
            score[1] for score in scores
        )

    else:

        average_score = 0
        best_score = 0

    total_minutes = sum(
        session[1] for session in sessions
    )

    completed_goals = sum(
        1 for goal in goals
        if goal[3] == 1
    )

    total_goals = len(goals)

    # =====================================================
    # TOP STATISTICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "≡ƒô¥ Quizzes",
            total_quizzes
        )

    with col2:
        st.metric(
            "≡ƒôê Average Score",
            f"{average_score:.0f}%"
        )

    with col3:
        st.metric(
            "≡ƒÅå Best Score",
            f"{best_score:.0f}%"
        )

    with col4:
        st.metric(
            "ΓÅ▒∩╕Å Study Time",
            f"{total_minutes} min"
        )

    st.divider()

    # =====================================================
    # QUIZ PERFORMANCE CHART
    # =====================================================

    st.subheader("≡ƒôê Quiz Performance")

    if scores:

        quiz_chart_data = {
            f"Quiz {i + 1}": score[1]
            for i, score in enumerate(reversed(scores))
        }

        st.bar_chart(
            quiz_chart_data
        )

    else:

        st.info(
            "Take some quizzes to see your performance chart."
        )

    st.divider()

    # =====================================================
    # STUDY TIME CHART
    # =====================================================

    st.subheader("ΓÅ▒∩╕Å Study Time")

    if sessions:

        study_chart_data = {
            f"Session {i + 1}": session[1]
            for i, session in enumerate(reversed(sessions))
        }

        st.bar_chart(
            study_chart_data
        )

    else:

        st.info(
            "Complete some study sessions to see your study-time chart."
        )

    st.divider()

    # =====================================================
    # GOAL PROGRESS
    # =====================================================

    st.subheader("≡ƒÄ» Goal Completion")

    if total_goals == 0:

        st.info(
            "Add goals to start tracking your completion."
        )

    else:

        goal_percentage = (
            completed_goals / total_goals
        )

        st.progress(
            goal_percentage
        )

        st.write(
            f"**{completed_goals} / {total_goals} goals completed**"
        )

        st.write(
            f"Completion rate: **{goal_percentage * 100:.0f}%**"
        )

    st.divider()

    # =====================================================
    # QUIZ HISTORY
    # =====================================================

    st.subheader("≡ƒô¥ Quiz History")

    if scores:

        for i, score in enumerate(scores):

            score_value = score[1]
            quiz_date = score[2]

            st.write(
                f"**Quiz {len(scores) - i}: "
                f"{score_value:.0f}%**"
            )

            st.progress(
                score_value / 100
            )

            st.caption(
                f"≡ƒôà {quiz_date}"
            )

    else:

        st.info("No quiz history yet.")

    st.divider()

    # =====================================================
    # STUDY HISTORY
    # =====================================================

    st.subheader("≡ƒôÜ Study History")

    if sessions:

        for session in sessions:

            session_minutes = session[1]
            session_date = session[2]

            st.write(
                f"≡ƒôÜ **{session_minutes} minutes**"
            )

            st.caption(
                f"≡ƒôà {session_date}"
            )

    else:

        st.info("No study sessions yet.")




# =========================================================
# STUDY TIMER
# =========================================================

elif page == "ΓÅ▒∩╕Å Study Timer":

    st.title("ΓÅ▒∩╕Å Study Timer")

    st.write(
        "Record your study sessions and build a consistent habit. ≡ƒôÜ"
    )

    minutes = st.number_input(
        "ΓÅ▒∩╕Å Study duration (minutes)",
        min_value=1,
        max_value=180,
        value=25
    )

    st.info(
        f"Your study session: {minutes} minutes"
    )

    if st.button("Γû╢∩╕Å Start Study Session"):

        session_date = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        add_study_session(
            minutes,
            session_date
        )

        st.success(
            f"Study session of {minutes} minutes recorded! ≡ƒÄë"
        )

    st.divider()

    st.subheader("≡ƒôÜ Study History")

    sessions = get_study_sessions()

    if not sessions:

        st.info(
            "No study sessions recorded yet."
        )

    else:

        total_minutes = sum(
            session[1] for session in sessions
        )

        st.metric(
            "ΓÅ▒∩╕Å Total Study Time",
            f"{total_minutes} minutes"
        )

        st.divider()

        for session in sessions:

            session_id = session[0]
            session_minutes = session[1]
            session_date = session[2]

            st.write(
                f"≡ƒôÜ **{session_minutes} minutes**"
            )

            st.caption(
                f"≡ƒòÉ {session_date}"
            )

            st.divider()



# =========================================================
# NOTES
# =========================================================

elif page == "≡ƒùÆ∩╕Å Notes":

    st.title("≡ƒùÆ∩╕Å My Notes")

    st.write(
        "Create and save your study notes."
    )

    note_title = st.text_input(
        "≡ƒôî Note title",
        placeholder="Example: Python Loops"
    )

    note_content = st.text_area(
        "≡ƒô¥ Write your notes",
        height=200,
        placeholder="Write your important concepts here..."
    )

    if st.button("≡ƒÆ╛ Save Note"):

        if note_title and note_content:

            created_at = datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )

            add_note(
                note_title,
                note_content,
                created_at
            )

            st.success(
                "Note saved successfully! ≡ƒÄë"
            )

        else:

            st.warning(
                "Please enter both title and content."
            )

    st.divider()

    st.subheader("≡ƒôÜ Saved Notes")

    notes = get_notes()

    if not notes:

        st.info(
            "No notes saved yet."
        )

    else:

        for note in notes:

            note_id = note[0]
            title = note[1]
            content = note[2]
            created_at = note[3]

            with st.expander(
                f"≡ƒôî {title}"
            ):

                st.write(content)

                st.caption(
                    f"Created: {created_at}"
                )
