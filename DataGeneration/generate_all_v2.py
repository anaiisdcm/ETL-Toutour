import pandas as pd
import numpy as np
import numpy.random as nrd
import random as rd
import string




dog = True
propriétaire = True
promeneur = True
promeneur_dispo = True
promenade_passées = True
note_promeneur = True
paiements_propriétaires = True
promenade_requests = True
notes_chien = True


if dog :
    # load & diplay
    df_quaggle_dog = pd.read_csv("./data_in/dogs_dataset.csv")
    n_dog = len(df_quaggle_dog['Breed'])
    print(df_quaggle_dog.head())
    
    
    # init fields
    id_dog = np.arange(0, n_dog, 1)
    chip_number = np.zeros(n_dog, )
    owner_id = np.zeros(n_dog, )
    name = nrd.choice(["John", "Twingo", "Bertholet"], n_dog)
    weight = df_quaggle_dog['Weight (kg)']
    breed = df_quaggle_dog['Breed']
    photo = nrd.randint(0, 3, n_dog)
    birthdate = 2025 - np.round(df_quaggle_dog['Age (Years)'])
    optimal_tour_duration = np.floor(weight/3 + nrd.rand(n_dog)*weight/10)
    sportivity = nrd.choice(["High", "Medium", "Low"], n_dog)
    
    
    # file in fields & save
    df_dog = pd.DataFrame({'id_dog': id_dog,
                          'chip_number': chip_number,
                          'owner_id': owner_id,
                          'name': name,
                          'weight': weight,
                          'breed': breed,
                          'photo': photo,
                          'birthdate': birthdate,
                          'optimal_tour_duration': optimal_tour_duration,
                          'sportivity': sportivity
              })
    
    df_dog.to_csv("./data_out/df_dog.csv")


if propriétaire :
    # --- propriétaires 
    n_propriétaire = 100  # exemple: 100 propriétaires
    
    id_propriétaire = np.arange(0, n_propriétaire, 1)
    nom = rd.choices(["Martin", "Bernard", "Dubois", "Thomas", "Robert"], k=n_propriétaire)
    prenom = rd.choices(["Jean", "Marie", "Pierre", "Sophie", "Luc"], k=n_propriétaire)
    mail = [f"{p}.{n}@example.com".lower() for p, n in zip(prenom, nom)]
    phone = ["06" + "".join(rd.choices(string.digits, k=8)) for _ in range(n_propriétaire)]
    photo = nrd.randint(0, 5, n_propriétaire)
    bio = ["Bio de " + p + " " + n for p, n in zip(prenom, nom)]
    
    df_propriétaire = pd.DataFrame({
        'id_propriétaire': id_propriétaire,
        'nom': nom,
        'prenom': prenom,
        'mail': mail,
        'phone': phone,
        'photo': photo,
        'bio': bio
    })
    df_propriétaire.to_csv("./data_out/df_propriétaire.csv", index=False)



if promeneur :
    # --- promeneurs 
    n_promeneur = 50  # exemple: 50 promeneurs
    
    id_promeneur = np.arange(0, n_promeneur, 1)
    nom = rd.choices(["Dupont", "Lambert", "Petit", "Moreau", "Girard"], k=n_promeneur)
    prenom = rd.choices(["Nicolas", "Camille", "Julien", "Élodie", "Thomas"], k=n_promeneur)
    photo = nrd.randint(0, 5, n_promeneur)
    bio = ["Bio de " + p + " " + n for p, n in zip(prenom, nom)]
    profil_verifie = rd.choices([True, False], k=n_promeneur)
    mail = [f"{p}.{n}@promeneur.com".lower() for p, n in zip(prenom, nom)]
    phone = ["07" + "".join(rd.choices(string.digits, k=8)) for _ in range(n_promeneur)]
    date_naissance = [rd.randint(1965, 2005) for _ in range(n_promeneur)]
    rib = ["FR76" + "".join(rd.choices(string.digits, k=23)) for _ in range(n_promeneur)]
    
    df_promeneur = pd.DataFrame({
        'id_promeneur': id_promeneur,
        'nom': nom,
        'prenom': prenom,
        'photo': photo,
        'bio': bio,
        'profil_verifie': profil_verifie,
        'mail': mail,
        'phone': phone,
        'date_naissance': date_naissance,
        'rib': rib
    })
    df_promeneur.to_csv("./data_out/df_promeneur.csv", index=False)





if promeneur_dispo :
    # --- promeneur_dispo 
    n_dispo = 200  # exemple: 200 disponibilités
    
    id_promeneur = rd.choices(df_promeneur['id_promeneur'], k=n_dispo)
    adresse = rd.choices(["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux"], k=n_dispo)
    horodate_debut_disponibilite = pd.date_range(start="2025-10-01", periods=n_dispo, freq="H").tolist()
    horodate_fin_disponibilite = pd.date_range(start="2025-10-02", periods=n_dispo, freq="H").tolist()
    
    df_promeneur_dispo = pd.DataFrame({
        'id_promeneur': id_promeneur,
        'adresse': adresse,
        'horodate_debut_disponibilite': horodate_debut_disponibilite,
        'horodate_fin_disponibilite': horodate_fin_disponibilite
    })
    df_promeneur_dispo.to_csv("./data_out/df_promeneur_dispo.csv", index=False)


