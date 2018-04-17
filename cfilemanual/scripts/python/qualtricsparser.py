import pandas as pd
import os

from inputmanager import InputManager
from survey_dict import survey_dict, survey_strings

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


    def make_headings_col(self):

        headings_col = []
        headings_col.append(survey_dict["phys_info"])
        if survey_strings["tlx"] in self.question_headings:
            headings_col.append(survey_dict["tlx"])
        if survey_strings["mrq"] in self.question_headings:
            headings_col.append(survey_dict["mrq"])

        headings_col = [elm for list in headings_col for elm in list]
        self.headings_col = pd.Series(headings_col)


    def parse_marked_data(self):

        for index, row in self.df.iterrows():
            par_id = row[0]
            if par_id.isnumeric():
                head_cir = row[0]
                data = list(row[self.total_prelim_qs:])
                data = [data[x:x+self.single_survey_length] for x in
                        range(0, len(data), self.single_survey_length)]

                cond_df = pd.DataFrame(self.headings_col)
                for i, survey in enumerate(data):
                    for x in range(0, 3):
                        survey.insert(0, "")
                    data_series = pd.Series(survey)
                    cond_df[f"Task {i + 1}"] = data_series
                cond_df.drop(0, axis=0, inplace=True)
                self.write_to_csv(par_id, cond_df)



    def parse_at_marks(self):
        if self.even_survey_length:
            self.question_headings = self.questions[self.total_prelim_qs:
                                                    self.total_prelim_qs +
                                                    self.single_survey_length]
        else:
            self.question_headings = set(self.questions[self.total_prelim_qs:])

        self.make_headings_col()


    def write_to_csv(self, par_id, cond_df, sensor_type="fNIRS", session="1"):

        if not os.path.exists(f"./{par_id[:-2]}00's_conditions/"):
            os.mkdir(f"./{par_id[:-2]}00's_conditions/")

        cond_df.to_csv((f"./{par_id[:-2]}00's_conditions/{par_id}_{sensor_type}_"
                        f"conditions_s{session}.csv"), index=False)




class ConditionsFileCreator(object):
    def __init__(self, headings_col, task_number):
        self.headings_col = headings_col
        self.task_number = task_number
