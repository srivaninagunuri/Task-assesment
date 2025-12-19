import streamlit as st

# --------------------------------------------------
# Maximum Profit Optimization Logic
# --------------------------------------------------
def max_profit(n):
    max_earning = 0
    best_solution = (0, 0, 0)

    # Try all possible combinations
    for t in range(0, n // 5 + 1):
        for p in range(0, n // 4 + 1):
            for c in range(0, n // 10 + 1):

                build_time = 5 * t + 4 * p + 10 * c
                if build_time > n:
                    continue

                remaining_time = n
                earning = 0

                # Build Theatres
                for _ in range(t):
                    remaining_time -= 5
                    if remaining_time > 0:
                        earning += remaining_time * 1500

                # Build Pubs
                for _ in range(p):
                    remaining_time -= 4
                    if remaining_time > 0:
                        earning += remaining_time * 1000

                # Build Commercial Parks
                for _ in range(c):
                    remaining_time -= 10
                    if remaining_time > 0:
                        earning += remaining_time * 2000

                if earning > max_earning:
                    max_earning = earning
                    best_solution = (t, p, c)

    return max_earning, best_solution


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(
    page_title="Maximum Profit Optimizer",
    page_icon="🏗️",
    layout="centered"
)

st.title("🏗️ Maximum Profit Optimization")
st.write("Calculate the best construction strategy to maximize earnings.")

st.divider()

# Input
n = st.number_input(
    "Enter total available time units:",
    min_value=1,
    step=1
)

# Button
if st.button("Calculate Maximum Profit"):
    earning, (t, p, c) = max_profit(n)

    st.success("Calculation completed successfully!")

    st.subheader("📊 Results")
    st.write(f"💰 **Maximum Earnings:** ₹ {earning}")
    st.write(f"🎭 **Theatres (T):** {t}")
    st.write(f"🍻 **Pubs (P):** {p}")
    st.write(f"🏢 **Commercial Parks (C):** {c}")

    st.divider()

    st.subheader("📋 Optimal Construction Plan")
    st.table({
        "Building Type": ["Theatres", "Pubs", "Commercial Parks"],
        "Count": [t, p, c]
    })
