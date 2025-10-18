import numpy as np
import numpy.random as rd
import pandas as pd


"""
This file contains function to clean pandas dataframe
"""

def clean_dog(df_dog):
    """
    Clean and validate dog data
    
    Args:
        df_dog (pandas.DataFrame): Raw dog data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned dog data
    """
    if df_dog.empty:
        print("⚠️  No dog data to clean")
        return df_dog
    
    print(f"🧹 Cleaning dog data...")
    print(f"Starting with {len(df_dog)} dogs")
    
    # Make a copy to avoid modifying the original
    df = df_dog.copy()


    #Remove dogs with missing ID, name or owner ID.
    df = df.dropna(subset=['dog_id','name','owner_id'])


    # Remove dogs with invalid weight
    # Weight cannot be over 150kg

    df = df.drop(df[df['weight'] > 150].index)
    
    # Remove dogs with invalid age
    # Weight cannot be older than 35 years old.
    df = df.drop(df[(df['birth_date'] < 1990)].index)

    # Remove dogs with invalid sportivity
    # Sportivity should be either 'Low', 'Medium' or 'High'.
    df = df.drop(df[~(df['athleticism'].isin(['Low', 'Medium', 'High']))].index)

    return df

def clean_proprietaire(df_proprietaire):
    """
    Clean and validate propriétaires data
    
    Args:
        df_propriétaire (pandas.DataFrame): Raw propriétaires data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned propriétaires data
    """
    if df_proprietaire.empty:
        print("⚠️  No propriétaires data to clean")
        return df_proprietaire
    
    print(f"🧹 Cleaning propriétaires data...")
    print(f"Starting with {len(df_proprietaire)} propriétaires")
    
    # Make a copy to avoid modifying the original
    df = df_proprietaire.copy()

    #Remove propriétaires with missing ID or name
    df = df.dropna(subset=['owner_id','last_name','first_name'])

    #Remove propriétaires with missing mail and phone number
    df = df.dropna(subset=['email','phone'], how='all')

    # Remove propriétaires with invalid e-mail
    # Keep only emails that contain exactly one '@' and at least one '.' before the '@'
    df = df[
        (df['email'].str.count('@') == 1) &
        (df['email'].str.contains('.', na=False)) &
        (df['email'].str.split('@').str[0].str.count('.') >= 1)
    ]
   
    # Remove propriétaires with invalid phone number
    # Phone number has to have 10 digits, and start with 06 or 07
    df = df[
        (df['phone'].str.isdigit()) &
        (df['phone'].str.len() == 10) &
        (df['phone'].str.startswith(('06', '07')))
    ]

    return df

def clean_promeneur(df_promeneur):
    """
    Clean and validate promeneurs data
    
    Args:
        df_promeneur (pandas.DataFrame): Raw promeneurs data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned promeneurs data
    """
    if df_promeneur.empty:
        print("⚠️  No promeneurs data to clean")
        return df_promeneur
    
    print(f"🧹 Cleaning promeneurs data...")
    print(f"Starting with {len(df_promeneur)} promeneurs")
    
    # Make a copy to avoid modifying the original
    df = df_promeneur.copy()

    #Remove promeneurs with missing ID or name
    df = df.dropna(subset=['id_promeneur','nom'])

    #Remove promeneurs with missing mail and phone number
    df = df.dropna(subset=['mail','phone'], how='all')

    # Remove promeneurs with invalid e-mail
    # Keep only emails that contain exactly one '@' and at least one '.' before the '@'
    df = df[
        (df['mail'].str.count('@') == 1) &
        (df['mail'].str.contains('.', na=False)) &
        (df['mail'].str.split('@').str[0].str.count('.') >= 1)
    ]
   
    # Remove promeneurs with invalid phone number
    # Phone number has to have 10 digits, and start with 06 or 07
    df = df[
        (df['phone'].str.isdigit()) &
        (df['phone'].str.len() == 10) &
        (df['phone'].str.startswith(('06', '07')))
    ]

    # Remove promeneurs with invalid age
    # Promeneur has to be born between 1965 and 2005
    df = df.drop(df[(df['date_naissance'] <= 1965) | (df['date_naissance'] >= 2005)].index)

    # Remove promeneurs with invalid RIB
    # RIB has to have 27 digits, and start with FR76.
    df = df[
        (df['rib'].str[:4].str.isdigit()) &
        (df['rib'].str.len() == 27) &
        (df['rib'].str.startswith(('FR76')))
    ]

    return df

