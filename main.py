from DataGeneration import generate_all_v2, make_noise
from Transform import clean
from EL_DB_Toutour import init_db, load_csv_to_db
from HotDog import run_app
import time
pause_time = 2

if __name__ == "__main__":
    print('Generating initial data ...')
    generate_all_v2.generate_all_csv()
    make_noise.make_noise(pc_null=1, pc_nullrows=0, pc_exagerated=0, directory_out="./data_out", except_ids=True)
    time.sleep(pause_time)

    print('Cleaning initial data ...')

    clean.clean_all()
    time.sleep(pause_time)

    print('Loading initial data into database ...')
    init_db.init_db()
    load_csv_to_db.main()
    time.sleep(pause_time)
    
    print('Hot Dog !')
    run_app.run_app()

