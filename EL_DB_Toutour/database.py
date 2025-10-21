from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

DATABASE_URL = "postgresql+psycopg2://usertoutour:mdp@localhost:5432/toutourBase"
#postgresql+psycopg2://<utilisateur>:<mot_de_passe>@<hôte>:<port>/<nom_de_la_base>
#Possibilité de créer un utilisateur dans PostgreSQL pour ce projet :
#sudo -u postgres psql (bash)
#CREATE ROLE usertoutour WITH LOGIN PASSWORD 'mdp'; (SQL)
#ALTER ROLE usertoutour WITH SUPERUSER; (SQL)
#\du --pour vérifier les droits des utilisateurs postgres (SQL)
# Et activer postgresql avec :
# sudo service postgresql start
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

if not database_exists(engine.url):
    create_database(engine.url)
    print("✅ Base de données 'toutourBase' créée.")
else:
    print("✅ Base déjà existante.")