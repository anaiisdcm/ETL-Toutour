import numpy as np
import pandas as pd
import os


"""
Data cleaning module for dog walking data.
Now includes relational cleaning across tables.
"""

# ============================================================
# 🧹 FONCTIONS DE NETTOYAGE INDIVIDUEL (inchangées ou corrigées)
# ============================================================

def clean_dog(dogs):
    if dogs.empty:
        print("⚠️  No dog data to clean")
        return dogs
    
    print(f"🧹 Cleaning dog data... ({len(dogs)} dogs)")
    df = dogs.copy()

    df = df.dropna(subset=['dog_id', 'name', 'owner_id'])
    df = df.drop(df[df['weight'] > 150].index)
    df = df.drop(df[df['birth_date'] < 1990].index)
    df = df[df['athleticism'].between(0, 10)]
    return df


def clean_owner(owners):
    if owners.empty:
        print("⚠️  No owners data to clean")
        return owners
    
    print(f"🧹 Cleaning owners data... ({len(owners)} owners)")
    df = owners.copy()

    df = df.dropna(subset=['owner_id', 'last_name', 'first_name'])
    df = df.dropna(subset=['email', 'phone'], how='all')

    df = df[
        (df['email'].str.count('@') == 1) &
        (df['email'].str.contains('.', na=False))
    ]

    df['phone'] = df['phone'].astype(str)
    df = df[
        (df['phone'].str.isdigit()) &
        (df['phone'].str.len() == 10) &
        (df['phone'].str.startswith(('06', '07')))
    ]
    return df


def clean_walker(walkers):
    if walkers.empty:
        print("⚠️  No walkers data to clean")
        return walkers
    
    print(f"🧹 Cleaning walkers data... ({len(walkers)} walkers)")
    df = walkers.copy()

    df = df.dropna(subset=['walker_id', 'last_name', 'first_name'])
    df = df.dropna(subset=['email', 'phone'], how='all')

    df = df[
        (df['email'].str.count('@') == 1) &
        (df['email'].str.contains('.', na=False))
    ]

    df['phone'] = df['phone'].astype(str)
    df = df[
        (df['phone'].str.isdigit()) &
        (df['phone'].str.len() == 10) &
        (df['phone'].str.startswith(('06', '07')))
    ]

    df = df.drop(df[(np.floor(df['birth_date']) <= 1965) | (np.floor(df['birth_date']) >= 2005)].index)
    df = df[
        (df['rib'].str[4:].str.isdigit()) &
        (df['rib'].str.len() == 27) &
        (df['rib'].str.startswith(('FR76')))
    ]
    return df


def clean_walker_availability(walker_availabilities):
    if walker_availabilities.empty:
        print("⚠️  No walkers availability data to clean")
        return walker_availabilities
    
    print(f"🧹 Cleaning walkers availability data... ({len(walker_availabilities)} rows)")
    df = walker_availabilities.copy()

    df = df.dropna(subset=['walker_id', 'address'])
    df["start_datetime"] = pd.to_datetime(df["start_datetime"], errors="coerce")
    df["end_datetime"] = pd.to_datetime(df["end_datetime"], errors="coerce")
    df = df.dropna(subset=["start_datetime", "end_datetime"])
    df = df[df['start_datetime'] < df['end_datetime']]
    return df


def clean_walk_requests(walk_requests):
    if walk_requests.empty:
        print("⚠️  No walk requests data to clean")
        return walk_requests
    
    print(f"🧹 Cleaning walk requests data... ({len(walk_requests)} rows)")
    df = walk_requests.copy()

    df = df.dropna(subset=['dog_id', 'walk_id'])
    df["ideal_start_datetime"] = pd.to_datetime(df["ideal_start_datetime"], errors="coerce")
    df = df.dropna(subset=["ideal_start_datetime"])
    df = df[df['duration_request'].apply(lambda x: isinstance(x, (int, float)))]
    df = df[df['distance_request'].apply(lambda x: isinstance(x, (int, float)))]
    return df


def clean_past_walks(past_walks):
    if past_walks.empty:
        print("⚠️  No past walks data to clean")
        return past_walks
    
    print(f"🧹 Cleaning past walks data... ({len(past_walks)} rows)")
    df = past_walks.copy()

    df = df.dropna(subset=['walk_id', 'walker_id', 'dog_id'])
    df["start_datetime"] = pd.to_datetime(df["start_datetime"], errors="coerce")
    df["end_datetime"] = pd.to_datetime(df["end_datetime"], errors="coerce")
    df = df.dropna(subset=["start_datetime", "end_datetime"])
    df = df[df['start_datetime'] < df['end_datetime']]
    df = df[pd.to_numeric(df['distance'], errors='coerce').notna()]
    return df


def clean_walker_review(walker_reviews):
    if walker_reviews.empty:
        print("⚠️  No walker reviews data to clean")
        return walker_reviews
    
    print(f"🧹 Cleaning walker reviews data... ({len(walker_reviews)} rows)")
    df = walker_reviews.copy()

    df = df.dropna(subset=['review_id', 'walk_id', 'walker_id', 'rating'])
    df = df[df['rating'].between(1, 5)]
    return df


