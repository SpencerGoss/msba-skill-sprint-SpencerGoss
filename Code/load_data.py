import sqlite3
import pandas as pd
import os

# Read CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "../Data/retentiondata_case.csv")
csv_path = os.path.abspath(csv_path)

print(f"Loading CSV from: {csv_path}")
df = pd.read_csv(csv_path)

print(f"Loading {len(df)} records from CSV...")

# Connect to SQLite database
conn = sqlite3.connect('retention.db')
cursor = conn.cursor()

# Insert into customers table
customers_data = df[['acct_ref', 'cust_ref', 'gender', 'age_years', 'is_married', 'has_dependents', 'dependents_count', 'referred_friend', 'referrals_count']].drop_duplicates(subset=['acct_ref'])
for _, row in customers_data.iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO customers 
        (acct_ref, cust_ref, gender, age_years, is_married, has_dependents, dependents_count, referred_friend, referrals_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

# Insert into service_subscriptions table
service_cols = ['acct_ref', 'internet_plan', 'home_phone', 'multi_line', 'add_on_security', 'add_on_backup', 'add_on_protection', 'tech_support_std', 'stream_tv', 'stream_movies', 'stream_music', 'unlimited_data_opt', 'premium_support', 'internet_tech', 'avg_gb_download']
for _, row in df[service_cols].iterrows():
    cursor.execute('''
        INSERT INTO service_subscriptions 
        (acct_ref, internet_plan, home_phone, multi_line, add_on_security, add_on_backup, add_on_protection, tech_support_std, stream_tv, stream_movies, stream_music, unlimited_data_opt, premium_support, internet_tech, avg_gb_download)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

# Insert into account_contracts table
contract_cols = ['acct_ref', 'contract_term', 'e_bill_opt_in', 'pay_method', 'tenure_mo', 'recent_offer', 'fiscal_qtr']
for _, row in df[contract_cols].drop_duplicates(subset=['acct_ref']).iterrows():
    cursor.execute('''
        INSERT INTO account_contracts 
        (acct_ref, contract_term, e_bill_opt_in, pay_method, tenure_mo, recent_offer, fiscal_qtr)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

# Insert into billing_fees table
billing_cols = ['acct_ref', 'monthly_fee', 'total_billed', 'refunds_total', 'extra_data_fees_total', 'long_dist_fees_total', 'avg_long_dist_fee']
for _, row in df[billing_cols].iterrows():
    cursor.execute('''
        INSERT INTO billing_fees 
        (acct_ref, monthly_fee, total_billed, refunds_total, extra_data_fees_total, long_dist_fees_total, avg_long_dist_fee)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

# Insert into churn_data table
churn_cols = ['acct_ref', 'left_flag']
for _, row in df[churn_cols].drop_duplicates(subset=['acct_ref']).iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO churn_data 
        (acct_ref, left_flag)
        VALUES (?, ?)
    ''', tuple(row))

# Commit changes
conn.commit()


