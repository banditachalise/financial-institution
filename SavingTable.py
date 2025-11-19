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
Saving_df = pd.read_sql("SELECT * FROM Saving", conn)
print("\n✅ Connected and loaded Saving table successfully!\n")

Transaction_df = pd.read_sql("SELECT * FROM [Transaction]", conn)
print("\n✅ Connected and loaded Transaction table successfully!\n")
"""
Saving_table_check.py
---------------------
Checks for data quality, inconsistencies, and basic summary of the Saving table.
"""

import pyodbc
import pandas as pd

# =============================================================================
# STEP 1: Connect to SQL Server
# =============================================================================
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=BANDEYYY;"       # Your server name
    "Database=DATAPROJECT;"  # Your database name
    "Trusted_Connection=yes;"
    "Encrypt=no;"            # Windows Authentication
)

# =============================================================================
# STEP 2: Load Tables
# =============================================================================
Saving_df = pd.read_sql("SELECT * FROM Saving", conn)
print("\n✅ Connected and loaded Saving table successfully!\n")

Customer_df = pd.read_sql("SELECT CustomerID FROM Customer", conn)
print("\n✅ Loaded Customer table for referential checks.\n")

# =============================================================================
# STEP 3: Basic Data Quality Checks
# =============================================================================
print("--- NULL Value Count by Column ---")
print(Saving_df.isnull().sum())

print("\n--- Data Types ---")
print(Saving_df.dtypes)

# Convert numeric columns to proper type (Balance, InterestRate, TimePeriod)
Saving_df['Balance'] = pd.to_numeric(Saving_df['Balance'], errors='coerce')
Saving_df['InterestRate'] = pd.to_numeric(Saving_df['InterestRate'], errors='coerce')
Saving_df['TimePeriod'] = pd.to_numeric(Saving_df['TimePeriod'], errors='coerce')

# ---------------------- Step 4: Check for negative or zero balances ----------------------
print("\n--- Accounts with Balance <= 0 ---")
negative_balances = Saving_df[Saving_df['Balance'] <= 0]
print(negative_balances if not negative_balances.empty else "No negative/zero balances ✅")

# ---------------------- Step 5: Logical values check ----------------------
# Check Month (1-12)
invalid_months = Saving_df[~Saving_df['Month'].between(1,12)]
print("\n--- Invalid Month Values ---")
print(invalid_months if not invalid_months.empty else "All months valid ✅")



# ---------------------- Step 6: Referential Integrity ----------------------
invalid_customers = Saving_df[~Saving_df['CustomerID'].isin(Customer_df['CustomerID'])]
print("\n--- Accounts with invalid CustomerID ---")
print(invalid_customers if not invalid_customers.empty else "All CustomerIDs valid ✅")

# ---------------------- Step 7: Duplicate AccountID ----------------------
duplicate_accounts = Saving_df[Saving_df.duplicated(subset=['SavingID'], keep=False)]
print("\n--- Duplicate SavingIDs ---")
print(duplicate_accounts if not duplicate_accounts.empty else "No duplicate SavingIDs ✅")

# ---------------------- Step 8: High balance check ----------------------
high_balance = Saving_df[Saving_df['Balance'] > 1000000]
print("\n--- Accounts with unusually high balance ---")
print(high_balance if not high_balance.empty else "No unusually high balances ✅")

# ---------------------- Step 9: Summary Analysis ----------------------
print("\n--- Savings Account Summary by Type ---")
print(Saving_df.groupby('Type')['Balance'].agg(['count','sum','mean']))

print("\n--- Savings Account Summary by Year ---")
print(Saving_df.groupby('Year')['Balance'].agg(['count','sum','mean']))

Saving_df.to_csv(r"C:\Users\chali\OneDrive\Documents\bandeyyy\DATAPROJECT\PYTHON\Saving_Cleaned.csv", index=False)
print("✅ Cleaned Saving table exported as")


# =============================================================================
# STEP 10: Close Connection
# =============================================================================
conn.close()
print("\n✅ Saving table checks complete and database connection closed.")
