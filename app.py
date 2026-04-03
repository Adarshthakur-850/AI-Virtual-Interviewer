import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.evaluator import generate_questions, evaluate_answer
from src.utils import initialize_session_state, plot_performance_chart

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="AI Virtual Interviewer", layout="wide")

# Sidebar - Configuration
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))

if not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar or .env file to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# Initialize Session State
initialize_session_state()

# Title
st.title("🤖 AI Virtual Interviewer")

# --- Step 1: Setup Interview ---
if not st.session_state.interview_active:
    st.header("Start New Interview")
    role_input = st.selectbox("Select Role", ["Python Developer", "Data Scientist", "Machine Learning Engineer", "Frontend Developer", "DevOps Engineer", "Custom"])
    if role_input == "Custom":
        role_input = st.text_input("Enter Role Name")
    
    start_btn = st.button("Start Interview")
    
    if start_btn and role_input:
        with st.spinner(f"Generating questions for {role_input}..."):
            questions = generate_questions(client, role_input, count=5)
            st.session_state.questions = questions
            st.session_state.role = role_input
            st.session_state.current_question_idx = 0
            st.session_state.evaluations = []
            st.session_state.interview_active = True
            st.rerun()

# --- Step 2: Interview Loop ---
else:
    # Progress Bar
    progress = st.session_state.current_question_idx / len(st.session_state.questions)
    st.progress(progress)
    st.write(f"**Role:** {st.session_state.role} | **Question {st.session_state.current_question_idx + 1} of {len(st.session_state.questions)}**")
    
    # Check if we finished all questions
    if st.session_state.current_question_idx < len(st.session_state.questions):
        current_q = st.session_state.questions[st.session_state.current_question_idx]
        
        # Chat Interface
        st.chat_message("assistant").write(current_q)
        
        user_answer = st.text_area("Your Answer:", key=f"ans_{st.session_state.current_question_idx}")
        
        if st.button("Submit Answer"):
            if user_answer:
                with st.spinner("Evaluating..."):
                    # Evaluate
                    eval_result = evaluate_answer(
                        client, 
                        st.session_state.role, 
                        current_q, 
                        user_answer
                    )
                    st.session_state.evaluations.append({
                        "question": current_q,
                        "answer": user_answer,
                        "evaluation": eval_result
                    })
                    
                    # Store immediate feedback in chat (optional - keeping it hidden until end for "test" feel, or show now)
                    # For this design, we'll advance to next question
                    st.session_state.current_question_idx += 1
                    st.rerun()
            else:
                st.warning("Please provide an answer.")
                
    # --- Step 3: Final Report ---
    else:
        st.success("Interview Completed!")
        
        st.divider()
        st.header("📝 Performance Report")
        
        evals = [e["evaluation"] for e in st.session_state.evaluations]
        
        # Calculate Average Score
        total_score = sum([e.get("score", 0) for e in evals])
        avg_score = total_score / len(evals) if evals else 0
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Overall Score", f"{avg_score:.1f} / 10")
            if avg_score >= 8:
                st.balloons()
            elif avg_score >= 5:
                st.info("Good effort!")
            else:
                st.warning("Needs improvement.")
        
        with col2:
            fig = plot_performance_chart(evals)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Detailed Breakdown")
        for i, item in enumerate(st.session_state.evaluations):
            with st.expander(f"Q{i+1}: {item['question']} (Score: {item['evaluation'].get('score', 0)}/10)"):
                st.write(f"**Your Answer:** {item['answer']}")
                st.write(f"**Feedback:** {item['evaluation'].get('feedback', '')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write("✅ **Strengths**")
                    for s in item['evaluation'].get('strengths', []):
                        st.write(f"- {s}")
                with c2:
                    st.write("🔧 **Improvements**")
                    for imp in item['evaluation'].get('improvements', []):
                        st.write(f"- {imp}")
        
        if st.button("Restart Interview"):
            st.session_state.interview_active = False
            st.session_state.messages = []
            st.session_state.current_question_idx = 0
            st.session_state.evaluations = []
            st.rerun()
