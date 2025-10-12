from .database import engine, Base
from . import models

def init_db():
    # Crée toutes les tables définies dans les modèles
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée !")

if __name__ == "__main__":
    init_db()