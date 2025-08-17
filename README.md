# Simple Budget App

A simple budgeting application that allows you to track income, expenses, and transactions. The app can import and export Excel files for easy data management.

## Features

- Track monthly income and expenses
- Record individual transactions
- Visualize budget data with charts
- Import/export data to Excel files
- Mobile-friendly interface
- Offline standalone mode available

## Installation

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. Run the application:

```
streamlit run app.py
```

## Usage

### Income & Expenses
- Add, edit, or remove income and expense categories
- Enter amounts for each category
- View visual breakdowns of your financial data

### Transactions
- Record individual transactions with date, category, description, and amount
- Transactions automatically update your income and expense totals

### File Operations
- Save your budget data to an Excel file
- Load budget data from a previously saved Excel file

### Offline Standalone Mode

To create a standalone executable that doesn't require running the server manually:

1. Double-click the `create_standalone.bat` file
2. Wait for the packaging process to complete
3. Navigate to the `dist/BudgetApp` folder
4. Double-click `BudgetApp.exe` to run the application

The standalone version will automatically start the server in the background and open the app in your default browser.

## For iOS Users
You can use this app on your iOS device by:

1. Running the app on your computer
2. Accessing it via your iOS device's web browser
3. Import/export Excel files that can be opened in iOS Numbers or Microsoft Excel

## License
This project is for personal use only.
