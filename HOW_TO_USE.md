# How To Use The Budget Application

## Getting Started

1. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```
   streamlit run app.py
   ```

3. **Access the Application**
   - The app will automatically open in your default web browser
   - If it doesn't, open your browser and go to: http://localhost:8501

## Using the Application

### Summary Tab
- View your overall financial status at a glance
- See total income, expenses, and net amount
- Visual charts show income vs expenses and expense breakdown

### Income Tab
- Add income sources by clicking "Add rows" at the bottom of the table
- Enter amounts for each income category
- The income distribution chart updates automatically

### Expenses Tab
- Add or edit expense categories
- Enter amounts for each expense
- View the expense breakdown chart

### Transactions Tab
- Click "Add New Transaction" to expand the form
- Fill in:
  - Date: When the transaction occurred
  - Category: Select from your income or expense categories
  - Description: What the transaction was for
  - Amount: How much money was involved
  - Type: Whether it was income or an expense
- Click "Add Transaction" to record it
- All transactions appear in the table below

## Saving and Loading Data

### Save Your Budget
- Click "Save to Excel" in the sidebar
- The file will be saved in the application directory with the name format: `budget_Month_Year.xlsx`

### Load a Previous Budget
- Click "Browse files" in the "Load from Excel" section
- Select your previously saved Excel file
- Your budget data will be loaded into the application

## Using on iOS
1. Run the application on your computer
2. Make sure your iOS device is on the same network as your computer
3. Find your computer's IP address
4. On your iOS device, open a web browser and go to: http://[your-computer-ip]:8501
5. You can export Excel files that can be opened in iOS Numbers or Microsoft Excel

## Tips
- Set your budget month at the top of the sidebar
- Add transactions regularly to keep your budget up to date
- Save your budget file frequently
- Use the charts to visualize where your money is going
