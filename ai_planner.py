import streamlit as st
from openai import OpenAI


def generate_study_plan(subject, exam_date, daily_minutes, difficulty):

    if "OPENAI_API_KEY" not in st.secrets:
        raise ValueError(
            "OpenAI API key is not configured."
        )

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    prompt = f"""
You are an AI study planner for a college student.

Create a practical and realistic study plan.

Student details:
- Subject: {subject}
- Exam date: {exam_date}
- Daily study time: {daily_minutes} minutes
- Difficulty level: {difficulty}

Create the plan in simple English.

Include:
1. Study strategy
2. Day-by-day study plan
3. Important topics to focus on
4. Practice activities
5. Revision plan
6. Final exam-day tips

Keep the plan realistic for a college student.
Use clear headings and bullet points.
"""

    response = client.responses.create(
        model=st.secrets.get("OPENAI_MODEL", "gpt-6-luna"),
        input=prompt
    )

    return response.output_text
