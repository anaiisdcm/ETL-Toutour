from EL_DB_Toutour.database import engine, Base
from EL_DB_Toutour import models
from sqlalchemy import text

def init_db():
    print("⚠️  ATTENTION : cette opération va SUPPRIMER toutes les tables de la base de données actuelle !")
    print(f"📂 Base de données ciblée : {engine.url.database}")
    print(f"👤 Utilisateur : {engine.url.username or '(aucun spécifié)'}")
    print(f"🖥️ Hôte : {engine.url.host}:{engine.url.port}")
    confirmation = input("👉 Es-tu sûr de vouloir continuer ? (tape 'Yes' pour confirmer) : ")

    if confirmation.lower() != "yes":
        print("❌ Opération annulée.")
        return

    with engine.connect() as conn:
        print("\n🧨 Suppression **complète** de toutes les tables (y compris parasites)...")
        # Vide tout le schéma public
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()
        print("✅ Schéma PostgreSQL entièrement réinitialisé.")

    print("\n🛠️ Création des nouvelles tables ORM...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès !")