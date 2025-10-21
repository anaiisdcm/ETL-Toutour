import pandas as pd
import numpy as np
import numpy.random as nrd
import random as rd
import string


def init_values():
    """
    Numbers numbers
    """
    n_total_past_walk = 1000
    n_total_dog = 100
    n_total_owner = 50
    n_total_walker = 50
    n_total_availability = 100
    n_total_request = 30

    if n_total_dog < n_total_owner  :
        print(f" *!* number of owner ({n_total_owner}) is superior to the number of dogs ({n_total_dogs})")
    if n_total_request < n_total_walker :
        print(f" *!* number of requests ({n_total_request}) is superior to the number of walkers ({n_total_walker})")
    
    return n_total_past_walk, n_total_dog, n_total_owner, n_total_walker, n_total_availability, n_total_request


def generate_all_csv(dog = True, owner = True, walker = True, walker_availability = True, past_walks = True, walker_review = True, owner_payment = True, walk_requests = True, dog_review = True):
    # for reproductibility
    nrd.seed(33)

    n_total_past_walk, n_total_dog, n_total_owner, n_total_walker, n_total_availability, n_total_request = init_values()


    """
    Generate all required csv
    """

    if owner :
        # --- owners 
        n_owner = n_total_owner
        
        last_name = rd.choices(["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Brunissende"], k=n_owner)
        first_name = rd.choices(["Jean", "Marie", "Pierre", "Sophie", "Luc", "Octave", "Odilon", "Odon", "Oger", "Olivier", "Oury", "Pacôme", "Palémon", "Parfait", "Pascal", "Paterne", "Patrice", "Paul", "Pépin", "Perceval", "Philémon", "Philibert", "Philippe", "Philothée", "Pie", "Pierre", "Pierrick", "Prosper", "Quentin", "Raoul", "Raphaël", "Raymond", "Régis", "Réjean", "Rémi", "Renaud", "René", "Reybaud", "Richard", "Robert", "Roch", "Rodolphe", "Rodrigue", "Roger", "Roland", "Romain", "Romuald", "Roméo", "Rome", "Ronan", "Roselin", "Salomon", "Samuel", "Savin", "Savinien", "Scholastique", "Sébastien", "Séraphin", "Serge", "Séverin", "Sidoine", "Sigebert", "Sigismond", "Silvère", "Simon", "Siméon", "Sixte", "Stanislas", "Stéphane", "Stephan", "Sylvain", "Sylvestre", "Tancrède", "Tanguy", "Taurin", "Théodore"], k=n_owner)
        email = [f"{p}.{n}@example.com".lower() for p, n in zip(first_name, last_name)]
        phone = ["06" + "".join(rd.choices(string.digits, k=8)) for _ in range(n_owner)]
        owner_id = [last_name[i] + first_name[i] + str(nrd.randint(0, 1e8)) for i in range(n_owner)]

        picture = ["/pictures/owners/" + idd for idd in owner_id]
        bio = ["Bio de " + p + " " + n for p, n in zip(first_name, last_name)]
        
        df_owner = pd.DataFrame({
            'owner_id': owner_id,
            'last_name': last_name,
            'first_name': first_name,
            'email': email,
            'phone': phone,
            'picture': picture,
            'bio': bio
        })
        df_owner.to_csv("./data_out/df_Owner.csv", index=False)




    if dog :
        # load & diplay
        df_quaggle_dog = pd.read_csv("./data_in/dogs_dataset.csv")
        n_dog = min(len(df_quaggle_dog['Breed']), n_total_dog)
        #print(df_quaggle_dog.head())
        
        random_ids = np.random.randint(1e5, 1e15, size=n_dog)
        chip_id = [str(250) + f"{r:015d}" for r in random_ids ]
        owner_id = nrd.choice(owner_id, n_dog, replace=True)
        name = nrd.choice(["John", "Milou", "Rex", "Idefix", 'Max','Charlie','Bella','Poppy','Daisy','Buster','Alfie','Millie','Molly','Rosie','Buddy','Barney','Lola','Roxy','Ruby','Tilly','Bailey','Marley','Tia', 'Bernie'], n_dog)

        
        # init fields
        dog_id = [f"{name[j]}_{chip_id[j]}" for j in range(n_dog)]
        
        
        weight = df_quaggle_dog['Weight (kg)'][:n_dog]
        breed = df_quaggle_dog['Breed'][:n_dog]
        picture = ["/pictures/dogs/" + idd for idd in dog_id]
        birthdate = 2025 - np.round(df_quaggle_dog['Age (Years)'])[:n_dog]
        optimal_tour_duration = np.floor( (weight + (nrd.rand(n_dog)+1)*weight/2)/3 )
        athleticism = nrd.randint(0, 10, size=n_dog)
        
        
        # file in fields & save
        df_dog = pd.DataFrame({'dog_id': dog_id,
                            'chip_id': chip_id,
                            'owner_id': owner_id,
                            'name': name,
                            'weight': weight,
                            'breed': breed,
                            'picture': picture,
                            'birth_date': birthdate,
                            'optimal_tour_duration': optimal_tour_duration,
                            'athleticism': athleticism
                })
        
        df_dog.to_csv("./data_out/df_Dog.csv")




    if walker :
        # --- walkers 
        n_walker = n_total_walker
        

        last_name = rd.choices(["Dupont", "Lambert", "Petit", "Moreau", "Girard"], k=n_walker)
        first_name = rd.choices(["Nicolas", "Camille", "Julien", "Élodie", "Thomas"], k=n_walker)
        walker_id = [last_name[i] + first_name[i] + str(nrd.randint(0, 1e8)) for i in range(n_walker)]

        picture = ["/pictures/walkers/" + idd for idd in walker_id]
        bio = ["Bio de " + p + " " + n for p, n in zip(first_name, last_name)]
        profil_verifie = rd.choices([True, False], k=n_walker)
        email = [f"{p}.{n}@laposte.net".lower() for p, n in zip(first_name, last_name)]
        phone = ["07" + "".join(rd.choices(string.digits, k=8)) for _ in range(n_walker)]
        birth_date = nrd.normal(1990, 20, size=n_walker)
        rib = ["FR76" + "".join(rd.choices(string.digits, k=23)) for _ in range(n_walker)]


        
        df_walker = pd.DataFrame({
            'walker_id': walker_id,
            'last_name': last_name,
            'first_name': first_name,
            'picture': picture,
            'bio': bio,
            'verified_profile': profil_verifie,
            'email': email,
            'phone': phone,
            'birth_date': birth_date,
            'rib': rib
        })
        df_walker.to_csv("./data_out/df_Walker.csv", index=False)


    if walker_availability :
        # --- walker_availability 
        n_availability = n_total_availability
        walker_id = rd.choices(df_walker['walker_id'], k=n_availability)

        address = rd.choices(["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux"], k=n_availability)
        
        # generate availability
        dr = pd.date_range("2025-10-10", "2026-02-02", freq="h")
        # random start datetime
        start_datetime = pd.to_datetime(np.sort(np.random.permutation(np.arange(len(dr)))[:n_availability]))
        # random start datetime + [1-6] h of availability
        end_datetime = start_datetime + pd.to_timedelta(nrd.randint(1, 6, size=n_availability), unit="h")

        #start_datetime = pd.date_range(start="2025-10-01", periods=n_availability, freq="h").tolist()
        #end_datetime = pd.date_range(start="2025-10-02", periods=n_availability, freq="h").tolist()
        
        availability_id = [walker_id[i] + str(start_datetime[i]) for i in range(n_availability)]

        df_walker_availability = pd.DataFrame({
            'walker_id': walker_id,
            'address': address,
            'availability_id':availability_id,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime
        })
        df_walker_availability.to_csv("./data_out/df_WalkerAvailability.csv", index=False)



    if walk_requests :
        # --- walks_requests 
        n_request = n_total_request
        
        dog_id = rd.choices(df_dog['dog_id'], k=n_request) 
        address = rd.choices(["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux"], k=n_request)
        ideal_start_datetime = pd.date_range(start="2025-10-03", periods=n_request, freq="h").tolist()
        duration_request = [nrd.randint(30, 120) if nrd.random() > 0.6 else np.nan for _ in range(n_request)]
        distance_request = [nrd.randint(1, 10) if nrd.random() > 0.6 else np.nan for _ in range(n_request)]
        walk_id = [dog_id[i] + str(ideal_start_datetime[i]) for i in range(n_request)]

        favorite_walker_id = [nrd.choice(df_walker['walker_id']) if rd.random() > 0.7 else np.nan for _ in range(n_request)]
        predicted_payment = [nrd.randint(10, 50) for _ in range(n_request)]
        
        df_walks_requests = pd.DataFrame({
            'dog_id': dog_id,
            'walk_id': walk_id,
            'address': address,
            'ideal_start_datetime': ideal_start_datetime,
            'duration_request': duration_request,
            'distance_request': distance_request,
            'favorite_walker_id': favorite_walker_id,
            'predicted_payment': predicted_payment
        })
        df_walks_requests.to_csv("./data_out/df_WalksRequests.csv", index=False)


    if past_walks :
        # --- past walks
        n_walk = n_total_past_walk 
        
        dog_id = rd.choices(df_dog['dog_id'], k=n_walk) 
        walker_id = rd.choices(df_walker['walker_id'], k=n_walk)
        distance = nrd.randint(1, 15, n_walk)
        start_datetime = pd.date_range(start="2025-09-01", periods=n_walk, freq="h").tolist()
        end_datetime = pd.date_range(start="2025-09-02", periods=n_walk, freq="h").tolist()

        walk_id = [dog_id[i] + '-' + walker_id[i] + str(start_datetime[i]) for i in range(n_walk)]
        picture = ["/pictures/past_walks/" + idd for idd in walk_id]

        dog_review_id = [walk_id[i] + "_dogreview" for i in range(n_walk)]
        walker_review_id = [walk_id[i] + "_walkerreview" for i in range(n_walk)]


        
        df_past_walks = pd.DataFrame({
            'walk_id': walk_id,
            'dog_id': dog_id,
            'walker_id': walker_id,
            'distance': distance,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'picture': picture,
            'dog_review_id': dog_review_id,
            'walker_review_id': walker_review_id
        })
        df_past_walks.to_csv("./data_out/df_past_walks.csv", index=False)



    # --- Walker Reviews
    if walker_review:
        df_walker_review = pd.DataFrame({
            'review_id': [wid + "_walkerreview" for wid in df_past_walks['walk_id']],
            'walk_id': df_past_walks['walk_id'],
            'walker_id': df_past_walks['walker_id'],
            'rating': nrd.choice(np.arange(1, 6), size=len(df_past_walks), replace=True, p=[0.1, 0.05, 0.05, 0.3, 0.5]),
            'comment': ["Commentaire pour walk " + str(i) for i in range(len(df_past_walks))]
        })
        df_walker_review.to_csv("./data_out/df_WalkerReview.csv", index=False)

    # --- Dog Reviews
    if dog_review:
        df_dog_review = pd.DataFrame({
            'review_id': [wid + "_dogreview" for wid in df_past_walks['walk_id']],
            'walk_id': df_past_walks['walk_id'],
            'dog_id': df_past_walks['dog_id'],
            'rating': nrd.choice(np.arange(1, 6), size=len(df_past_walks), replace=True, p=[0.1, 0.05, 0.05, 0.3, 0.5]),
            'comment': ["Commentaire pour chien " + str(i) for i in range(len(df_past_walks))]
        })
        df_dog_review.to_csv("./data_out/df_DogReview.csv", index=False)





    if owner_payment :
        # --- owner_payment 
        n_payment = n_total_past_walk
        # payment is supposed unique for a walk
        walk_id = nrd.choice(df_past_walks['walk_id'], n_payment, replace=False)
        amount = [rd.randint(3, 40) for _ in range(n_payment)] # should go look in the walk_request, predicted_payment
        payment_datetime = pd.date_range(start="2025-09-10", periods=n_payment, freq="h").tolist()
        payment_method = rd.choices(["DebitCard", "CreditCard"], k=n_payment)
        payment_status = rd.choices(["complete", "pending", "failed"], k=n_payment)
        payment_id = [walk_id[i] + "_000" for i in range(n_payment)]

        df_owner_payment = pd.DataFrame({
            'payment_id':payment_id,
            'walk_id': walk_id,
            'amount': amount,
            'payment_datetime': payment_datetime,
            'payment_method': payment_method,
            'payment_status': payment_status
        })
        df_owner_payment.to_csv("./data_out/df_OwnerPayment.csv", index=False)

    return None


if __name__ == "__main__":
    generate_all_csv()