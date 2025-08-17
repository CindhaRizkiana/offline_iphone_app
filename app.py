import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import uuid

# Set page configuration
st.set_page_config(
    page_title="Simple Budget App",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply iOS-like custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        border-bottom: 1px solid #f0f0f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
        gap: 0;
        padding-top: 10px;
        padding-bottom: 10px;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #007aff;
        border-bottom: 2px solid #007aff;
    }
    .stButton>button {
        background-color: #007aff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #0062cc;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f8f8;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetric"] > div:first-child {
        color: #007aff;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #f0f0f0;
    }
    [data-testid="stDataFrameResizable"] > div > div > div {
        background-color: #f8f8f8;
    }
    .stPlotlyChart {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {
        'income': pd.DataFrame({
            'Category': ['Salary', 'Side Hustle', 'Other'],
            'Amount': [0.0, 0.0, 0.0]
        }),
        'expenses': pd.DataFrame({
            'Category': ['Housing', 'Utilities', 'Groceries', 'Transportation', 
                        'Health', 'Entertainment', 'Personal', 'Debt', 'Savings', 'Other'],
            'Amount': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }),
        'transactions': pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount', 'Type']),
        'month': datetime.now().strftime('%B %Y')
    }

if 'file_path' not in st.session_state:
    st.session_state.file_path = None

# Helper functions
def save_to_excel(data, file_path=None):
    """Save budget data to Excel file"""
    if file_path is None:
        file_path = f"budget_{data['month'].replace(' ', '_')}.xlsx"
    
    with pd.ExcelWriter(file_path) as writer:
        data['income'].to_excel(writer, sheet_name='Income', index=False)
        data['expenses'].to_excel(writer, sheet_name='Expenses', index=False)
        data['transactions'].to_excel(writer, sheet_name='Transactions', index=False)
        
        # Create summary sheet
        summary = pd.DataFrame({
            'Category': ['Total Income', 'Total Expenses', 'Net'],
            'Amount': [
                data['income']['Amount'].sum(),
                data['expenses']['Amount'].sum(),
                data['income']['Amount'].sum() - data['expenses']['Amount'].sum()
            ]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)
    
    return file_path

def load_from_excel(file_path):
    """Load budget data from Excel file"""
    try:
        income = pd.read_excel(file_path, sheet_name='Income')
        expenses = pd.read_excel(file_path, sheet_name='Expenses')
        transactions = pd.read_excel(file_path, sheet_name='Transactions')
        
        # Convert date column to datetime if it exists
        if 'Date' in transactions.columns:
            transactions['Date'] = pd.to_datetime(transactions['Date']).dt.date
        
        month = os.path.basename(file_path).replace('budget_', '').replace('.xlsx', '').replace('_', ' ')
        
        return {
            'income': income,
            'expenses': expenses,
            'transactions': transactions,
            'month': month
        }
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Sidebar
st.sidebar.title("Budget Controls")

# Month selection
month = st.sidebar.text_input("Budget Month", value=st.session_state.budget_data['month'])
if month != st.session_state.budget_data['month']:
    st.session_state.budget_data['month'] = month

# File operations
st.sidebar.header("File Operations")

# Save to Excel
if st.sidebar.button("Save to Excel"):
    file_path = save_to_excel(st.session_state.budget_data)
    st.sidebar.success(f"Saved to {file_path}")
    st.session_state.file_path = file_path

# Load from Excel
uploaded_file = st.sidebar.file_uploader("Load from Excel", type="xlsx")
if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_file = f"temp_{uuid.uuid4()}.xlsx"
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load the data
    loaded_data = load_from_excel(temp_file)
    if loaded_data:
        st.session_state.budget_data = loaded_data
        st.sidebar.success("Data loaded successfully!")
    
    # Clean up the temporary file
    try:
        os.remove(temp_file)
    except:
        pass

# Main content
st.title("Budget App")

# Month selector at the top
col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Budget for: {st.session_state.budget_data['month']}")
with col2:
    if st.button("Change Month"):
        st.session_state.show_month_selector = True

# Month selection popup
if 'show_month_selector' not in st.session_state:
    st.session_state.show_month_selector = False

if st.session_state.show_month_selector:
    with st.expander("Select Month", expanded=True):
        month = st.text_input("Budget Month", value=st.session_state.budget_data['month'])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save"):
                st.session_state.budget_data['month'] = month
                st.session_state.show_month_selector = False
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.show_month_selector = False
                st.rerun()

# Create tabs with iOS-style icons
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💵 Income", "💸 Expenses", "📝 Transactions"])

with tab1:
    st.header("Overview")
    
    # Calculate totals
    total_income = st.session_state.budget_data['income']['Amount'].sum()
    total_expenses = st.session_state.budget_data['expenses']['Amount'].sum()
    net = total_income - total_expenses
    
    # Display summary metrics in iOS-style cards
    st.markdown("### This Month")
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"${total_income:.2f}")
    col2.metric("Expenses", f"${total_expenses:.2f}")
    col3.metric("Balance", f"${net:.2f}", delta=f"${net:.2f}")
    
    # Progress bar for budget usage
    st.markdown("### Budget Usage")
    if total_income > 0:
        progress = min(total_expenses / total_income, 1.0)
        progress_color = "#4CAF50" if progress < 0.8 else "#FFA500" if progress < 1.0 else "#F44336"
        st.progress(progress)
        st.caption(f"You've used {progress*100:.1f}% of your income")
    else:
        st.info("Add income to see your budget usage")
    
    # Create charts with iOS-style colors
    st.markdown("### Income vs Expenses")
    
    # Bar chart comparing income and expenses
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=['Income'],
        y=[total_income],
        name='Income',
        marker_color='#34C759'  # iOS green
    ))
    fig1.add_trace(go.Bar(
        x=['Expenses'],
        y=[total_expenses],
        name='Expenses',
        marker_color='#FF3B30'  # iOS red
    ))
    fig1.update_layout(
        barmode='group',
        xaxis_title="",
        yaxis_title="Amount ($)",
        legend_title="",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="-apple-system")
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Expense breakdown pie chart
    if total_expenses > 0:
        st.markdown("### Expense Breakdown")
        fig2 = px.pie(
            st.session_state.budget_data['expenses'],
            values='Amount',
            names='Category',
            hole=0.5,
            color_discrete_sequence=[
                '#007AFF',  # iOS blue
                '#34C759',  # iOS green
                '#FF9500',  # iOS orange
                '#FF3B30',  # iOS red
                '#5856D6',  # iOS purple
                '#FF2D55',  # iOS pink
                '#AF52DE',  # iOS purple
                '#5AC8FA',  # iOS light blue
                '#FFCC00',  # iOS yellow
                '#8E8E93',  # iOS gray
            ]
        )
        fig2.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="-apple-system"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Add expenses to see your expense breakdown")

