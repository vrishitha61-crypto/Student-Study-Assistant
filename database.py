import sqlite3


# Create the database and tables
def create_database():

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    # Goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            deadline TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT
        )
    """)

    # Quiz scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score REAL,
            date TEXT
        )
    """)

    # Study sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            minutes INTEGER,
            date TEXT
        )
    """)

    connection.commit()
    connection.close()


# Add a new goal
def add_goal(goal, deadline):

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO goals (goal, deadline)
        VALUES (?, ?)
        """,
        (goal, str(deadline))
    )

    connection.commit()
    connection.close()


# Get all goals
def get_goals():

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM goals"
    )

    goals = cursor.fetchall()

    connection.close()

    return goals

# Add a note
def add_note(title, content, created_at):

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notes (title, content, created_at)
        VALUES (?, ?, ?)
        """,
        (title, content, created_at)
    )

    connection.commit()
    connection.close()


# Get all notes
def get_notes():

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    )

    notes = cursor.fetchall()

    connection.close()

    return notes

# Save quiz score
def add_quiz_score(score, quiz_date):

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_scores (score, date)
        VALUES (?, ?)
        """,
        (score, quiz_date)
    )

    connection.commit()
    connection.close()


# Get all quiz scores
def get_quiz_scores():

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM quiz_scores ORDER BY id DESC"
    )

    scores = cursor.fetchall()

    connection.close()

    return scores

# Save a study session
def add_study_session(minutes, session_date):

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO study_sessions (minutes, date)
        VALUES (?, ?)
        """,
        (minutes, session_date)
    )

    connection.commit()
    connection.close()


# Get all study sessions
def get_study_sessions():

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM study_sessions ORDER BY id DESC"
    )

    sessions = cursor.fetchall()

    connection.close()

    return sessions

# Get dashboard statistics
def get_dashboard_stats():

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    # Number of completed goals
    cursor.execute(
        "SELECT COUNT(*) FROM goals WHERE completed = 1"
    )
    completed_goals = cursor.fetchone()[0]

    # Number of quizzes
    cursor.execute(
        "SELECT COUNT(*) FROM quiz_scores"
    )
    quizzes = cursor.fetchone()[0]

    # Average quiz score
    cursor.execute(
        "SELECT AVG(score) FROM quiz_scores"
    )
    average_score = cursor.fetchone()[0]

    if average_score is None:
        average_score = 0

    # Total study time
    cursor.execute(
        "SELECT SUM(minutes) FROM study_sessions"
    )
    total_minutes = cursor.fetchone()[0]

    if total_minutes is None:
        total_minutes = 0

    connection.close()

    return (
        completed_goals,
        quizzes,
        average_score,
        total_minutes
    )

# Update goal completion status
def update_goal_status(goal_id, completed):

    connection = sqlite3.connect("study_assistant.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE goals
        SET completed = ?
        WHERE id = ?
        """,
        (int(completed), goal_id)
    )

    connection.commit()
    connection.close()
