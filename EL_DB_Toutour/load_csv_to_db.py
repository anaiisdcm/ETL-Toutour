# EL_DB_Toutour/load_all_data.py
import os
import pandas as pd
from sqlalchemy import text
from .database import engine
from datetime import datetime, timedelta

def float_year_to_date(year_float):
    year = int(year_float)
    remainder = year_float - year
    start_of_year = datetime(year, 1, 1)
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    delta = timedelta(days=remainder * days_in_year)
    return (start_of_year + delta).date()

# --- 📋 Ordre de chargement (important !) ---
LOAD_ORDER = [
    ("owners", "df_Owner.csv"),
    ("walkers", "df_Walker.csv"),
    ("dogs", "df_Dog.csv"),
    ("walker_availabilities", "df_WalkerAvailability.csv"),
    ("walk_requests", "df_WalksRequests.csv"),
    ("past_walks", "df_past_walks.csv"),
    ("dog_reviews", "df_DogReview.csv"),
    ("walker_reviews", "df_WalkerReview.csv"),
    ("owner_payments", "df_OwnerPayment.csv"),
]

DATA_DIR = "./DataGeneration/data_out"

def load_table(table_name, csv_file):
    csv_path = os.path.join(DATA_DIR, csv_file)
    if not os.path.exists(csv_path):
        print(f"⚠️  CSV manquant pour {table_name} → {csv_file}")
        return False

    df = pd.read_csv(csv_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    if 'birth_date' in df.columns:
        df['birth_date'] = df['birth_date'].apply(float_year_to_date)

    try:
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))

        for start in range(0, len(df), 100):
            chunk = df.iloc[start:start+100]
            chunk.to_sql(table_name, engine, if_exists="append", index=False)
            print(f"   → {table_name}: lignes {start}-{start+len(chunk)-1} insérées")

        print(f"✅ Table {table_name} remplie ({len(df)} lignes)")
        return True

    except Exception as e:
        print(f"❌ Erreur lors du chargement de {table_name}: {e}")
        return False

def main():
    print(f"🚀 Chargement des données dans la base : {engine.url.database}")
    print("📂 Répertoire :", os.path.abspath(DATA_DIR))

    for table_name, csv_file in LOAD_ORDER:
        try:
            load_table(table_name, csv_file)
        except Exception as e:
            print(f"❌ Erreur sur {table_name}: {e}")

    print("\n🎉 Tous les fichiers traités !")

if __name__ == "__main__":
    main()