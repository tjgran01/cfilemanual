import pandas as pd
import os
import csv
from collections import Counter

from inputmanager import InputManager


class BIOPACParser(object):
    def __init__(self, bio_file="./samplebiopac/7777_BIOPAC_s2.csv",
                 mark_csv=False):
        self.file_path = bio_file
        if self.file_path[-4:] == ".txt" and make_csv:
            self.convert_to_csv()
        self.df = pd.read_csv(f"{self.file_path[:-4]}.csv", header=9)
        self.get_col_names()
        self.mark_col = self.df["Mark"]
        self.mark_list = self.get_mark_list(self.mark_col)
        self.num_of_marks = len(self.mark_list) / 2 # Two pulses = 1 mark.


    def convert_to_csv(self):
        with open(self.file_path, "r") as in_txt:
            reader = csv.reader(in_txt, delimiter=",")

            data = [r for r in reader]

        with open(f"{self.file_path[:-4]}.csv", "w") as out_csv:
            csv_writer = csv.writer(out_csv, delimiter=",")
            for d in data:
                csv_writer.writerow(d)
            print(".csv file written.")


    def get_col_names(self):

        new_col_names = []
        for col_name in self.df.columns:

            ans = InputManager.get_variable_name(f"Input a measure name "
                                                 f"for column: {col_name}. "
                                                 "Type 'd' to drop col, "
                                                 " or 'k' to keep default: ")
            if ans == 'k':
                new_col_names.append(col_name)
            elif ans == 'd':
                self.df.drop(col_name)
            else:
                new_col_names.append(ans)

        self.df.columns = new_col_names



    def get_mark_list(self, mark_col):

        mark_list = [indx for indx, mark in enumerate(mark_col)
                     if mark > 0 and mark < 10]
        cleaned_ml = []
        for indx, mark in enumerate(mark_list):
            y = mark_list[indx - 1]
            if mark != y + 1:
                cleaned_ml.append(mark)
        return cleaned_ml