if promenade_requests :
    # --- Promenades_requests 
    n_request = 150
    
    id_chien = rd.choices(np.arange(0, n_dog, 1), k=n_request)  # suppose n_dog défini plus haut
    id_promenade = np.arange(0, n_request, 1)
    adresse = rd.choices(["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux"], k=n_request)
    horodate_debut_ideal = pd.date_range(start="2025-10-03", periods=n_request, freq="H").tolist()
    duree_request = [rd.randint(30, 120) if rd.random() > 0.5 else np.nan for _ in range(n_request)]
    distance_request = [rd.randint(1, 10) if rd.random() > 0.5 else np.nan for _ in range(n_request)]
    id_promeneur_favori = [rd.choice(df_promeneur['id_promeneur']) if rd.random() > 0.7 else np.nan for _ in range(n_request)]
    remuneration_predite = [rd.randint(10, 50) for _ in range(n_request)]
    
    df_promenades_requests = pd.DataFrame({
        'id_chien': id_chien,
        'id_promenade': id_promenade,
        'adresse': adresse,
        'horodate_debut_ideal': horodate_debut_ideal,
        'duree_request': duree_request,
        'distance_request': distance_request,
        'id_promeneur_favori': id_promeneur_favori,
        'remuneration_predite': remuneration_predite
    })
    df_promenades_requests.to_csv("./data_out/df_promenades_requests.csv", index=False)




if promenade_passées :
    # --- promenades_passées
    n_promenade = 100 
    
    id_promenade = np.arange(0, n_promenade, 1)
    id_chien = rd.choices(np.arange(0, n_dog, 1), k=n_promenade)
    id_promeneur = rd.choices(df_promeneur['id_promeneur'], k=n_promenade)
    distance = nrd.randint(1, 15, n_promenade)
    horodate_debut = pd.date_range(start="2025-09-01", periods=n_promenade, freq="H").tolist()
    horodate_fin = pd.date_range(start="2025-09-02", periods=n_promenade, freq="H").tolist()
    photo = nrd.randint(0, 5, n_promenade)
    avis_chien_id = [rd.choice([None, np.nan, rd.randint(0, 100)]) for _ in range(n_promenade)]
    avis_promeneur_id = [rd.choice([None, np.nan, rd.randint(0, 100)]) for _ in range(n_promenade)]
    
    df_promenades_passées = pd.DataFrame({
        'id_promenade': id_promenade,
        'id_chien': id_chien,
        'id_promeneur': id_promeneur,
        'distance': distance,
        'horodate_debut': horodate_debut,
        'horodate_fin': horodate_fin,
        'photo': photo,
        'avis_chien_id': avis_chien_id,
        'avis_promeneur_id': avis_promeneur_id
    })
    df_promenades_passées.to_csv("./data_out/df_promenades_passées.csv", index=False)



if note_promeneur :
    # --- notes_promeneurs
    n_notes_promeneur = 80 
    
    id_promenade = rd.choices(df_promenades_passées['id_promenade'], k=n_notes_promeneur)
    id_promeneur = rd.choices(df_promeneur['id_promeneur'], k=n_notes_promeneur)
    note = nrd.randint(1, 5, n_notes_promeneur)
    commentaire = ["Commentaire pour " + str(i) for i in range(n_notes_promeneur)]
    
    df_notes_promeneurs = pd.DataFrame({
        'id_promenade': id_promenade,
        'id_promeneur': id_promeneur,
        'note': note,
        'commentaire': commentaire
    })
    df_notes_promeneurs.to_csv("./data_out/df_notes_promeneurs.csv", index=False)

if notes_chien :
    # --- notes_chien 
    n_notes_chien = 80
    
    id_promenade = rd.choices(df_promenades_passées['id_promenade'], k=n_notes_chien)
    id_chien = rd.choices(np.arange(0, n_dog, 1), k=n_notes_chien)
    note = nrd.randint(1, 5, n_notes_chien)
    commentaire = ["Commentaire pour chien " + str(i) for i in range(n_notes_chien)]
    
    df_notes_chien = pd.DataFrame({
        'id_promenade': id_promenade,
        'id_chien': id_chien,
        'note': note,
        'commentaire': commentaire
    })
    df_notes_chien.to_csv("./data_out/df_notes_chien.csv", index=False)



if paiements_propriétaires :
    # --- paiements_propriétaires 
    n_paiements = 90
    
    id_promenade = rd.choices(df_promenades_passées['id_promenade'], k=n_paiements)
    montant = [rd.randint(5, 40) for _ in range(n_paiements)]
    horodate_paiement = pd.date_range(start="2025-09-10", periods=n_paiements, freq="H").tolist()
    moyen_paiement = rd.choices(["CB", "Paypal", "Virement"], k=n_paiements)
    statut_paiement = rd.choices(["Payé", "En attente", "Échoué"], k=n_paiements)
    
    df_paiements_propriétaires = pd.DataFrame({
        'id_promenade': id_promenade,
        'montant': montant,
        'horodate_paiement': horodate_paiement,
        'moyen_paiement': moyen_paiement,
        'statut_paiement': statut_paiement
    })
    df_paiements_propriétaires.to_csv("./data_out/df_paiements_propriétaires.csv", index=False)
