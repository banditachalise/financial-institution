import pyodbc
import pandas as pd
from datetime import datetime

# ---------------------- Connect to SQL Server ----------------------
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=BANDEYYY;"       # Your server name
    "Database=DATAPROJECT;"  # Your database name
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)

# ---------------------- Load Transaction Table ----------------------
Transaction_df = pd.read_sql("SELECT * FROM [Transaction]", conn)
print("\n✅ Connected and loaded Transaction table successfully!\n")

# =============================================================================
# STEP 3: Check for NULL Values
# =============================================================================
print("--- NULL Value Count by Column ([Transaction] Table) ---")
print(Transaction_df.isnull().sum())

# =============================================================================
# STEP 4: Duplicate TransactionIDs
# =============================================================================
duplicate_txns = Transaction_df[Transaction_df.duplicated(subset=['TransactionID'], keep=False)]
print("\n--- Duplicate TransactionIDs ---")
print(duplicate_txns if not duplicate_txns.empty else "No duplicate TransactionIDs ✅")

# =============================================================================
# STEP 5: Amount Checks
# =============================================================================
# Convert Amount to numeric (in case it's stored as string)
Transaction_df['Amount'] = pd.to_numeric(Transaction_df['Amount'], errors='coerce')

# Check for negative amounts (unexpected)
negative_amounts = Transaction_df[Transaction_df['Amount'] < 0]
print("\n--- Transactions with negative amounts ---")
print(negative_amounts if not negative_amounts.empty else "No unexpected negative amounts ✅")

# Check for unusually high amounts
high_amounts = Transaction_df[Transaction_df['Amount'] > 1000000]  # Example threshold
print("\n--- Transactions with unusually high amounts ---")
print(high_amounts if not high_amounts.empty else "No unusually high amounts ✅")

# =============================================================================
# STEP 6: TransactionType Checks
# =============================================================================
valid_types = ['Deposit', 'Withdrawal', 'Loan Payment', 'Fee']  # Add more if needed
invalid_types = Transaction_df[~Transaction_df['TransactionType'].isin(valid_types)]
print("\n--- Transactions with invalid TransactionType ---")
print(invalid_types if not invalid_types.empty else "All transaction types valid ✅")

# =============================================================================
# STEP 7: Date Checks
# =============================================================================
# Convert TransactionDate to datetime
Transaction_df['TransactionDate'] = pd.to_datetime(Transaction_df['TransactionDate'], errors='coerce', format='%Y-%m-%d')

# Check for invalid dates
invalid_dates = Transaction_df[Transaction_df['TransactionDate'].isna()]
print("\n--- Transactions with invalid dates ---")
print(invalid_dates if not invalid_dates.empty else "All dates valid ✅")

# Check for transactions in the future
today = pd.to_datetime(datetime.today().date())
future_dates = Transaction_df[Transaction_df['TransactionDate'] > today]
print("\n--- Transactions dated in the future ---")
print(future_dates if not future_dates.empty else "No future-dated transactions ✅")

# =============================================================================
# STEP 8: Referential Integrity
# =============================================================================
# Ensure CustomerID exists in Customer table
valid_customers = pd.read_sql("SELECT CustomerID FROM Customer", conn)
invalid_customers = Transaction_df[~Transaction_df['CustomerID'].isin(valid_customers['CustomerID'])]
print("\n--- Transactions with invalid CustomerID ---")
print(invalid_customers if not invalid_customers.empty else "All CustomerIDs valid ✅")

# =============================================================================
# STEP 9: Optional Summary Analysis
# =============================================================================
print("\n--- Transactions Summary by Type ---")
print(Transaction_df.groupby('TransactionType')['Amount'].agg(['count','sum','mean']))

print("\n--- Transactions Summary by Customer ---")
print(Transaction_df.groupby('CustomerID')['Amount'].agg(['count','sum','mean']))

Transaction_df.to_csv(r"C:\Users\chali\OneDrive\Documents\bandeyyy\DATAPROJECT\PYTHON\Transaction_Cleaned.csv", index=False)
print("✅ Cleaned Transaction table exported")


# =============================================================================
# STEP 10: Close Connection
# =============================================================================
conn.close()
print("\n✅ Transaction table checks complete and database connection closed.")