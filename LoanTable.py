

import pyodbc
import pandas as pd
from datetime import datetime

# =============================================================================
# ---------------------- STEP 1: Connect to SQL Server ----------------------
# =============================================================================
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=BANDEYYY;"       # Replace with your server name
    "Database=DATAPROJECT;"  # Replace with your database name
    "Trusted_Connection=yes;"
    "Encrypt=no;"            # Windows Authentication
)

# =============================================================================
# ---------------------- STEP 2: Load Tables ----------------------
# =============================================================================
Loan_df = pd.read_sql("SELECT * FROM Loan", conn)
print("\n✅ Connected and loaded Loan table successfully!\n")

Transaction_df = pd.read_sql("SELECT * FROM [Transaction]", conn)
print("\n✅ Connected and loaded Transaction table successfully!\n")

# =============================================================================
# ---------------------- STEP 3: Basic Data Quality Checks ----------------------
# =============================================================================

# 1. Check for NULL values
print("--- NULL Value Count by Column (Loan Table) ---")
print(Loan_df.isnull().sum())

# 2. Check for negative or zero loan amounts
print("\n--- Loans with Amount <= 0 ---")
negative_loans = Loan_df[Loan_df['Amount'] <= 0]
print(negative_loans if not negative_loans.empty else "No negative/zero amounts ✅")

# 3. Check logical dates (IssuedDate should not be after ClosedDate)
print("\n--- Loans with IssuedDate after ClosedDate ---")
logical_date_errors = Loan_df[Loan_df['IssuedDate'] > Loan_df['ClosedDate']]
print(logical_date_errors if not logical_date_errors.empty else "No logical date errors ✅")

# 4. Check status vs Amount consistency
print("\n--- Status inconsistencies ---")
status_inconsistencies = Loan_df[
    ((Loan_df['Status'] == 'Closed') & (Loan_df['Amount'] > 0)) |
    ((Loan_df['Status'] == 'Active') & (Loan_df['Amount'] == 0))
]
print(status_inconsistencies if not status_inconsistencies.empty else "All statuses consistent ✅")

# 5. Check for invalid CustomerIDs
print("\n--- Loans with invalid CustomerID ---")
valid_customers = pd.read_sql("SELECT CustomerID FROM Customer", conn)
invalid_customers = Loan_df[~Loan_df['CustomerID'].isin(valid_customers['CustomerID'])]
print(invalid_customers if not invalid_customers.empty else "All CustomerIDs valid ✅")

# 6. Check for duplicate LoanIDs
print("\n--- Duplicate LoanIDs ---")
duplicate_loans = Loan_df[Loan_df.duplicated(subset=['LoanID'], keep=False)]
print(duplicate_loans if not duplicate_loans.empty else "No duplicate LoanIDs ✅")

# 7. Optional: Identify unusually large loans (example threshold: 1,000,000)
print("\n--- Loans exceeding 1,000,000 ---")
large_loans = Loan_df[Loan_df['Amount'] > 1000000]
print(large_loans if not large_loans.empty else "No unusually large loans ✅")

# =============================================================================
# ---------------------- STEP 4: Loan Payment Analysis ----------------------
# =============================================================================

# Filter transactions for Loan Payments only
loan_payments = Transaction_df[Transaction_df['TransactionType'] == 'Loan Payment']

# Merge loans with payments using CustomerID
loans_with_txn = Loan_df.merge(
    loan_payments,
    on='CustomerID',
    how='left',
    suffixes=('_loan', '_txn')
)

# Calculate total payment per loan
payments = loans_with_txn.groupby(['LoanID', 'CustomerID'])['Amount_txn'].sum().reset_index()
payments.rename(columns={'Amount_txn':'TotalPaid'}, inplace=True)

# Merge total payments with original Loan table
loan_analysis = Loan_df.merge(payments, on=['LoanID', 'CustomerID'], how='left')
loan_analysis['TotalPaid'] = loan_analysis['TotalPaid'].fillna(0)

# Calculate expected interest and outstanding balance
loan_analysis['ExpectedInterest'] = loan_analysis['Amount'] * (loan_analysis['InterestRate'] / 100)
loan_analysis['Outstanding'] = loan_analysis['Amount'] + loan_analysis['ExpectedInterest'] - loan_analysis['TotalPaid']

# Check overdue loans
today = pd.to_datetime(datetime.today().date())
loan_analysis['LoanDueDate'] = pd.to_datetime(loan_analysis['LoanDueDate'], errors='coerce')
loan_analysis['IsOverdue'] = (loan_analysis['LoanDueDate'] < today) & (loan_analysis['Outstanding'] > 0)

# Display loan analysis
print("\n--- Loan Analysis ---")
print(loan_analysis[['CustomerID','LoanID','Amount','ExpectedInterest','TotalPaid','Outstanding','IsOverdue']])

# =============================================================================
# ---------------------- STEP 5: Status vs Dates Check ----------------------
# =============================================================================

# Convert dates for consistency
Loan_df['ClosedDate'] = pd.to_datetime(Loan_df['ClosedDate'], errors='coerce')
Loan_df['LoanDueDate'] = pd.to_datetime(Loan_df['LoanDueDate'], errors='coerce')

# Find loans with status vs ClosedDate / LoanDueDate issues
late_or_overdue_loans = Loan_df[
    ((Loan_df['Status'] == 'Closed') & (Loan_df['ClosedDate'] > Loan_df['LoanDueDate'])) |
    ((Loan_df['Status'] == 'Active') & ((Loan_df['ClosedDate'].notna()) | (Loan_df['LoanDueDate'] <= today)))
]

# Display inconsistencies
print("\n--- Loans with Status vs ClosedDate / LoanDueDate Issues ---")
print(late_or_overdue_loans[['LoanID','CustomerID','Status','LoanDueDate','ClosedDate']])




Loan_df.to_csv(r"C:\Users\chali\OneDrive\Documents\bandeyyy\DATAPROJECT\PYTHON\Customer_Loan.csv", index=False)
print("✅ Cleaned Loan table exported as")


# =============================================================================
# ---------------------- STEP 6: Close Database Connection ----------------------
# =============================================================================
conn.close()
print("\n✅ Loan table checks complete and database connection closed.")
