import pandas as pd
import os
import csv
from collections import Counter

from inputmanager import InputManager

class FNIRSParser(object):
    def __init__(self, fnirs_file="./samplefnirs/test_1.csv"):
        self.fnirs_file = fnirs_file
        self.df = pd.read_csv(fnirs_file, header=34)
        self.mark_col = self.df["Mark"].tolist()
        self.marks = [mark for mark in self.mark_col if mark > 0]
        self.mark_indexes = [indx for indx, mark in enumerate(self.mark_col)
                             if mark > 0]
        self.valid_marks = self.validate_marks(self.marks)
        self.valid_spaceing = self.validate_spacing(self.mark_indexes)
        if self.valid_marks:
            print("Marking appears to be valid. Even number of marks found. \n")
            print(f"Mark spacing Warnings: {[len(self.space_warnings)]}\n")
            print(f"Mark values:\n{self.mark_counts}")
            self.onsets = self.get_onsets(self.mark_indexes)
            self.task_number = len(self.onsets)
            self.durations = self.get_durations(self.onsets)
        else:
            print("\033[1mWARNING:\033[0m\n"
                  "Something appears to have gone wrong in the marking "
                  "of this file. fNIRS marks need to be opened and closed. "
                  "You can continue to attempt to parse the file, but the "
                  "outcomes may not be correct. Make sure to check outputs "
                  "for validity if you decide to continue. ")
            ans = InputManager.get_yes_or_no("Try anyway? (Y/n): ")
            if not ans:
                pass
            self.get_onsets()



    def validate_marks(self, marks):

        self.mark_counts = Counter(marks)
        for key, value in self.mark_counts.items():
            if value % 2 != 0:
                return False
        return True


    def validate_spacing(self, mark_indexes):

        self.space_warnings = []
        for indx, mark in enumerate(mark_indexes):
            if indx % 2 == 0 or indx == 0:
                # only onset marks
                if int(mark) + 5 != int(mark_indexes[indx + 1]):
                    if int(mark_indexes[indx + 1]) - int(mark) == 4:
                        print("\033[1mWARNING:\033[0m\n"
                              f"The spacing between Mark onset number: "
                              f"{int(indx / 2)}, "
                               "and it's Mark offset are not exact. If you "
                               "experience a many of these warnings "
                               "something may be wrong with the marking in this"
                               " file. \n\n"
                               f"Check the original file around index {mark} "
                               "to ensure that this was a sampling issue, and "
                               "not a larger issue that could invalidate the "
                               "data. \n")
                        self.space_warnings.append(indx)
                    else:
                        return False
        return True



    def get_onsets(self, mark_indexes):

        return [mark_index for indx, mark_index in enumerate(mark_indexes)
                if indx % 2 == 0 or indx == 0]


    def get_durations(self, onsets):

        durations = []
        for indx, onset in enumerate(onsets):
            if indx > 0:
                last_onset = onsets[indx - 1]
                durations.append(onset - last_onset)
        return durations


    def write_to_conditions(self, c_dir="./sample_cond/", par_id="sample",
                            sess="1"):

        with open(f"{c_dir}/{par_id}_fNIRS_conditions_s{sess}.csv", "a") as c_file:
            print("Opened!")
