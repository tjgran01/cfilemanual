import pandas as pd
import os

from inputmanager import InputManager

class QualtricsParser(object):
    def __init__(self, file_path=None, clean_it=True):
        if not file_path:
            file_path = InputManager.get_valid_fpath("Please enter a filepath "
                                                     "for the Qualtrics export "
                                                     "you wish to parse: ")
        self.load_in_file(file_path)
        if clean_it:
            self.clean_qualtrics_export()
            self.set_headers()
            self.find_marks()


    def load_in_file(self, file_path):
        self.df = pd.read_csv(file_path)
        last_slash = file_path.rfind("/")
        self.file_name = file_path[last_slash + 1:]
        print(f"File: '{self.file_name}' sucessfully loaded.")


    def clean_qualtrics_export(self, col_to_drop=None):
        if not col_to_drop:
            col_to_drop = ["ResponseID", "ResponseSet", "IPAddress", "StartDate",
            			   "EndDate", "RecipientLastName",	"RecipientFirstName",
            			   "RecipientEmail", "ExternalDataReference", "Finished",
            			   "Status", "LocationLatitude", "LocationLongitude",
            			   "LocationAccuracy"]

        self.df.drop(col_to_drop, axis=1, inplace=True)
        self.df.drop(self.df.index[1], axis=0, inplace=True)
        self.id_col = self.df.iloc[:, 0]
        self.par_ids = self.id_col.tolist()
        self.head_cir_col = self.df.iloc[:, 1]
        print("Unneeded columns have been stripped away.")


    def set_headers(self):
        headcol = self.df.iloc[0]
        self.df.columns = headcol
        self.questions = list(self.df.columns)
        print("Headers set.")


    def find_marks(self, mark=" "):
        self.mark_list = [i for i, x in enumerate(self.questions) if x == mark]
        print(f"Marks found: {len(self.mark_list)} \n"
              f"Locations: {self.mark_list}")
        self.even_survey_length = self.check_if_even_qs(self.mark_list)
        if self.even_survey_length:
            self.total_survey_length = len(self.questions)
            self.total_tasks = len(self.mark_list)
            self.single_survey_length = self.mark_list[1] - self.mark_list[0]
            self.total_prelim_qs = (self.total_survey_length -
                                   (self.single_survey_length *
                                    self.total_tasks))


    def check_if_even_qs(self, mark_list):

        questions_per_survey = []
        for i, x in enumerate(self.mark_list):
            if i > 0:
                y = self.mark_list[i - 1]
                questions_per_survey.append(x - y)
        if len(set(questions_per_survey)) != 1:
            return False
        return True



    def parse_at_marks(self):
        self.question_headings = set(self.questions[self.total_prelim_qs:])


class HeadingLoader(object):
    def __init__(self):
        self.headings = {"tlx": ["", "onset", "duration", "stim", "tlx",
    								"tlx_mental", "tlx_physical",
    								"tlx_temporal", "tlx_performance",
    								"tlx_effort", "tlx_frustration"],
						"mrq": ["", "onset", "duration", "stim", "mrq"],
						}
