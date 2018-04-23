import pandas as pd
import numpy as np
import os
import csv


from inputmanager import InputManager


class BIOPACParser(object):
    """Takes in a BIOPAC .txt file, creates a .csv verision of the .txt file,
    and finds the onsets and durations of tasks in the data.
    """
    def __init__(self, bio_file="./samplebiopac/7777_BIOPAC_s2.csv",
                 mark_csv=False):
        self.file_path = bio_file
        if self.file_path[-4:] == ".txt" and make_csv:
            self.convert_to_csv()
        self.df = pd.read_csv(f"{self.file_path[:-4]}.csv", header=9)
        self.get_col_names()
        self.mark_col = self.df["Mark"]
        self.mark_list = self.get_mark_list(self.mark_col)
        self.num_of_marks = int(len(self.mark_list) / 2) # Two pulses = 1 mark.
        self.onsets = self.get_onsets(self.mark_list)
        self.durations = self.get_durations(self.onsets, self.close_marks)


    def convert_to_csv(self):
        """Takes the current .txt file, reads the incoming information, and
        writes it to a .csv
        """
        with open(self.file_path, "r") as in_txt:
            reader = csv.reader(in_txt, delimiter=",")

            data = [r for r in reader]

        with open(f"{self.file_path[:-4]}.csv", "w") as out_csv:
            csv_writer = csv.writer(out_csv, delimiter=",")
            for d in data:
                csv_writer.writerow(d)
            print(".csv file written.")


    def get_col_names(self):
        """Asks the user to rename the columns if they were not properly named
        before.
        """
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
        """Culls down the list of marks (as the marking pulse is about 0.5
        seconds) and returns only the first index (row) value of that mark.

        Args:
            mark_col(Series): The column in the BIOPAC df that holds the marking
            information.
        Returns
            cleaned_ml(list): A cleaned mark list - with one index value
            representing one voltage change in the BIOPAC.
        Note:
            This will not clean out noise in the BIOPAC data file. A function
            will soon be added to account for this.
        """
        mark_list = [indx for indx, mark in enumerate(mark_col)
                     if mark > 0 and mark < 10]
        cleaned_ml = []
        for indx, mark in enumerate(mark_list):
            y = mark_list[indx - 1]
            if mark != y + 1:
                cleaned_ml.append(mark)
        return cleaned_ml


    def get_task_information(self, mark_type="open_close"):
        """Determines how many tasks are in the current data file based on the
        fingerprint left by the marks. This is for sanity checking purposes.

        Args:
            mark_type(str): The mark structure of the list - 'open_close' by
            default, meaning the first set of marks indicates the start of a
            task, and the next set of marks indicates the end of a task.
        Sets:
            self.task_num(int): The number of tasks in the physiological data.
        """

        if mark_type == "open_close":
            self.task_num = int(self.num_of_marks / 2)


    def get_onsets(self, mark_list):
        """Gets the onset index (row #) of each task in the data.

        Args:
            mark_list(list): the list of indexs (row #s) of all of the marks
            in the data.
        Returns:
            open_marks(list): A list of the marks that indicate a mark has been
            opened.
        Sets:
            self.close_marks(list): A list of the marks that indicate a mark has
            been closed.
        """
        # Remove duplicate marks.
        marks = [mark for indx, mark in enumerate(mark_list)
                 if indx % 2 == 0 or indx == 0]
        open_marks = [mark for indx, mark in enumerate(marks)
                      if indx % 2 == 0 or indx == 0]
        self.close_marks = [mark for indx, mark in enumerate(marks)
                            if indx % 2 != 0]

        return open_marks


    def get_durations(self, onsets, close_marks):
        """Gets the amount of indexes during which a participant was performing
        a task.

        Args:
            onsets(list): A list of the marks that indicate a mark has been
            opened.
            close_marks(list): A list of the marks that indicate a mark has been
            closed.
        Returns:
            durations(list): the amount of indexes during which a participant
            was performing a task.
        """
        onsets = np.array(onsets)
        close_marks = np.array(close_marks)
        durations = close_marks - onsets
        return list(durations)