with tab2:
    st.header("Income")
    
    # Add new income button
    if st.button("+ Add Income Source", key="add_income"):
        st.session_state.show_add_income = True
    
    # Add income form
    if 'show_add_income' not in st.session_state:
        st.session_state.show_add_income = False
        
    if st.session_state.show_add_income:
        with st.form("add_income_form"):
            st.subheader("Add Income Source")
            category = st.text_input("Source Name")
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save"):
                    if category and amount > 0:
                        new_income = pd.DataFrame({
                            'Category': [category],
                            'Amount': [amount]
                        })
                        st.session_state.budget_data['income'] = pd.concat(
                            [st.session_state.budget_data['income'], new_income],
                            ignore_index=True
                        )
                        st.session_state.show_add_income = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_add_income = False
                    st.rerun()
    
    # Display income in iOS-style cards
    if not st.session_state.budget_data['income'].empty:
        for i, row in st.session_state.budget_data['income'].iterrows():
            col1, col2, col3 = st.columns([3, 1, 0.5])
            with col1:
                st.markdown(f"**{row['Category']}**")
            with col2:
                st.markdown(f"${row['Amount']:.2f}")
            with col3:
                if st.button("✏️", key=f"edit_income_{i}"):
                    st.session_state.edit_income_index = i
                    st.session_state.show_edit_income = True
    else:
        st.info("No income sources added yet. Click '+ Add Income Source' to get started.")
    
    # Edit income form
    if 'show_edit_income' not in st.session_state:
        st.session_state.show_edit_income = False
        st.session_state.edit_income_index = None
        
    if st.session_state.show_edit_income and st.session_state.edit_income_index is not None:
        i = st.session_state.edit_income_index
        with st.form("edit_income_form"):
            st.subheader("Edit Income Source")
            category = st.text_input("Source Name", value=st.session_state.budget_data['income'].loc[i, 'Category'])
            amount = st.number_input("Amount ($)", value=float(st.session_state.budget_data['income'].loc[i, 'Amount']), min_value=0.0, format="%.2f")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("Save"):
                    if category and amount >= 0:
                        st.session_state.budget_data['income'].loc[i, 'Category'] = category
                        st.session_state.budget_data['income'].loc[i, 'Amount'] = amount
                        st.session_state.show_edit_income = False
                        st.session_state.edit_income_index = None
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_edit_income = False
                    st.session_state.edit_income_index = None
                    st.rerun()
            with col3:
                if st.form_submit_button("Delete"):
                    st.session_state.budget_data['income'] = st.session_state.budget_data['income'].drop(i).reset_index(drop=True)
                    st.session_state.show_edit_income = False
                    st.session_state.edit_income_index = None
                    st.rerun()
    
    # Display income chart with iOS colors
    if not st.session_state.budget_data['income'].empty and st.session_state.budget_data['income']['Amount'].sum() > 0:
        st.markdown("### Income Distribution")
        fig = px.bar(
            st.session_state.budget_data['income'],
            x='Category',
            y='Amount',
            color='Category',
            text_auto='.2s',
            color_discrete_sequence=[
                '#007AFF',  # iOS blue
                '#34C759',  # iOS green
                '#FF9500',  # iOS orange
                '#FF3B30',  # iOS red
                '#5856D6',  # iOS purple
            ]
        )
        fig.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="-apple-system"),
            xaxis_title="",
            yaxis_title="Amount ($)"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Expenses")
    
    # Add new expense button
    if st.button("+ Add Expense", key="add_expense"):
        st.session_state.show_add_expense = True
    
    # Add expense form
    if 'show_add_expense' not in st.session_state:
        st.session_state.show_add_expense = False
        
    if st.session_state.show_add_expense:
        with st.form("add_expense_form"):
            st.subheader("Add Expense")
            category = st.text_input("Category Name")
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save"):
                    if category and amount > 0:
                        new_expense = pd.DataFrame({
                            'Category': [category],
                            'Amount': [amount]
                        })
                        st.session_state.budget_data['expenses'] = pd.concat(
                            [st.session_state.budget_data['expenses'], new_expense],
                            ignore_index=True
                        )
                        st.session_state.show_add_expense = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_add_expense = False
                    st.rerun()
    
    # Display expenses in iOS-style cards
    if not st.session_state.budget_data['expenses'].empty:
        for i, row in st.session_state.budget_data['expenses'].iterrows():
            col1, col2, col3 = st.columns([3, 1, 0.5])
            with col1:
                st.markdown(f"**{row['Category']}**")
            with col2:
                st.markdown(f"${row['Amount']:.2f}")
            with col3:
                if st.button("✏️", key=f"edit_expense_{i}"):
                    st.session_state.edit_expense_index = i
                    st.session_state.show_edit_expense = True
    else:
        st.info("No expenses added yet. Click '+ Add Expense' to get started.")
    
    # Edit expense form
    if 'show_edit_expense' not in st.session_state:
        st.session_state.show_edit_expense = False
        st.session_state.edit_expense_index = None
        
    if st.session_state.show_edit_expense and st.session_state.edit_expense_index is not None:
        i = st.session_state.edit_expense_index
        with st.form("edit_expense_form"):
            st.subheader("Edit Expense")
            category = st.text_input("Category Name", value=st.session_state.budget_data['expenses'].loc[i, 'Category'])
            amount = st.number_input("Amount ($)", value=float(st.session_state.budget_data['expenses'].loc[i, 'Amount']), min_value=0.0, format="%.2f")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("Save"):
                    if category and amount >= 0:
                        st.session_state.budget_data['expenses'].loc[i, 'Category'] = category
                        st.session_state.budget_data['expenses'].loc[i, 'Amount'] = amount
                        st.session_state.show_edit_expense = False
                        st.session_state.edit_expense_index = None
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_edit_expense = False
                    st.session_state.edit_expense_index = None
                    st.rerun()
            with col3:
                if st.form_submit_button("Delete"):
                    st.session_state.budget_data['expenses'] = st.session_state.budget_data['expenses'].drop(i).reset_index(drop=True)
                    st.session_state.show_edit_expense = False
                    st.session_state.edit_expense_index = None
                    st.rerun()
    
    # Display expense chart with iOS colors
    if not st.session_state.budget_data['expenses'].empty and st.session_state.budget_data['expenses']['Amount'].sum() > 0:
        st.markdown("### Expense Distribution")
        fig = px.bar(
            st.session_state.budget_data['expenses'],
            x='Category',
            y='Amount',
            color='Category',
            text_auto='.2s',
            color_discrete_sequence=[
                '#FF3B30',  # iOS red
                '#FF9500',  # iOS orange
                '#FFCC00',  # iOS yellow
                '#34C759',  # iOS green
                '#5AC8FA',  # iOS light blue
                '#007AFF',  # iOS blue
                '#5856D6',  # iOS purple
                '#FF2D55',  # iOS pink
            ]
        )
        fig.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="-apple-system"),
            xaxis_title="",
            yaxis_title="Amount ($)"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Transactions")
    
    # Add new transaction button
    if st.button("+ Add Transaction", key="add_transaction"):
        st.session_state.show_add_transaction = True
    
    # Add transaction form
    if 'show_add_transaction' not in st.session_state:
        st.session_state.show_add_transaction = False
        
    if st.session_state.show_add_transaction:
        with st.form("add_transaction_form"):
            st.subheader("Add Transaction")
            
            date = st.date_input("Date", value=datetime.now().date())
            trans_type = st.selectbox("Type", options=["Income", "Expense"])
            
            # Dynamic category options based on type
            if trans_type == "Income":
                category_options = list(st.session_state.budget_data['income']['Category'])
            else:
                category_options = list(st.session_state.budget_data['expenses']['Category'])
                
            if category_options:
                category = st.selectbox("Category", options=category_options)
            else:
                category = st.text_input("Category (please add categories first)")
                
            description = st.text_input("Description")
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save"):
                    if category and amount > 0:
                        # Add to transactions
                        new_transaction = pd.DataFrame({
                            'Date': [date],
                            'Category': [category],
                            'Description': [description],
                            'Amount': [amount],
                            'Type': [trans_type]
                        })
                        
                        st.session_state.budget_data['transactions'] = pd.concat(
                            [st.session_state.budget_data['transactions'], new_transaction],
                            ignore_index=True
                        )
                        
                        # Update income or expense totals
                        if trans_type == "Income":
                            idx = st.session_state.budget_data['income']['Category'] == category
                            if any(idx):
                                st.session_state.budget_data['income'].loc[idx, 'Amount'] += amount
                        else:  # Expense
                            idx = st.session_state.budget_data['expenses']['Category'] == category
                            if any(idx):
                                st.session_state.budget_data['expenses'].loc[idx, 'Amount'] += amount
                        
                        st.session_state.show_add_transaction = False
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_add_transaction = False
                    st.rerun()
    
    # Display transactions in iOS-style cards
    if not st.session_state.budget_data['transactions'].empty:
        # Group by date
        st.session_state.budget_data['transactions']['Date'] = pd.to_datetime(st.session_state.budget_data['transactions']['Date'])
        grouped = st.session_state.budget_data['transactions'].sort_values('Date', ascending=False).groupby(st.session_state.budget_data['transactions']['Date'].dt.date)
        
        for date, group in grouped:
            st.markdown(f"### {date.strftime('%B %d, %Y')}")
            
            for i, row in group.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                    with col1:
                        st.markdown(f"**{row['Category']}**")
                        if row['Description']:
                            st.caption(row['Description'])
                    with col2:
                        color = "#34C759" if row['Type'] == "Income" else "#FF3B30"
                        st.markdown(f"<span style='color:{color}'>${row['Amount']:.2f}</span>", unsafe_allow_html=True)
                    with col3:
                        st.caption(row['Type'])
                    with col4:
                        if st.button("✏️", key=f"edit_transaction_{i}"):
                            st.session_state.edit_transaction_index = i
                            st.session_state.show_edit_transaction = True
                st.markdown("<hr style='margin: 5px 0; opacity: 0.2'>", unsafe_allow_html=True)
    else:
        st.info("No transactions yet. Click '+ Add Transaction' to get started.")
    
    # Edit transaction form
    if 'show_edit_transaction' not in st.session_state:
        st.session_state.show_edit_transaction = False
        st.session_state.edit_transaction_index = None
        
    if st.session_state.show_edit_transaction and st.session_state.edit_transaction_index is not None:
        i = st.session_state.edit_transaction_index
        with st.form("edit_transaction_form"):
            st.subheader("Edit Transaction")
            
            date = st.date_input("Date", value=st.session_state.budget_data['transactions'].loc[i, 'Date'])
            trans_type = st.selectbox("Type", options=["Income", "Expense"], index=0 if st.session_state.budget_data['transactions'].loc[i, 'Type'] == "Income" else 1)
            
            # Dynamic category options based on type
            if trans_type == "Income":
                category_options = list(st.session_state.budget_data['income']['Category'])
            else:
                category_options = list(st.session_state.budget_data['expenses']['Category'])
                
            if category_options:
                try:
                    category_index = category_options.index(st.session_state.budget_data['transactions'].loc[i, 'Category'])
                except ValueError:
                    category_index = 0
                category = st.selectbox("Category", options=category_options, index=category_index)
            else:
                category = st.text_input("Category", value=st.session_state.budget_data['transactions'].loc[i, 'Category'])
                
            description = st.text_input("Description", value=st.session_state.budget_data['transactions'].loc[i, 'Description'])
            amount = st.number_input("Amount ($)", value=float(st.session_state.budget_data['transactions'].loc[i, 'Amount']), min_value=0.0, format="%.2f")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("Save"):
                    if category and amount > 0:
                        # Update transaction
                        st.session_state.budget_data['transactions'].loc[i, 'Date'] = date
                        st.session_state.budget_data['transactions'].loc[i, 'Category'] = category
                        st.session_state.budget_data['transactions'].loc[i, 'Description'] = description
                        st.session_state.budget_data['transactions'].loc[i, 'Amount'] = amount
                        st.session_state.budget_data['transactions'].loc[i, 'Type'] = trans_type
                        
                        st.session_state.show_edit_transaction = False
                        st.session_state.edit_transaction_index = None
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_edit_transaction = False
                    st.session_state.edit_transaction_index = None
                    st.rerun()
            with col3:
                if st.form_submit_button("Delete"):
                    st.session_state.budget_data['transactions'] = st.session_state.budget_data['transactions'].drop(i).reset_index(drop=True)
                    st.session_state.show_edit_transaction = False
                    st.session_state.edit_transaction_index = None
                    st.rerun()

# Add file operations to the bottom of the page instead of sidebar
st.markdown("---")
st.subheader("File Operations")

col1, col2 = st.columns(2)

with col1:
    # Save to Excel
    if st.button("Save to Excel", key="save_excel"):
        file_path = save_to_excel(st.session_state.budget_data)
        st.success(f"Saved to {file_path}")
        st.session_state.file_path = file_path

with col2:
    # Load from Excel
    uploaded_file = st.file_uploader("Load from Excel", type="xlsx")
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_file = f"temp_{uuid.uuid4()}.xlsx"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load the data
        loaded_data = load_from_excel(temp_file)
        if loaded_data:
            st.session_state.budget_data = loaded_data
            st.success("Data loaded successfully!")
        
        # Clean up the temporary file
        try:
            os.remove(temp_file)
        except:
            pass

# Footer
st.markdown("---")
st.caption("Simple Budget App - Made with ❤️")
