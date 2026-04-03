import streamlit as st
import pandas as pd
import plotly.express as px

def initialize_session_state():
    """Initializes Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = [] # Chat history
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "evaluations" not in st.session_state:
        st.session_state.evaluations = []
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "role" not in st.session_state:
        st.session_state.role = ""

def plot_performance_chart(evaluations):
    """Generates a bar chart of scores per question."""
    if not evaluations:
        return None
    
    data = []
    for i, ev in enumerate(evaluations):
        data.append({
            "Question": f"Q{i+1}",
            "Score": ev.get("score", 0)
        })
    
    df = pd.DataFrame(data)
    fig = px.bar(df, x="Question", y="Score", range_y=[0, 10], 
                 title="Performance by Question", color="Score",
                 color_continuous_scale="RdBu")
    return fig
