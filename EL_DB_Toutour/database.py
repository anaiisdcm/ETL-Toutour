from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://thomas:@localhost:5432/toutourBase"
#postgresql+psycopg2://<utilisateur>:<mot_de_passe>@<hôte>:<port>/<nom_de_la_base>
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()