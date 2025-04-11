import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime

# App setup
st.set_page_config(page_title="Student Budget Planner", layout="centered")
st.title("🎓 Student Budget Planner")
st.subheader("Plan your monthly expenses wisely!")

# Initialize session state to track monthly data
if 'monthly_data' not in st.session_state:
    st.session_state['monthly_data'] = []

# User Inputs
income = st.number_input("Monthly Income (₹)", min_value=0)

st.markdown("### Enter your monthly expenses:")
rent = st.number_input("🏠 Rent", min_value=0)
food = st.number_input("🍜 Food", min_value=0)
transport = st.number_input("🚌 Transport", min_value=0)
internet = st.number_input("🌐 Internet", min_value=0)
others = st.number_input("📦 Other Expenses", min_value=0)

if st.button("📊 Calculate Budget"):
    # Budget calculations
    total_expense = rent + food + transport + internet + others
    balance = income - total_expense

    st.markdown(f"### 💸 Total Expenses: ₹{total_expense}")
    st.markdown(f"### 💰 Remaining Balance: ₹{balance}")

    # Feedback
    if balance < 0:
        st.error("You're overspending! Try to cut down on some expenses. 😬")
    elif balance < income * 0.2:
        st.warning("You're cutting it close. Try to save a bit more! ⚠️")
    else:
        st.success("Great job! You're managing your budget well. ✅")

    # Pie Chart - Spending Breakdown
    labels = ['Rent', 'Food', 'Transport', 'Internet', 'Others']
    values = [rent, food, transport, internet, others]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Generate Report CSV
    report = pd.DataFrame({
        'Category': ['Income', 'Rent', 'Food', 'Transport', 'Internet', 'Others', 'Total Expenses', 'Remaining Balance'],
        'Amount': [income, rent, food, transport, internet, others, total_expense, balance]
    })

    csv = report.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV Report",
        data=csv,
        file_name='budget_report.csv',
        mime='text/csv',
    )

    # Save month data to session
    month = datetime.datetime.now().strftime("%B %Y")
    st.session_state['monthly_data'].append({
        'Month': month,
        'Income': income,
        'Expenses': total_expense,
        'Balance': balance
    })

# Plotly Bar Chart of all saved months
if len(st.session_state['monthly_data']) > 1:
    st.markdown("### 📈 Monthly Budget Trends")

    df_months = pd.DataFrame(st.session_state['monthly_data'])

    fig = px.bar(
        df_months,
        x="Month",
        y=["Income", "Expenses", "Balance"],
        barmode="group",
        title="Monthly Budget Overview",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)
