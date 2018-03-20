import pandas as pd
import os

def main(par_id):
    target_dir = f"{os.getcwd()}/data_files/"
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    os.chdir(f"{os.getcwd()}/data_files/")



if __name__ == "__main__":
    main(par_id=0000)
