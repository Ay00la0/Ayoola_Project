# Project HCI 584X - Personal Budgeting and Expense Tracker
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


# Set up the page
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title('Personal Expense Tracker')


# load data
def load_data():
    try:
        return pd.read_excel('expenses.xlsx')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

# Function to save data
def save_data(df):
    df.to_excel('expenses.xlsx', index=False)



# Sidebar for adding expenses
with st.sidebar:
    st.header('Add New Expense')
    amount = st.number_input('Amount ($)', min_value=0.01, format='%.2f')
    category = st.selectbox('Category', ['Food', 'Housing', 'Transportation', 'Utilities', 'Entertainment', 'Healthcare', 'Other'])
    date = st.date_input('Date', value=datetime.now())

    if st.button('Log Expense'):
        df = load_data()
        new_expense = pd.DataFrame({'Date': [date], 'Category': [category], 'Amount': [amount]})
        df = pd.concat([df, new_expense], ignore_index=True)
        save_data(df)
        st.success(f'Expense logged: ${amount:.2f} in {category} on {date}')

# Load expense data
df = load_data()


# If there's data, display charts
if not df.empty:
    # Expenses by category - Bar chart
    st.subheader('Expenses by Category')
    category_total = df.groupby('Category')['Amount'].sum()
    fig_bar = px.bar(category_total, x=category_total.index, y=category_total.values, title='Expenses', labels={'x': 'Category', 'y': 'Amount'})
    st.plotly_chart(fig_bar)

    # Expenses over time - Line chart
    st.subheader('Expenses Over Time')
    daily_expenses = df.groupby('Date')['Amount'].sum().reset_index()
    fig_line = px.line(daily_expenses, x='Date', y='Amount', title='Daily Expenses')
    st.plotly_chart(fig_line)

    # Expense Summary - Metrics
    st.subheader('Expense Summary')
    total_spent = df['Amount'].sum()
    avg_daily = total_spent / len(df['Date'].unique())
    highest_expense = df['Amount'].max()
    col1, col2, col3 = st.columns(3)
    col1.metric('Total Spent', f'${total_spent:.2f}')
    col2.metric('Average Daily Spend', f'${avg_daily:.2f}')
    col3.metric('Highest Single Expense', f'${highest_expense:.2f}')
    
    # Filter and display recent expenses in a table
    st.subheader('Recent Expenses')
    selected_categories = st.multiselect('Filter by Category', options=df['Category'].unique(), default=df['Category'].unique())
    date_range = st.date_input('Filter by Date Range', value=(df['Date'].min(), df['Date'].max()), key='date_range_input')
    
    # Verify that two dates were selected
    if len(date_range) != 2:
        st.warning('Please select both start and end dates')
    else:
        # Convert DataFrame's Date column to date objects
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        filtered_df = df[
            (df['Category'].isin(selected_categories)) & 
            (df['Date'] >= date_range[0]) & 
            (df['Date'] <= date_range[1])
            ]
        st.dataframe(filtered_df.style.format({'Amount': '${:.2f}', 'Date': lambda x: x.strftime('%Y-%m-%d')}))

        # Download filtered data as CSV
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button('Download filtered data as CSV', data=csv, file_name='expenses.csv', mime='text/csv')

else:
    st.info('No expenses logged yet. Use the sidebar to add your first expense!')


