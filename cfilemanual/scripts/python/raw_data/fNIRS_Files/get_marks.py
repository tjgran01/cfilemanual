import pandas as pd
import os

files = []
for f_name in os.listdir(os.getcwd()):
    if "_Deoxy" in f_name:
        df = pd.read_csv(f_name, header=34)
        marks = df["Mark"].tolist()
        marks = [i_mark for i_mark, mark in enumerate(marks) if mark > 0]
        marks = [mark for i_mark, mark in enumerate(marks) if i_mark % 2 != 0]
        durations = []
        for indx, onset in enumerate(marks):
            if indx > 0 and indx % 2 != 0:
                last_onset = marks[indx - 1]
                durations.append(onset - last_onset)
        marks = [mark for i_mark, mark in enumerate(marks) if i_mark % 2 != 0]
        print(f_name)
        print(f"Onsets: {marks}")
        x = (len(marks))
        print(f"Durations: {durations}")
        print("")
        if x == 15:
            files.append(f_name)

print(files)