def clean_promeneur_dispo(df_promeneur_dispo):
    """
    Clean and validate promeneurs availability data
    
    Args:
        df_promeneur_dispo (pandas.DataFrame): Raw promeneurs availability data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned promeneurs availability data
    """
    if df_promeneur_dispo.empty:
        print("⚠️  No promeneurs availability data to clean")
        return df_promeneur_dispo
    
    print(f"🧹 Cleaning promeneurs availability data...")
    print(f"Starting with {len(df_promeneur_dispo)} promeneurs available")
    
    # Make a copy to avoid modifying the original
    df = df_promeneur_dispo.copy()

    #Remove availabilities with missing promeneur ID or adresse
    df = df.dropna(subset=['id_promeneur','adresse'])

    #Try to convert availabilities where the starting and ending time are not on good format to a timestamp
    df["horodate_debut_disponibilite"] = pd.to_datetime(
        df["horodate_debut_disponibilite"], errors="coerce"
    )
    df["horodate_fin_disponibilite"] = pd.to_datetime(
        df["horodate_fin_disponibilite"], errors="coerce"
    )

    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["horodate_debut_disponibilite"])
    df = df.dropna(subset=["horodate_fin_disponibilite"])

    #Remove availabilities where starting time is after ending time
    df = df[
        (df['horodate_debut_disponibilite'] < df['horodate_fin_disponibilite'])
    ]

    return df

def clean_promenades_requests(df_promenades_requests):
    """
    Clean and validate promenades requests data
    
    Args:
        df_promenades_requests (pandas.DataFrame): Raw promenades requests  data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned promenades requests data
    """
    if df_promenades_requests.empty:
        print("⚠️  No promenades requests data to clean")
        return df_promenades_requests
    
    print(f"🧹 Cleaning promenades requests data...")
    print(f"Starting with {len(df_promenades_requests)} promenades requests")
    
    # Make a copy to avoid modifying the original
    df = df_promenades_requests.copy()

    #Remove availabilities with missing dog ID or promenade ID
    df = df.dropna(subset=['id_chien','id_promenade'])

    #Try to convert availabilities where the starting time are not on good format to a timestamp
    df["horodate_debut_ideal"] = pd.to_datetime(
        df["horodate_debut_ideal"], errors="coerce"
    )
    
    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["horodate_debut_ideal"])

    #Remove availabilities where duree is not a digit
    df = df[
        (df['duree_request'].str.isdigit())
    ]

    #Remove availabilities where distance is not a digit
    df = df[
        (df['distance_request'].str.isdigit())
    ]
    
    return df

def clean_promenades_passees(df_promenades_passees):
    """
    Clean and validate promenades passées data
    
    Args:
        df_promenades_passées (pandas.DataFrame): Raw promenades passées data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned promenades passées data
    """
    if df_promenades_passees.empty:
        print("⚠️  No promenades passées data to clean")
        return df_promenades_passees
    
    print(f"🧹 Cleaning promenades passées data...")
    print(f"Starting with {len(df_promenades_passees)} promenades passées")
    
    # Make a copy to avoid modifying the original
    df = df_promenades_passees.copy()

    #Remove promenades passées with missing promenade ID, promeneur ID or dog ID
    df = df.dropna(subset=['id_promenade','id_promeneur','id_chien'])

    #Try to convert promenades passées where the starting and ending time are not on good format to a timestamp
    df["horodate_debut"] = pd.to_datetime(
        df["horodate_debut"], errors="coerce"
    )
    df["horodate_fin"] = pd.to_datetime(
        df["horodate_fin"], errors="coerce"
    )

    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["horodate_debut"])
    df = df.dropna(subset=["horodate_fin"])

    #Remove promenades where starting time is after ending time
    df = df[
        (df['horodate_debut'] < df['horodate_fin'])
    ]

    #Remove promenades where distance is not a digit
    df = df[
        (df['distance'].str.isdigit())
    ]

    return df

