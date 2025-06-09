import cx_Oracle
import pandas as pd
from datetime import datetime

# Database connection
import oracledb

# Don't call init_oracle_client() to stay in thin mode
conn = oracledb.connect(
    user="bank_reviews",
    password="1431",
    dsn="localhost:1521/XE"  # Adjust host and service name
)
print("Connection successful!")

def load_data_to_oracle(df):
    # Clean and enforce schema constraints
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['created_date'] = datetime.now()

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').clip(lower=1.0, upper=5.0).round(1)
    df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce').clip(lower=-1.0, upper=1.0).round(2)

    # Drop rows with missing critical fields

    banks = df[['bank']].drop_duplicates()
    banks['created_date'] = datetime.now()

    with conn.cursor() as cursor:
        bank_map = {}

        # Insert banks and get bank IDs
        for _, row in banks.iterrows():
            bank_id_var = cursor.var(oracledb.NUMBER)
            try:
                
                cursor.execute("""
                    INSERT INTO banks (bank_name, created_date)
                    VALUES (:1, :2)
                    RETURNING bank_id INTO :3
                """, [row['bank'], row['created_date'], bank_id_var])
                bank_map[row['bank']] = bank_id_var.getvalue()[0]
                print(f"Inserted bank: {row['bank']} with ID {bank_map[row['bank']]}")
            except oracledb.IntegrityError:
                # Bank already exists — fetch its ID
                print(f"Skipping bank due to error: {e}")
                cursor.execute("SELECT bank_id FROM banks WHERE bank_name = :1", [row['bank']])
                bank_map[row['bank']] = cursor.getvalue()[0]

        # Insert reviews
        success_count, fail_count = 0, 0
        for _, row in df.iterrows():
            try:
                rating = float(row['rating'])
                sentiment = float(row['sentiment'])

                # Clamp to valid ranges
                rating = min(rating, 9.9)
                sentiment = min(max(sentiment, 0), 9.99)
                cursor.execute("""
                    INSERT INTO reviews (
                        bank_id, review_date, rating, 
                        review_text, sentiment_score, label
                    ) VALUES (
                        :1, :2, :3,
                        :4, :5, :6
                    )
                """, [
                    bank_map[row['bank']],
                    row['date'].to_pydatetime(),
                    rating,
                    str(row['review']),
                    sentiment,
                    str(row['label']) if pd.notnull(row.get('label')) else None
                ])
                success_count += 1
            except Exception as e:
                print(f"Skipping review due to error: {e}")
                fail_count += 1

        conn.commit()
        print(f"✅ Inserted {success_count} reviews successfully.")
        print(f"⚠️ Skipped {fail_count} problematic rows.")