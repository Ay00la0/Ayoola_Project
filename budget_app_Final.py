# %pip install openpyxl
# %pip install streamlit
# %pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set up the page
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title('Personal Expense Tracker')

# Load or initialize categories
CATEGORY_FILE = 'categories.xlsx'

def load_categories():
    try:
        return pd.read_excel(CATEGORY_FILE)['Category'].tolist()
    except FileNotFoundError:
        return ['Food', 'Housing', 'Transportation', 'Utilities', 'Personal Care', 'Education', 'Savings and Investments', 'Entertainment', 'Healthcare', 'Other']

def save_categories(categories):
    pd.DataFrame({'Category': categories}).to_excel(CATEGORY_FILE, index=False)

categories = load_categories()

# Load expense data
EXPENSE_FILE = 'expenses_Final.xlsx'

def load_data():
    try:
        return pd.read_excel(EXPENSE_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Category', 'Amount'])

def save_data(df):
    df.to_excel(EXPENSE_FILE, index=False)

df = load_data()

# Ensure the 'Date' column is in datetime.date format (date only)
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

# Sidebar for managing categories
with st.sidebar:
    st.header("Manage Categories")
    st.write("Current Categories:")
    st.write(categories)
    
    # Add a new category
    new_category = st.text_input("Add New Category")
    if st.button("Add Category"):
        if new_category and new_category not in categories:
            categories.append(new_category)
            save_categories(categories)
            st.success(f"Added new category: {new_category}")
        else:
            st.warning("Category already exists or is empty.")

    # Delete an existing category
    category_to_delete = st.selectbox("Delete Category", options=categories)
    if st.button("Delete Category"):
        if category_to_delete in categories:
            categories.remove(category_to_delete)
            save_categories(categories)
            st.success(f"Deleted category: {category_to_delete}")
        else:
            st.warning("Category not found.")

# Sidebar for adding expenses
with st.sidebar:
    st.header('Add New Expense')
    amount = st.number_input('Amount ($)', min_value=0.01, format='%.2f')
    category = st.selectbox('Category', categories)
    date = st.date_input('Date', value=datetime.now().date())  # Use date only

    if st.button('Log Expense'):
        new_expense = pd.DataFrame({'Date': [date], 'Category': [category], 'Amount': [amount]})
        df = pd.concat([df, new_expense], ignore_index=True)
        save_data(df)
        st.success(f'Expense logged: ${amount:.2f} in {category} on {date}')

# Main content: Show and analyze expenses
if not df.empty:
    # Expenses by category
    st.subheader("Expenses by Category")
    category_total = df.groupby('Category')['Amount'].sum()
    fig = px.bar(category_total, x=category_total.index, y=category_total.values, title="Expenses by Category")
    st.plotly_chart(fig)
    
    # Calculate metrics
    total_spent = df['Amount'].sum()
    avg_daily = total_spent / len(df['Date'].unique()) if len(df['Date'].unique()) > 0 else 0
    highest_expense = df['Amount'].max()

    # Display metrics
    st.subheader("Expense Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"${total_spent:.2f}")
    col2.metric("Average Daily Spending", f"${avg_daily:.2f}")
    col3.metric("Highest Single Expense", f"${highest_expense:.2f}")


    # Recent expenses table
    st.subheader("Recent Expenses")
    st.dataframe(df)
else:
    st.info("No expenses logged yet. Use the sidebar to add your first expense!")