def clean_dog_review(dog_reviews):
    if dog_reviews.empty:
        print("⚠️  No dog reviews data to clean")
        return dog_reviews
    
    print(f"🧹 Cleaning dog reviews data... ({len(dog_reviews)} rows)")
    df = dog_reviews.copy()

    df = df.dropna(subset=['review_id', 'walk_id', 'dog_id', 'rating'])
    df = df[df['rating'].between(1, 5)]
    return df


def clean_owner_payments(owner_payments):
    if owner_payments.empty:
        print("⚠️  No owner payments data to clean")
        return owner_payments
    
    print(f"🧹 Cleaning owner payments data... ({len(owner_payments)} rows)")
    df = owner_payments.copy()

    df = df.dropna(subset=['payment_id', 'amount', 'walk_id'])
    df["payment_datetime"] = pd.to_datetime(df["payment_datetime"], errors="coerce")
    df = df.dropna(subset=["payment_datetime"])
    df = df[df['amount'].between(5, 40)]
    df = df[df['payment_method'].isin(["DebitCard", "CreditCard"])]
    df = df[df['payment_status'].isin(["complete", "pending", "failed"])]
    return df


# ============================================================
# 🔗 NETTOYAGE RELATIONNEL ENTRE TABLES
# ============================================================

def clean_relations(
    df_dog, df_owner, df_walker,
    df_availability, df_walkrequests, df_pastwalks,
    df_walkerreview, df_dogreview, df_payment
):
    print("\n🔗 Vérification des relations entre tables...")

    valid_owner_ids = set(df_owner['owner_id'])
    df_dog = df_dog[df_dog['owner_id'].isin(valid_owner_ids)]

    valid_walker_ids = set(df_walker['walker_id'])
    df_availability = df_availability[df_availability['walker_id'].isin(valid_walker_ids)]

    df_pastwalks = df_pastwalks[
        df_pastwalks['walker_id'].isin(valid_walker_ids) &
        df_pastwalks['dog_id'].isin(df_dog['dog_id'])
    ]

    df_dogreview = df_dogreview[
        df_dogreview['walk_id'].isin(df_pastwalks['walk_id']) &
        df_dogreview['dog_id'].isin(df_dog['dog_id'])
    ]

    df_walkerreview = df_walkerreview[
        df_walkerreview['walk_id'].isin(df_pastwalks['walk_id']) &
        df_walkerreview['walker_id'].isin(df_walker['walker_id'])
    ]

    df_walkrequests = df_walkrequests[
        df_walkrequests['dog_id'].isin(df_dog['dog_id']) &
        df_walkrequests['favorite_walker_id'].isin(df_walker['walker_id'])
    ]

    df_payment = df_payment[
        df_payment['walk_id'].isin(df_pastwalks['walk_id'])
    ]

    return (
        df_dog, df_owner, df_walker,
        df_availability, df_walkrequests, df_pastwalks,
        df_walkerreview, df_dogreview, df_payment
    )


# ============================================================
# 🚀 NETTOYAGE GLOBAL
# ============================================================

def clean_all_relational():
    print("🚀 Chargement et nettoyage de tous les CSV...")

    data_paths = {
        "dog": "./data_out/df_Dog.csv",
        "owner": "./data_out/df_Owner.csv",
        "walker": "./data_out/df_Walker.csv",
        "availability": "./data_out/df_WalkerAvailability.csv",
        "walkrequests": "./data_out/df_WalksRequests.csv",
        "pastwalks": "./data_out/df_past_walks.csv",
        "walkerreview": "./data_out/df_WalkerReview.csv",
        "dogreview": "./data_out/df_DogReview.csv",
        "payment": "./data_out/df_OwnerPayment.csv",
    }

    dfs = {name: pd.read_csv(path, dtype={'phone': str}) for name, path in data_paths.items()}

    dfs["dog"] = clean_dog(dfs["dog"])
    dfs["owner"] = clean_owner(dfs["owner"])
    dfs["walker"] = clean_walker(dfs["walker"])
    dfs["availability"] = clean_walker_availability(dfs["availability"])
    dfs["walkrequests"] = clean_walk_requests(dfs["walkrequests"])
    dfs["pastwalks"] = clean_past_walks(dfs["pastwalks"])
    dfs["walkerreview"] = clean_walker_review(dfs["walkerreview"])
    dfs["dogreview"] = clean_dog_review(dfs["dogreview"])
    dfs["payment"] = clean_owner_payments(dfs["payment"])

    dfs["dog"], dfs["owner"], dfs["walker"], dfs["availability"], dfs["walkrequests"], dfs["pastwalks"], dfs["walkerreview"], dfs["dogreview"], dfs["payment"] = clean_relations(
        df_dog=dfs["dog"],
        df_owner=dfs["owner"],
        df_walker=dfs["walker"],
        df_availability=dfs["availability"],
        df_walkrequests=dfs["walkrequests"],
        df_pastwalks=dfs["pastwalks"],
        df_walkerreview=dfs["walkerreview"],
        df_dogreview=dfs["dogreview"],
        df_payment=dfs["payment"],
    )

    print("\n💾 Sauvegarde des fichiers nettoyés...")
    for name, df in dfs.items():
        df.to_csv(data_paths[name], index=False)
        print(f"✅ {name} -> {len(df)} lignes sauvegardées")

    print("\n🎉 Nettoyage complet terminé !")


if __name__ == "__main__":
    clean_all_relational()
