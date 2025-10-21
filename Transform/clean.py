import numpy as np
import numpy.random as rd
import pandas as pd


"""
This file contains function to clean pandas dataframe
"""

def clean_dog(dogs):
    """
    Clean and validate dog data
    
    Args:
        dogs (pandas.DataFrame): Raw dog data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned dog data
    """
    if dogs.empty:
        print("⚠️  No dog data to clean")
        return dogs
    
    print(f"🧹 Cleaning dog data...")
    print(f"Starting with {len(dogs)} dogs")
    
    # Make a copy to avoid modifying the original
    df = dogs.copy()

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


def clean_owner(owners):
    """
    Clean and validate owners data
    
    Args:
        owners (pandas.DataFrame): Raw owners data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned owners data
    """
    if owners.empty:
        print("⚠️  No owners data to clean")
        return owners
    
    print(f"🧹 Cleaning owners data...")
    print(f"Starting with {len(owners)} owners")
    
    # Make a copy to avoid modifying the original
    df = owners.copy()

    #Remove owners with missing ID or name
    df = df.dropna(subset=['owner_id','last_name'])

    #Remove owners with missing mail and phone number
    df = df.dropna(subset=['email','phone'], how='all')

    # Remove owners with invalid e-mail
    # Keep only emails that contain exactly one '@' and at least one '.' before the '@'
    df = df[
        (df['email'].str.count('@') == 1) &
        (df['email'].str.contains('.', na=False)) &
        (df['email'].str.split('@').str[0].str.count('.') >= 1)
    ]
   
    # Remove owners with invalid phone number
    # Phone number has to have 10 digits, and start with 06 or 07
    df['phone'] = df['phone'].astype(str)
    df = df[
        (df['phone'].str.isdigit()) &
        (df['phone'].str.len() == 10) &
        (df['phone'].str.startswith(('06', '07')))
    ]

    return df

def clean_walker(walkers):
    """
    Clean and validate walkers data
    
    Args:
        walkers (pandas.DataFrame): Raw walkers data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned walkers data
    """
    if walkers.empty:
        print("⚠️  No walkers data to clean")
        return walkers
    
    print(f"🧹 Cleaning walkers data...")
    print(f"Starting with {len(walkers)} walkers")
    
    # Make a copy to avoid modifying the original
    df = walkers.copy()

    #Remove walkers with missing ID or name
    df = df.dropna(subset=['walker_id','last_name'])

    #Remove walkers with missing mail and phone number
    df = df.dropna(subset=['email','phone'], how='all')

    # Remove walkers with invalid e-mail
    # Keep only emails that contain exactly one '@' and at least one '.' before the '@'
    df = df[
        (df['email'].str.count('@') == 1) &
        (df['email'].str.contains('.', na=False)) &
        (df['email'].str.split('@').str[0].str.count('.') >= 1)
    ]
   
    # Remove walkers with invalid phone number
    # Phone number has to have 10 digits, and start with 06 or 07
    df['phone'] = df['phone'].astype(str)
    df = df[
        (df['phone'].str.isdigit()) &
        (df['phone'].str.len() == 10) &
        (df['phone'].str.startswith(('06', '07')))
    ]

    # Remove walkers with invalid age
    # walker has to be born between 1965 and 2005
    df = df.drop(df[(df['birth_date'] <= 1965) | (df['birth_date'] >= 2005)].index)

    # Remove walkers with invalid RIB
    # RIB has to have 27 digits, and start with FR76.
    df = df[
        (df['rib'].str[:4].str.isdigit()) &
        (df['rib'].str.len() == 27) &
        (df['rib'].str.startswith(('FR76')))
    ]

    return df

def clean_walker_availability(walker_availabilities):
    """
    Clean and validate walkers availability data
    
    Args:
        walker_availabilities (pandas.DataFrame): Raw walkers availability data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned walkers availability data
    """
    if walker_availabilities.empty:
        print("⚠️  No walkers availability data to clean")
        return walker_availabilities
    
    print(f"🧹 Cleaning walkers availability data...")
    print(f"Starting with {len(walker_availabilities)} walkers available")
    
    # Make a copy to avoid modifying the original
    df = walker_availabilities.copy()

    #Remove availabilities with missing walker ID or adresse
    df = df.dropna(subset=['walker_id','address'])

    #Try to convert availabilities where the starting and ending time are not on good format to a timestamp
    df["start_datetime"] = pd.to_datetime(
        df["start_datetime"], errors="coerce"
    )
    df["end_datetime"] = pd.to_datetime(
        df["end_datetime"], errors="coerce"
    )

    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["start_datetime"])
    df = df.dropna(subset=["end_datetime"])

    #Remove availabilities where starting time is after ending time
    df = df[
        (df['start_datetime'] < df['end_datetime'])
    ]

    return df

def clean_walk_requests(walk_requests):
    """
    Clean and validate walks requests data
    
    Args:
        walk_requests (pandas.DataFrame): Raw walks requests  data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned walks requests data
    """
    if walk_requests.empty:
        print("⚠️  No walks requests data to clean")
        return walk_requests
    
    print(f"🧹 Cleaning walks requests data...")
    print(f"Starting with {len(walk_requests)} walks requests")
    
    # Make a copy to avoid modifying the original
    df = walk_requests.copy()

    #Remove availabilities with missing dog ID or walk ID
    df = df.dropna(subset=['dog_id','walk_id'])

    #Try to convert availabilities where the starting time are not on good format to a timestamp
    df["ideal_start_datetime"] = pd.to_datetime(
        df["ideal_start_datetime"], errors="coerce"
    )
    
    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["ideal_start_datetime"])

    #Remove availabilities where duration is not a int or a float
    df = df[df['duration_request'].apply(lambda x: isinstance(x, (int, float)))]


    #Remove availabilities where distance is not a int or a float
    df = df[df['distance_request'].apply(lambda x: isinstance(x, (int, float)))]
    
    return df

