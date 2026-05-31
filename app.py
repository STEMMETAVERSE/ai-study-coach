import streamlit as st
import os
from huggingface_hub import InferenceClient

# ---------------- CONFIG ----------------

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)

# ---------------- UI ----------------

st.title("🏆 AI Study Coach")

goal = st.text_input(
    "What are you studying?",
    placeholder="Python Programming, Machine Learning, Calculus..."
)

# ---------------- GENERATE PLAN ----------------

if st.button("Get Study Plan"):

    if not goal.strip():

        st.warning("Please enter a study goal.")

    elif not HF_TOKEN:

        st.error("HF_TOKEN secret key is missing.")

    else:

        prompt = f"""
Create a motivating study plan for:

{goal}

Include:
1. Daily study schedule
2. Weekly goals
3. Revision strategy
4. Productivity tips
5. Motivational advice

Keep the plan practical and beginner-friendly.
"""

        with st.spinner("Building your study plan..."):

            try:

                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.2-1B-Instruct",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert study coach helping students learn effectively."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=400,
                    temperature=0.7,
                    top_p=0.9
                )

                study_plan = response.choices[0].message.content

                st.subheader("📚 Your Study Plan")

                st.markdown(study_plan)

            except Exception as e:

                st.error(f"System Response: {e}")
