import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from EL_DB_Toutour.database import engine, Base

# # --- Données simulées ---
# df_propriétaire = pd.read_csv('./data_test_hot_dog/df_proprietaire.csv', delimiter=';')

# df_dog = pd.read_csv('./data_test_hot_dog/df_dog.csv', delimiter=';')

# df_promenades_passees = pd.read_csv('./data_test_hot_dog/df_promenades_passees.csv', delimiter=';')

# df_notes_chien = pd.read_csv('./data_test_hot_dog/df_notes_chien.csv', delimiter=';')

# df_notes_promeneurs =  pd.read_csv('./data_test_hot_dog/df_notes_promeneurs.csv', delimiter=';')

# df_promeneurs = pd.read_csv('./data_test_hot_dog/df_promeneurs.csv', delimiter=';')


# --- Configuration de la page ---
st.set_page_config(page_title="Hot dog", layout="wide")
st.logo('./HotDog/toutour.png')
st.title(f"Hot dog {datetime.now().year} 🐾")

# --- Gestion de l'état de session ---
if "connected_owner" not in st.session_state:
    st.session_state.connected_owner = None
if "selected_dog" not in st.session_state:
    st.session_state.selected_dog = None

# --- Fonction de réinitialisation (changement de chien sélectionné) ---
def reset_dog():
    st.session_state.selected_dog = None

# --- Fonction de réinitialisation (déconnexion) ---
def reset_session():
    st.session_state.connected_owner = None
    st.session_state.selected_dog = None

# --- Étape 1 : Connexion (sélection du propriétaire) ---
if not st.session_state.connected_owner:
    st.header("Connexion propriétaire")
    query_owner = "SELECT owner_id, last_name, first_name, CONCAT(last_name, ' ', first_name) AS full_name FROM owners;"
    df_owner = pd.read_sql(query_owner, con=engine)
    nom_prenom_proprietaire = st.selectbox("Sélectionnez votre nom :", [""] + list(df_owner['full_name']))
    id_proprietaire = df_owner[df_owner[['last_name', 'first_name']].agg(' '.join, axis=1)==nom_prenom_proprietaire]['owner_id'].iat[0] if nom_prenom_proprietaire!='' else ''
    if id_proprietaire and st.button("Se connecter"):
        st.session_state.connected_owner = id_proprietaire
        st.rerun()

# --- Étape 2 : Sélection du chien ---
elif st.session_state.connected_owner and not st.session_state.selected_dog:
    st.button("Déconnexion", on_click=reset_session)
    query_owner_dogs = f"SELECT dog_id, name FROM dogs WHERE owner_id='{st.session_state.connected_owner}';"
    df_owner_dogs = pd.read_sql(query_owner_dogs, con=engine)
    query_owner_name = f"SELECT first_name FROM owners WHERE owner_id='{st.session_state.connected_owner}';"
    df_owner = pd.read_sql(query_owner_name, con=engine)
    st.success(f"Bienvenue {df_owner['first_name'].iat[0]} 👋")
    
    nom_chien = st.selectbox("Sélectionnez votre chien :", [""] + list(df_owner_dogs['name']))
    # f SELECT dog_id FROM Dog WHERE owner_id={st.session_state.connected_owner} AND name={nom_chien}
    id_chien = df_owner_dogs[df_owner_dogs['name']==nom_chien]['dog_id'].iat[0] if nom_chien!='' else ''
    if id_chien and st.button("Valider"):
        st.session_state.selected_dog = id_chien
        st.rerun()

