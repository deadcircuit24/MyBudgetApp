import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- CONFIG & SASSY THEMES ---
st.set_page_config(page_title="Budget Architect", layout="wide")

# Theme logic
themes = {
    "Professional": {"bg": "#FFFFFF", "text": "#000000"},
    "Barbie": {"bg": "#FFC0CB", "text": "#D01E64"},
    "Stranger Things": {"bg": "#000000", "text": "#E50914"},
    "One Piece": {"bg": "#F4D03F", "text": "#1A5276"}
}

theme_choice = st.sidebar.selectbox("Choose Your Vibe ✨", list(themes.keys()))
st.markdown(f"""<style>.stApp {{ background-color: {themes[theme_choice]['bg']}; color: {themes[theme_choice]['text']}; }}</style>""", unsafe_allow_html=True)

# --- DATABASE ENGINE (CSV) ---
def get_data(profile):
    filename = f"{profile.lower().replace(' ', '_')}_data.csv"
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Sub", "Amount"])

# --- SIDEBAR & PROFILES ---
st.sidebar.title("👤 Profiles")
active_profile = st.sidebar.radio("Switch Budgeting:", ["Personal", "College Fund", "Startup Savings"])
df = get_data(active_profile)

menu = st.sidebar.selectbox("Go to:", ["Dashboard", "Log Money", "Savings Goal"])

# --- LOGIC: ADDING DATA ---
if menu == "Log Money":
    st.header(f"📝 Logging for {active_profile}")
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            t_type = st.selectbox("Type", ["Income", "Expense"])
            cat = st.selectbox("Category", ["Food", "Stationary", "Clothes", "Travel", "Competition Wins", "Allowance"])
            sub = st.text_input("Sub-Category (e.g. Chocolates, Bus, Pen)")
        with col2:
            amt = st.number_input("Amount (INR)", min_value=0.0)
            dt = st.date_input("Date", date.today())
        
        if st.form_submit_button("Add Record"):
            new_row = pd.DataFrame([[dt, t_type, cat, sub, amt]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(f"{active_profile.lower().replace(' ', '_')}_data.csv", index=False)
            st.success("Got it! Money tracked. 💸")

# --- LOGIC: ANALYTICS ---
elif menu == "Dashboard":
    st.header(f"📊 {active_profile} Analytics")
    if not df.empty:
        df['Amount'] = df['Amount'].astype(float)
        expenses = df[df['Type'] == 'Expense']
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Spending by Category")
            fig = px.pie(expenses, values='Amount', names='Category', hole=0.4)
            st.plotly_chart(fig)
        with col2:
            st.subheader("Recent Transactions")
            st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.info("No data yet! Go log some expenses first.")

# --- LOGIC: SAVINGS GOAL (The "Cut the Chocolate" Logic) ---
elif menu == "Savings Goal":
    st.header("🎯 Financial Goals")
    goal_amt = st.number_input("How much do you need? (INR)", min_value=1.0)
    target_date = st.date_input("By when?", date.today())
    
    if st.button("Calculate Reality Check"):
        days_left = (target_date - date.today()).days
        if days_left <= 0:
            st.error("Unless you have a time machine, pick a future date! 🕰️")
        else:
            daily_needed = goal_amt / days_left
            st.write(f"You need to save **₹{daily_needed:.2f} per day**.")
            
            # Smart Suggestion
            choc_spend = df[df['Sub'].str.contains("chocolate", case=False, na=False)]['Amount'].sum()
            if choc_spend > 0:
                st.warning(f"💡 Bestie, you've spent ₹{choc_spend} on chocolates alone. Cut that out and you're much closer!")
            else:
                st.success("You're doing great! No unnecessary 'chocolate' spending detected yet. 🍫")