def clean_note_promeneur(df_notes_promeneurs):
    """
    Clean and validate notes promeneurs data
    
    Args:
        df_notes_promeneurs (pandas.DataFrame): Raw notes promeneurs data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned notes promeneurs data
    """
    if df_notes_promeneurs.empty:
        print("⚠️  No notes promeneurs data to clean")
        return df_notes_promeneurs
    
    print(f"🧹 Cleaning notes promeneurs data...")
    print(f"Starting with {len(df_notes_promeneurs)} notes promeneurs")
    
    # Make a copy to avoid modifying the original
    df = df_notes_promeneurs.copy()

    #Remove notes promeneurs with missing promenade ID, promeneur ID or note
    df = df.dropna(subset=['id_promenade','id_promeneur','note'])

    #Keep notes where note is an integer between 1 and 5
    df = df[df['note'].between(1, 5)]

    return df 

def clean_note_chien(df_notes_chien):
    """
    Clean and validate notes chien data
    
    Args:
        df_notes_chien (pandas.DataFrame): Raw notes chien data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned notes chien data
    """
    if df_notes_chien.empty:
        print("⚠️  No notes chien data to clean")
        return df_notes_chien
    
    print(f"🧹 Cleaning notes chien data...")
    print(f"Starting with {len(df_notes_chien)} notes chien")
    
    # Make a copy to avoid modifying the original
    df = df_notes_chien.copy()

    #Remove notes chien with missing promenade ID, dog ID or note
    df = df.dropna(subset=['id_promenade','id_chien','note'])

    #Keep notes where note is an integer between 1 and 5
    df = df[df['note'].between(1, 5)]

    return df 

def clean_paiements_proprietaires(df_paiements_proprietaires):
    """
    Clean and validate paiements propriétaires data
    
    Args:
        df_paiements_propriétaires (pandas.DataFrame): Raw paiements propriétaires  data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned paiements propriétaires data
    """
    if df_paiements_proprietaires.empty:
        print("⚠️  No paiements propriétaires data to clean")
        return df_paiements_proprietaires
    
    print(f"🧹 Cleaning paiements propriétaires data...")
    print(f"Starting with {len(df_paiements_proprietaires)} paiements propriétaires")
    
    # Make a copy to avoid modifying the original
    df = df_paiements_proprietaires.copy()

    #Remove paiements  with missing promenade ID or montant
    df = df.dropna(subset=['montant','id_promenade'])

    #Try to convert times where the payment time is not on good format to a timestamp
    df["horodate_paiement"] = pd.to_datetime(
        df["horodate_paiement"], errors="coerce"
    )
    
    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["horodate_paiement"])

    #Keep payments where montant is an integer between 5 and 40
    df = df[df['montant'].between(5,40)]

    # Remove payments with invalid moyen
    # Moyen should be either 'CB', 'Paypal' or 'Virement'.
    df = df.drop(df[~(df['moyen_paiement'].isin(['CB', 'Paypal', 'Virement']))].index)

    # Remove payments with invalid status
    # Status should be either 'Payé', 'En attente' or 'Échoué'.
    df = df.drop(df[~(df['statut_paiement'].isin(['Payé', 'En attente', 'Échoué']))].index)
    
    return df

def clean_csv(path_csv, cleaning_function):
    df_to_clean = pd.read_csv(path_csv)
    df_cleaned = cleaning_function(df_to_clean)
    df_cleaned.to_csv(path_csv)
    return None


def clean_all():
    clean_csv("./data_out/df_Dog.csv", clean_dog)
    clean_csv("./data_out/df_Owner.csv", clean_proprietaire)
    clean_csv("./data_out/df_Walker.csv", clean_promeneur)
    clean_csv("./data_out/df_WalkerAvailability.csv", clean_promeneur_dispo)
    clean_csv("./data_out/df_WalksRequets.csv", clean_promenades_requests)
    clean_csv("./data_out/df_past_walks.csv", clean_promenades_passees)
    clean_csv("./data_out/df_WalkerReview.csv", clean_note_promeneur)
    clean_csv("./data_out/df_DogReview.csv", clean_note_chien)
    clean_csv("./data_out/df_OwnerPayment.csv", clean_paiements_proprietaires)


if __name__ == "__main__":
    clean_all()
