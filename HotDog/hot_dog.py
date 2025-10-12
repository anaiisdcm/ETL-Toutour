import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# --- Données simulées ---
df_propriétaire = pd.read_csv('./data/df_proprietaire.csv', delimiter=';')

df_dog = pd.read_csv('./data/df_dog.csv', delimiter=';')

df_promenades_passees = pd.read_csv('./data/df_promenades_passees.csv', delimiter=';')

df_notes_chien = pd.read_csv('./data/df_notes_chien.csv', delimiter=';')

df_notes_promeneurs =  pd.read_csv('./data/df_notes_promeneurs.csv', delimiter=';')

df_promeneurs = pd.read_csv('./data/df_promeneurs.csv', delimiter=';')


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
    nom_prenom_proprietaire = st.selectbox("Sélectionnez votre nom :", [""] + list(df_propriétaire[['nom', 'prenom']].agg(' '.join, axis=1)))
    id_proprietaire = df_propriétaire[df_propriétaire[['nom', 'prenom']].agg(' '.join, axis=1)==nom_prenom_proprietaire]['id_propriétaire'].iat[0] if nom_prenom_proprietaire!='' else ''
    if id_proprietaire and st.button("Se connecter"):
        st.session_state.connected_owner = id_proprietaire
        st.rerun()

# --- Étape 2 : Sélection du chien ---
elif st.session_state.connected_owner and not st.session_state.selected_dog:
    st.button("Déconnexion", on_click=reset_session)
    st.success(f"Bienvenue {df_propriétaire[df_propriétaire['id_propriétaire'] == st.session_state.connected_owner]['prenom'].iat[0]} 👋")
    
    # SELECT * FROM dog WHERE owner_id=id_proprietaire
    chiens_possedes = df_dog[df_dog['owner_id']==st.session_state.connected_owner]['name']
    nom_chien = st.selectbox("Sélectionnez votre chien :", [""] + list(chiens_possedes))
    id_chien = df_dog[df_dog['name']==nom_chien]['id_dog'].iat[0] if nom_chien!='' else ''
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

    st.success(f"Connecté en tant que {df_propriétaire[df_propriétaire['id_propriétaire']==proprietaire][['prenom', 'nom']].agg(' '.join, axis=1).iat[0]}")



    st.subheader(f"Les promenades de {df_dog[df_dog['id_dog']==chien]['name'].iat[0]} en {datetime.now().year}🐕")

    # SELECT * FROM promenades_passees WHERE id_dog=chien AND YEAR(horodate_debut)=2025
    df_promenades_passees_dog = df_promenades_passees[df_promenades_passees['id_dog']==chien]
    df_promenades_passees_dog['horodate_debut'] = pd.to_datetime(df_promenades_passees_dog['horodate_debut'])
    df_promenades_passees_dog['horodate_fin'] = pd.to_datetime(df_promenades_passees_dog['horodate_fin'])
    df_promenades_passees_dog = df_promenades_passees_dog[df_promenades_passees_dog['horodate_debut'].dt.year==datetime.now().year]

    df_promenades_notees_dog = pd.merge(df_promenades_passees_dog, df_notes_chien.drop('id_dog', axis=1), on='id_promenade')

    df_promeneurs_notes_dog = pd.merge(df_promenades_passees_dog, df_notes_promeneurs.drop('id_promeneur', axis=1), on='id_promenade')

    if not df_promenades_passees_dog.empty :
        # -----------------------------
        # INDICATEURS CLÉS
        # -----------------------------
        duree_totale = (df_promenades_passees_dog['horodate_fin'] - df_promenades_passees_dog['horodate_debut']).sum()
        distance_totale = df_promenades_passees_dog['distance'].sum()

        promenade_pref = df_promenades_notees_dog.loc[df_promenades_notees_dog["note"].idxmax()]
        promenade_plus_longue = df_promenades_passees_dog.loc[df_promenades_passees_dog['distance'].idxmax()]
        promeneur_pref = df_promeneurs_notes_dog.groupby("id_promeneur")["note"].mean().idxmax()
        horaire_frequent = df_promenades_passees_dog['horodate_debut'].dt.hour.mode().iat[0]


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
            st.metric("Promeneur préféré", df_promeneurs[df_promeneurs['id_promeneur']==promeneur_pref][['prenom', 'nom']].agg(' '.join, axis=1).iat[0])
        with col5:
            st.metric("Promenade la plus longue", f"{promenade_plus_longue['distance']:.1f} km ({promenade_plus_longue['horodate_debut'].strftime('%d/%m')})")
        with col6:
            st.metric(f"Promenade préférée de {df_dog[df_dog['id_dog']==chien]['name'].iat[0]}", f"{promenade_pref['note']} ⭐ ({promenade_pref['horodate_debut'].strftime('%d/%m')})")

        # -----------------------------
        # COMMENTAIRES POSITIFS
        # -----------------------------

        bons_commentaires = df_promenades_notees_dog[df_promenades_notees_dog["note"] >= 4]
        if not bons_commentaires.empty:
            st.write("### Votre chien est apprécié !")
            displayed_comments = 0
            for _, row in bons_commentaires.iterrows():
                if displayed_comments < 5 and not(pd.isnull(row['commentaire'])):
                    st.badge(f"★ {row['note']} — {row['commentaire']}")
                    displayed_comments +=1

        # -----------------------------
        # GRAPHIQUES DYNAMIQUES
        # -----------------------------
        st.write("### Répartition des distances de balade avec Toutour")
        df_monthly = df_promenades_passees_dog.groupby(df_promenades_passees_dog['horodate_debut'].dt.month)[["distance"]].sum()
        df_monthly.index = [datetime(datetime.now().year, m, 1).strftime("%b") for m in df_monthly.index]
        st.line_chart(df_monthly)