# --- Étape 3 : Tableau de bord du chien ---
elif st.session_state.selected_dog:
    proprietaire = st.session_state.connected_owner
    chien = st.session_state.selected_dog

    col1, col2, = st.columns(2)
    with col1:
        st.button("Déconnexion", on_click=reset_session)
    with col2:
        st.button("Changer de chien", on_click=reset_dog)

    query_owner_name = f"SELECT first_name, last_name FROM owners WHERE owner_id='{st.session_state.connected_owner}';"
    df_owner = pd.read_sql(query_owner_name, con=engine)
    st.success(f"Connecté en tant que {df_owner[['first_name', 'last_name']].agg(' '.join, axis=1).iat[0]}")

    query_dog_name = f"SELECT name FROM dogs WHERE owner_id='{st.session_state.connected_owner}' AND dog_id='{st.session_state.selected_dog}';"
    df_dog_name = pd.read_sql(query_dog_name, con=engine)
    st.subheader(f"Les promenades de {df_dog_name['name'].iat[0]} en {datetime.now().year}🐕")

    query_past_walks = f"SELECT walk_id, walker_id, distance, start_datetime, end_datetime, dog_review_id, walker_review_id FROM past_walks WHERE dog_id='{st.session_state.selected_dog}' AND EXTRACT(YEAR FROM start_datetime) ={datetime.now().year};"
    df_past_walks = pd.read_sql(query_past_walks, con=engine)
    
    # df_promenades_notees_dog = pd.merge(df_promenades_passees_dog, df_notes_chien.drop('id_dog', axis=1), on='id_promenade')

    # df_promeneurs_notes_dog = pd.merge(df_promenades_passees_dog, df_notes_promeneurs.drop('id_promeneur', axis=1), on='id_promenade')

    query_dog_reviews = f"SELECT rating, comment FROM dog_reviews JOIN past_walks ON dog_reviews.walk_id=past_walks.walk_id WHERE dog_reviews.dog_id='{st.session_state.selected_dog}' AND EXTRACT(YEAR FROM past_walks.start_datetime) ={datetime.now().year};"
    df_dog_reviews = pd.read_sql(query_dog_reviews, con=engine)
 
    query_walk_reviews = f"SELECT rating, comment FROM walker_reviews JOIN past_walks ON walker_reviews.walk_id=past_walks.walk_id WHERE past_walks.dog_id='{st.session_state.selected_dog}' AND EXTRACT(YEAR FROM past_walks.start_datetime) ={datetime.now().year};"
    df_walk_reviews = pd.read_sql(query_walk_reviews, con=engine)


    if not df_past_walks.empty :
        # probalement des bugs ici
        # -----------------------------
        # INDICATEURS CLÉS
        # -----------------------------
        duree_totale = (df_past_walks['end_datetime'] - df_past_walks['start_datetime']).sum()
        distance_totale = df_past_walks['distance'].sum()

        promenade_pref = df_walk_reviews.loc[df_walk_reviews["rating"].idxmax()]
        promenade_plus_longue = df_past_walks.loc[df_past_walks['distance'].idxmax()]
        # Probablement un bug ici avec idxmax
        promeneur_pref = df_walk_reviews.groupby("walker_id")["rating"].mean().idxmax()
        query_best_walker = f"SELECT first_name, last_name FROM walkers WHERE dog_reviews.dog_id='{promeneur_pref}';"
        df_best_walker = pd.read_sql(query_best_walker, con=engine)

        horaire_frequent = df_past_walks['start_datetime'].dt.hour.mode().iat[0]


        # -----------------------------
        # AFFICHAGE DES INDICATEURS
        # -----------------------------
        st.write("### ")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Durée cumulée de promenade", f"{duree_totale.days:.0f} jours {duree_totale.seconds // 3600:.0f} h {duree_totale.seconds // 60 % 60:.0f} min")
        with col2:
            st.metric("Distance totale parcourue", f"{distance_totale:.1f} km")
        with col3:
            st.metric("Horaire de balade préféré", f"{horaire_frequent}h")

        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Promeneur préféré", df_best_walker[['first_name', 'last_name']].agg(' '.join, axis=1).iat[0])
        with col5:
            st.metric("Promenade la plus longue", f"{promenade_plus_longue['distance']:.1f} km ({promenade_plus_longue['start_datetime'].strftime('%d/%m')})")
        with col6:
            st.metric(f"Promenade préférée de {df_dog_name['name'].iat[0]}", f"{promenade_pref['rating']} ⭐ ({promenade_pref['start_datetime'].strftime('%d/%m')})")

        # -----------------------------
        # COMMENTAIRES POSITIFS
        # -----------------------------

        bons_commentaires = df_dog_reviews[df_dog_reviews["rating"] >= 4]
        if not bons_commentaires.empty:
            st.write("### Votre chien est apprécié !")
            displayed_comments = 0
            for _, row in bons_commentaires.iterrows():
                if displayed_comments < 5 and not(pd.isnull(row['comment'])):
                    st.badge(f"★ {row['rating']} — {row['comment']}")
                    displayed_comments +=1

        # -----------------------------
        # GRAPHIQUES DYNAMIQUES
        # -----------------------------
        st.write("### Répartition des distances de balade avec Toutour")
        df_monthly = df_past_walks.groupby(df_past_walks['start_datetime'].dt.month)[["distance"]].sum()
        df_monthly.index = [datetime(datetime.now().year, m, 1).strftime("%b") for m in df_monthly.index]
        st.line_chart(df_monthly)
    else :
        st.badge("Pas de balade réalisée sur Toutour cette année :(")

