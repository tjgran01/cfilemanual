import pandas as pd
import os

from inputmanager import InputManager
from survey_dict import survey_dict, survey_strings

class QualtricsParser(object):
    """Object that finds a qualtrics export file, examines it, and if possible
    auto-generates the conditions files based on the survey dataself.

    Args:
        qual_export(str): File path to where the qualtrics download is located.
    Returns:
        None
    """
    def __init__(self, qual_export=None, clean_it=True):
        if not qual_export:
            qual_export = InputManager.get_valid_fpath("Please enter a filepath "
                                                     "for the Qualtrics export "
                                                     "you wish to parse: ")
        self.load_in_file(qual_export)
        if clean_it:
            self.clean_qualtrics_export()
            self.set_headers()
            self.find_marks()


    def load_in_file(self, qual_export):
        """Loads the Qualtrics Export .csv as a pandas DataFrame object.

        Args:
            qual_export(str): File path to where the qualtrics download is
            located.
        Sets:
            self.df(DataFrame): a pandas DataFrame of the Qualtrics export.
            self.file_name(str): the name of the Qualtrics export file.
        """
        self.df = pd.read_csv(qual_export)
        last_slash = qual_export.rfind("/")
        self.file_name = qual_export[last_slash + 1:]
        print(f"File: '{self.file_name}' sucessfully loaded.")


    def clean_qualtrics_export(self, col_to_drop=None):
        """Drops the columns and rows in self.df that are not needed in the
        generation of conditions files.

        Args:
            col_to_drop(list): list of columns to drop from the Qualtrics Export
        Sets:
            self.id_col(Series): The column in self.df that corresponds to
            the participant IDs in the experiment.
            self.par_ids(list): A list of participant IDs.
            self.head_cir_col(Series): The column in self.df that corresponds to
            the participants head sizes.
        """
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
        """Sets the header column of self.df to the text of the questions asked
        in the Qualtrics Surveys.

        Args:
            None
        Sets:
            self.df.columns: Sets the headers of self.df to the questions asked
            in the Qualtrics survey.
            self.questions(list): List of all of the questions asked in the
            survey."""
        headcol = self.df.iloc[0]
        self.df.columns = headcol
        self.questions = list(self.df.columns)
        print("Headers set.")


    def find_marks(self, mark=" "):
        """Looks through the question headers and picks out which of the headers
        indicate a mark in the data.

        Args:
            mark(str): The string value of the mark question in qualtrics.
            Default=" "
        Sets:
            self.mark_list(list): A list of the indexes of where the marks are
            in the qualtrics export.
            self.total_survey_length: The number of total question in the export.
            self.total_tasks: The number of tasks the participant was subjected
            to during the experiment.
            self.single_survey_length: The number of questions in each survey
            that was given after a task was completed.
            self.total_prelim_qs: The number of questions asked before the first
            task survey was started.
            """
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


    def parse_at_marks(self):
        """Determines if the number of questions in each Qualtrics survey are
        even and then decides on a parsing method.

        Args:
            None
        Sets:
            self.question_headings(set): Non-repeating seting of the questions
            in the Qualtrics Export."""
        if self.even_survey_length:
            self.question_headings = self.questions[self.total_prelim_qs:
                                                    self.total_prelim_qs +
                                                    self.single_survey_length]
        else:
            print("\033[1mWARNING\033[0m: Number of survey questions found in"
                  " this export are not even across tasks. This may lead to "
                  " errors when attempting to parse the file.")
            self.question_headings = set(self.questions[self.total_prelim_qs:])

        self.make_headings_col()


    def check_if_even_qs(self, mark_list):
        """Checks to see if the amount of questions administered in each survey
        are equal to one another.

        Args:
            mark_list(list): List of the mark indexes in the Qualtrics Export
        Returns:
            Bool: True if the space between indexes are true, False if they are
            not."""
        questions_per_survey = []
        for i, x in enumerate(self.mark_list):
            if i > 0:
                y = self.mark_list[i - 1]
                questions_per_survey.append(x - y)
        if len(set(questions_per_survey)) != 1:
            return False
        return True


    def make_headings_col(self):
        """Finds the proper variable names for the conditions files based on the
         survey questions given to the participants.

        Args:
            None
        Sets:
            self.headings_col(Series): A series object with all of the proper
            headings to be written to the exported conditions files.
        """
        headings_col = []
        headings_col.append(survey_dict["phys_info"])
        if survey_strings["tlx"] in self.question_headings:
            headings_col.append(survey_dict["tlx"])
        if survey_strings["mrq"] in self.question_headings:
            headings_col.append(survey_dict["mrq"])

        headings_col = [elm for list in headings_col for elm in list]
        self.headings_col = pd.Series(headings_col)


    def qualtrics_to_conditions(self):
        """Properly parses the data in the qualtrics export to the format it
        needs to be written to in the conditions file.

        Args:
            None
        Sets:
            cond_df(DataFrame): A DataFrame object corresponding to an individual
            conditions file to be written.
        """
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

    def write_to_csv(self, par_id, cond_df, sensor_type="fNIRS", session="1"):
        """Writes cond_df to a .csv file.

        Args:
            par_id(str): The participant ID number corresponding the the conditions
            file.
            cond_df(DataFrame): The DataFrame object to be written to a .csv
            file.
            sensor_type(str): The Sensor type the the conditions file is being
            written for.
            session(str): The session number that the conditions file is being
            written for.
        """

        if not os.path.exists(f"./{par_id[:-2]}00's_conditions/"):
            os.mkdir(f"./{par_id[:-2]}00's_conditions/")

        cond_df.to_csv((f"./{par_id[:-2]}00's_conditions/{par_id}_{sensor_type}_"
                        f"conditions_s{session}.csv"), index=False)
        print(f"\033[1mSUCCESS:\033[0m\n"
              f"File: {par_id}_{sensor_type}_conditions_s{session}.csv\n"
              f"written to: {os.getcwd()}/{par_id[:-2]}00's_conditions\n")


    def print_info(self):
        print(f"File being parsed: {self.file_name}")
        print(f"Ids in experiment:\n {self.id_col}")
        print(f"Total Survey Length: {self.total_survey_length}")
        print(f"Number of preliminary questions: {self.total_prelim_qs}")
        print(f"Number of questions per survey: {self.single_survey_length}")
        print(f"Number of tasks: {self.total_tasks}")
        print(f"All question headings: {self.question_headings}")
