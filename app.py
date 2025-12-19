# streamlit_app.py

import streamlit as st
from agent import ReasoningAgent

# Initialize agent
agent = ReasoningAgent()

st.set_page_config(page_title="Multi-Step Reasoning Agent", layout="centered")

st.title("🧠 Multi-Step Reasoning Agent")
st.write(
    "This app demonstrates a planner–executor–verifier reasoning agent. "
    "Enter a question involving time calculation or simple logic."
)

# User input
question = st.text_input(
    "Enter your question:",
    placeholder="If a train leaves at 4:30 and arrives at 8:05, how long is the journey?"
)

# Run agent
if st.button("Run Agent"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking step by step..."):
            result = agent.solve(question)

        if result["status"] == "success":
            st.success("Answer")
            st.write(result["answer"])

            with st.expander("Show reasoning details"):
                st.markdown("**Plan:**")
                st.text(result["metadata"]["plan"])
                st.markdown("**Verification:**")
                st.json(result["metadata"]["checks"])
        else:
            st.error("Could not determine a valid answer")
            with st.expander("Debug details"):
                st.json(result)

st.markdown("---")
st.caption("Built by Srivani Nagunuri · Reasoning Agent Demo")