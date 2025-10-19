import os

def run_app():
    commande = f'streamlit run ./HotDog/hot_dog.py'
    print(commande)
    
    os.system(commande)

if __name__=='__main__':
    print("Testing hot dog ...")
    run_app()

    