# Import of the necessary libaries
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import random
import time

# The Google Sheet is connected to our app
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read()

# Plotting the business question
st.markdown("<h2 style='text-align: center;'>Which district from NY is the one where more taxis are picked up?</h3>", unsafe_allow_html=True)

# Pie chart configurations
pie_chart, ax_pie = plt.subplots(figsize=(4, 4))
ax_pie.pie(data['Pickups'], labels=data['Borough'], autopct='%1.1f%%', startangle=120, textprops={'fontsize': 8}, labeldistance=1.1)
ax_pie.axis('equal')

# Bar chart configurations
bar_chart, ax_bar = plt.subplots(figsize=(4, 4))
ax_bar.bar(data['Borough'], data['Pickups'], color=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
ax_bar.tick_params(axis='x', labelsize=7)
ax_bar.tick_params(axis='y', labelsize=7)

# Configuration of the different state sessions
if "start_time" not in st.session_state:
    st.session_state.start_time = None # Tracking if the timer has started
if "answered" not in st.session_state:
    st.session_state.answered = False # Tracking if the user has answered the question
if "graph_shown" not in st.session_state:
    st.session_state.graph_shown = False  # Tracking if graph has been shown

# Configuration of the button that randomly displays one of the graphs
random_button = st.button("Click here to visualize a graph")

if random_button:
    graph = random.choice([1, 2]) # Randomly choosing a graph

    if graph == 1:
        st.pyplot(pie_chart)
        
    elif graph == 2:
        st.pyplot(bar_chart)

    st.session_state.start_time = time.time() # Starts the counter
    st.session_state.graph_shown = True  # Indicates that the graph has been shown to allow the Answer button to be displayed
    st.session_state.answered = False # Question has not been answered yet

# Configutation of the Answer button
if st.session_state.graph_shown and not st.session_state.answered:
    answer = st.button("I answered your question")

    if answer:
        end = time.time()
        time_taken = end - st.session_state.start_time # Once the user has answered, the time taken between clicking the two buttons is calculated

        st.write(f"It has taken you {time_taken:.2f} seconds to answer the question.") # And shown to the user
        st.session_state.answered = True

# Once the time taken is shown, a button to reset and rerun everything and allow the user to strat again appears
if st.session_state.answered:
    if st.button("Try again :)"):
        st.session_state.start_time = None
        st.session_state.answered = False
        st.session_state.graph_shown = False
        st.rerun()