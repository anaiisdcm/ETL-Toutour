from .database import engine, Base
from . import models

def init_db():
    print("⚠️  ATTENTION : cette opération va SUPPRIMER toutes les tables de la base de données actuelle !")
    print(f"📂 Base de données ciblée : {engine.url.database}")
    print(f"👤 Utilisateur : {engine.url.username or '(aucun spécifié)'}")
    print(f"🖥️ Hôte : {engine.url.host}:{engine.url.port}")
    confirmation = input("👉 Es-tu sûr de vouloir continuer ? (tape 'OUI' pour confirmer) : ")

    if confirmation != "OUI":
        print("❌ Opération annulée.")
        return

    print("\n🧹 Suppression de toutes les tables existantes...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Toutes les tables ont été supprimées.")

    print("\n🛠️ Création des nouvelles tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_db()