def clean_past_walks(past_walks):
    """
    Clean and validate past walks data
    
    Args:
        past_walks (pandas.DataFrame): Raw past walks data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned past walks data
    """
    if past_walks.empty:
        print("⚠️  No past walks data to clean")
        return past_walks
    
    print(f"🧹 Cleaning past walks data...")
    print(f"Starting with {len(past_walks)} past walks")
    
    # Make a copy to avoid modifying the original
    df = past_walks.copy()

    #Remove past walks with missing walk ID, walker ID or dog ID
    df = df.dropna(subset=['walk_id','walker_id','dog_id'])

    #Try to convert walks passées where the starting and ending time are not on good format to a timestamp
    df["start_datetime"] = pd.to_datetime(
        df["start_datetime"], errors="coerce"
    )
    df["end_datetime"] = pd.to_datetime(
        df["end_datetime"], errors="coerce"
    )

    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["start_datetime"])
    df = df.dropna(subset=["end_datetime"])

    #Remove walks where starting time is after ending time
    df = df[
        (df['start_datetime'] < df['end_datetime'])
    ]

    #Remove walks where distance is not a number
    df = df[pd.to_numeric(df['distance'], errors='coerce').notna()]


    return df

def clean_walker_review(walker_reviews):
    """
    Clean and validate walker reviews data
    
    Args:
        walker_reviews (pandas.DataFrame): Raw walker reviews data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned walker reviews data
    """
    if walker_reviews.empty:
        print("⚠️  No walker reviews data to clean")
        return walker_reviews
    
    print(f"🧹 Cleaning walker reviews data...")
    print(f"Starting with {len(walker_reviews)} walker reviews")
    
    # Make a copy to avoid modifying the original
    df = walker_reviews.copy()

    #Remove walker reviews with missing review ID, walk ID, walker ID or rating
    df = df.dropna(subset=['review_id', 'walk_id','walker_id','rating'])

    #Keep ratings where rating is an integer between 1 and 5
    df = df[df['rating'].between(1, 5)]

    return df 

def clean_dog_review(dog_reviews):
    """
    Clean and validate dog reviews data
    
    Args:
        dog_reviews (pandas.DataFrame): Raw dog reviews data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned dog reviews data
    """
    if dog_reviews.empty:
        print("⚠️  No dog reviews data to clean")
        return dog_reviews
    
    print(f"🧹 Cleaning dog reviews data...")
    print(f"Starting with {len(dog_reviews)} dog reviews")
    
    # Make a copy to avoid modifying the original
    df = dog_reviews.copy()

    #Remove dog reviews with missing review ID, walk ID, dog ID or rating
    df = df.dropna(subset=['review_id','walk_id','dog_id','rating'])

    #Keep ratings where rating is an integer between 1 and 5
    df = df[df['rating'].between(1, 5)]

    return df 

def clean_owner_payments(owner_payments):
    """
    Clean and validate owner payments data
    
    Args:
        owner_payments (pandas.DataFrame): Raw owner payments  data from CSV
        
    Returns:
        pandas.DataFrame: Cleaned owner payments data
    """
    if owner_payments.empty:
        print("⚠️  No owner payments data to clean")
        return owner_payments
    
    print(f"🧹 Cleaning owner payments data...")
    print(f"Starting with {len(owner_payments)} owner payments")
    
    # Make a copy to avoid modifying the original
    df = owner_payments.copy()

    #Remove paiements  with missing payment ID, walk ID or amount
    df = df.dropna(subset=['payment_id','amount','walk_id'])

    #Try to convert times where the payment time is not on good format to a timestamp
    df["payment_datetime"] = pd.to_datetime(
        df["payment_datetime"], errors="coerce"
    )
    
    # Remove rows where conversion was unsuccessful
    df = df.dropna(subset=["payment_datetime"])

    #Keep payments where amount is an integer between 5 and 40
    df = df[df['amount'].between(5,40)]

    # Remove payments with invalid method
    # Method should be either 'CB', 'Paypal' or 'Virement'.
    df = df.drop(df[~(df['payment_method'].isin(['CB', 'Paypal', 'Virement']))].index)

    # Remove payments with invalid status
    # Status should be either 'Payé', 'En attente' or 'Échoué'.
    df = df.drop(df[~(df['payment_status'].isin(['Payé', 'En attente', 'Échoué']))].index)
    
    return df

def clean_csv(path_csv, cleaning_function):
    df_to_clean = pd.read_csv(path_csv)
    df_cleaned = cleaning_function(df_to_clean)
    df_cleaned.to_csv(path_csv)
    return None


def clean_all():
    clean_csv("./data_out/df_Dog.csv", clean_dog)
    clean_csv("./data_out/df_Owner.csv", clean_owner)
    clean_csv("./data_out/df_Walker.csv", clean_walker)
    clean_csv("./data_out/df_WalkerAvailability.csv", clean_walker_availability)
    clean_csv("./data_out/df_WalksRequests.csv", clean_walk_requests)
    clean_csv("./data_out/df_past_walks.csv", clean_past_walks)
    clean_csv("./data_out/df_WalkerReview.csv", clean_walker_review)
    clean_csv("./data_out/df_DogReview.csv", clean_dog_review)
    clean_csv("./data_out/df_OwnerPayment.csv", clean_owner_payments)


if __name__ == "__main__":
    clean_all()
