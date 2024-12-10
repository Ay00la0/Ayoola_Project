# Ease - Personal Budgeting and Expense Tracker
# By Ayoola Adebowale 341516232 
 Project for HCI584X Personal Budgeting and Expense Tracker 

This project helps users log, categorize, and visualize their personal expenses. It is built using Streamlit. The data can be exported to a CSV file. 

<ins> The Required Python Libraries: </ins> 
pandas
streamlit
plotly
openpyxl (for Excel file support)

**Using the EXpense Tracker**
1. Open Application in your web browser - Streamlit
2. Use bar to Enter an EXpense amount spent, Select category and Choose date of expenses and Click the Log Button.
3. You can also add and delete a category from the side bar.
4. Success message would be shown.

On the right hand side, you can navigate to the daily spending trends to view expenses by category

Click on either the Date, Category or Amount to reaarange in ascending or desending format.


**TROUBLESHOOT**
FileNotFoundError - If expenses.xlsx not in directory
No data for chart if expenses is not logged

**LIMITATIONS**
Data stored in Excel Files (Not suitable for high-volume dtata processing)

**FUTURE PLANS**
1. Saetting limit ofr easch category by Month or Year
2. Store large data in cloud datatbase
3. *** Trying to add the expenses summary and filtering and export CSV from budget_CH.py to the final py ***

**FOR DEVELOPERS**
Code Base - budget_CH_Final.py and expenses.xlsx

Extending the Project - Integrate with Financial APIs for automation and better Vizualization of datas in grapoh (Colour)


