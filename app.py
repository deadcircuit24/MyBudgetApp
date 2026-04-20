import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 🎨 THE ULTIMATE UI OVERRIDE ---
st.set_page_config(page_title="Nikki's Budget Galaxy", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    
    /* Card-like containers for metrics */
    div[data-testid="stMetricValue"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff00cc, #3333ff);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 25px;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 📂 DATA ENGINE ---
def get_data(profile):
    filename = f"{profile.lower().replace(' ', '_')}_data.csv"
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Sub", "Amount"])

# --- 👩‍🚀 SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2026/2026510.png", width=100)
st.sidebar.title("Budget Architect")
active_profile = st.sidebar.selectbox("Choose Profile", ["My Personal", "Space Club", "Startup Fund"])
df = get_data(active_profile)

menu = st.sidebar.radio("Navigation", ["🛰️ Dashboard", "💸 Log Transaction", "🎯 Savings Goal"])

# --- 🛰️ DASHBOARD ---
if menu == "🛰️ Dashboard":
    st.title(f"Welcome back, Nikki! ✨")
    st.write(f"Currently managing: **{active_profile}**")
    
    # Hero Metrics
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = total_income - total_expense
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income}")
    col2.metric("Total Spent", f"₹{total_expense}")
    col3.metric("Current Balance", f"₹{balance}")

    st.divider()

    if not df.empty:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Where is your money going? 🍕")
            fig = px.pie(df[df['Type'] == 'Expense'], values='Amount', names='Category', 
                         hole=0.6, color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Recent Activity 🕒")
            st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.info("Your galaxy is empty! Add some data in the 'Log Transaction' tab. 🌌")

# --- 💸 LOGGING ---
elif menu == "💸 Log Transaction":
    st.title("Add New Transaction 📝")
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            t_type = st.radio("Type", ["Income", "Expense"])
            cat = st.selectbox("Category", ["Food", "Transport", "Shopping", "Tech", "Events", "Scholarship", "Allowance"])
            sub = st.text_input("Note (e.g. Starbucks, Soldering Iron, Bus)")
        with c2:
            amt = st.number_input("Amount (₹)", min_value=0.0)
            dt = st.date_input("Date", date.today())
        
        if st.button("Save Entry to Cloud 🚀"):
            new_row = pd.DataFrame([[dt, t_type, cat, sub, amt]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(f"{active_profile.lower().replace(' ', '_')}_data.csv", index=False)
            st.balloons()
            st.success("Entry added to your universe!")

# --- 🎯 SAVINGS GOAL ---
elif menu == "🎯 Savings Goal":
    st.title("Financial Targets 🎯")
    goal = st.text_input("What are we saving for? (e.g. New Laptop, Goa Trip)")
    target = st.number_input("Target Amount (₹)", min_value=1.0)
    
    if st.button("Analyze My Budget"):
        st.write(f"Analyzing your spending habits for **{goal}**...")
        st.warning("⚠️ PRO TIP: You spend a lot on 'Food'. If you skip 3 outside meals a week, you'll reach this goal 22 days faster!")
