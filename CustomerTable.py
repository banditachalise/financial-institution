
import os 
import pyodbc
import pandas as pd

# ---------------------- Connect to SQL Server ----------------------
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=BANDEYYY;"       # Your server name
    "Database=DATAPROJECT;"  # Your database name
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)

# ---------------------- Load Customer Table ----------------------
Customer_df = pd.read_sql("SELECT * FROM Customer", conn)
print("\n✅ Connected and loaded Customer table successfully!\n")

# ---------------------- Check for NULL Values ----------------------
print("--- NULL Value Count by Column (Customer Table) ---")
print(Customer_df.isnull().sum())

# ---------------------- Check for duplicate records ----------------------
print("\n--- Duplicate Customers (by Name + ContactInfo) ---")
duplicates = Customer_df[Customer_df.duplicated(subset=["Name", "ContactInfo"], keep=False)]
print(duplicates if not duplicates.empty else "No duplicates found ✅")

# ---------------------- Validate Age values ----------------------
Customer_df['Age'] = pd.to_numeric(Customer_df['Age'], errors='coerce')
invalid_ages = Customer_df[(Customer_df["Age"] < 0) | (Customer_df["Age"] > 120)]
print("\n--- Invalid Ages ---")
print(invalid_ages if not invalid_ages.empty else "All ages are valid ✅")

# ---------------------- Check for invalid contact info ----------------------
print("\n--- Invalid Contact Info ---")
invalid_contact = Customer_df[Customer_df["ContactInfo"].str.len() < 10]
print(invalid_contact if not invalid_contact.empty else "All contact info is valid ✅")

# ---------------------- Check for missing or blank addresses ----------------------
print("\n--- Missing or Blank Addresses ---")
invalid_address = Customer_df[Customer_df["Address"].isnull() | (Customer_df["Address"].str.strip() == "")]
print(invalid_address if not invalid_address.empty else "All addresses are valid ✅")

# ---------------------- Logical errors: ClosedDate before JoinedDate ----------------------
print("\n--- Logical Date Errors (Closed before Joined) ---")
logical_error = Customer_df[
    (Customer_df["ClosedDate"].notnull()) & (Customer_df["ClosedDate"] < Customer_df["JoinedDate"])
]
print(logical_error if not logical_error.empty else "No logical date errors ✅")

# ---------------------- Ensure numeric columns for balance and loan ----------------------
Customer_df['CurrentBalance'] = pd.to_numeric(Customer_df['CurrentBalance'], errors='coerce')
Customer_df['OutstandingLoan'] = pd.to_numeric(Customer_df['OutstandingLoan'], errors='coerce')

# ---------------------- Check for negative balances ----------------------
print("\n--- Negative CurrentBalance ---")
print(Customer_df[Customer_df['CurrentBalance'] < 0] if not Customer_df[Customer_df['CurrentBalance'] < 0].empty else "No negative CurrentBalance ✅")

print("\n--- Negative OutstandingLoan ---")
print(Customer_df[Customer_df['OutstandingLoan'] < 0] if not Customer_df[Customer_df['OutstandingLoan'] < 0].empty else "No negative OutstandingLoan ✅")


# Show customers with NULL CurrentBalance
null_current = Customer_df[Customer_df['CurrentBalance'].isnull()]
print("\n--- Customers with NULL CurrentBalance ---")
print(null_current)

Customer_df.to_csv(r"C:\Users\chali\OneDrive\Documents\bandeyyy\DATAPROJECT\PYTHON\Customer_Cleaned.csv", index=False)
print("✅ Cleaned Customer table exported as")


# ---------------------- Close connection ----------------------
conn.close()
print("\n✅ Database connection closed.")
