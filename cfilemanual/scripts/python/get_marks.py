import pandas as pd
import os
import csv

def main(par_id):

    target_dir = f"{os.getcwd()}/data_files/"
    cond_dir = f"{os.getcwd()}/experiment_{str(par_id)[:2]}_cfiles/"

    for var in (target_dir, cond_dir):
        if not os.path.exists(var):
            os.mkdir(var)

    for file_name in os.listdir(target_dir):
        if str(par_id) in file_name and "Probe1_Deoxy" in file_name:
            df = pd.read_csv(f"{target_dir}/{file_name}", header=34)
            mark_list = df["Mark"].tolist()
            semantic_mark_list = [x for x in mark_list if x > 0]
            onsets = [i for i, x in enumerate(mark_list) if x > 0]
            print(onsets)
            print(semantic_mark_list)
            offset_onsets = onsets[1:]
            offset_onsets.append(offset_onsets[-1] + 100)
            durations = [offset_onsets - onsets for offset_onsets, onsets in zip(offset_onsets, onsets)]

    for file_name in os.listdir(cond_dir):
        if str(par_id) in file_name:
            with open(f"{cond_dir}/{file_name}", "r") as in_csv:
                old_file = csv.reader(in_csv)
                new_file = []
                for row in old_file:
                    if row[0] == "onset":
                        row = onsets[:len(row) -1]
                        row.insert(0, "onset")
                    elif row[0] == "duration":
                        row = durations[:len(row) - 1]
                        row.insert(0, "duration")
                    new_file.append(row)

                print(new_file)

            with open(f"{cond_dir}/{file_name}", "w") as out_csv:
                writer = csv.writer(out_csv)

                for row in new_file:
                    writer.writerow(row)




            # df = pd.read_csv(f"{cond_dir}/{file_name}")
            # df.loc["onset"] = onsets[:df.shape[1]]



if __name__ == "__main__":
    main(par_id=9999)
