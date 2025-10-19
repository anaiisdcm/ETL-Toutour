from DataGeneration import generate_all_v2, make_noise
from Transform import clean
from EL_DB_Toutour import init_db, load_csv_to_db
from HotDog import run_app
import time

if __name__ == "__main__":
    print('Generating initial data ...')
    generate_all_v2.generate_all_csv()
    # make_noise.make_noise()
    time.sleep(2)

    print('Cleaning initial data ...')
    # clean.clean_all()
    time.sleep(2)

    print('Loading initial data into database ...')
    init_db.init_db()
    load_csv_to_db.main()
    time.sleep(2)
    
    print('Hot Dog !')
    run_app.run_app()

