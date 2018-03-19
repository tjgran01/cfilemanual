import pandas as pd
import os
import getpass
import csv

import get_qualtrics
from inputmanager import InputManager


def check_if_download():
	if not os.path.exists(f"{os.getcwd()}/MyQualtricsDownload/"):
		apiToken = get_qualtrics.get_api_token()
		surveyId = get_qualtrics.get_survey_id(apiToken)
		get_qualtrics.main(surveyId, apiToken)


def get_q_measures(num_questions):

	keyword_measures = {"tlx": ["", "onset", "duration", "stim", "tlx",
								"tlx_mental", "tlx_physical",
								"tlx_temporal", "tlx_performance",
								"tlx_effort", "tlx_frustration"]
						}

	q_measures = []
	for x in range(0, num_questions + 1):
		if x == 0:
			q_measures.append("")
		elif x == 1:
			q_measures.append("stim")
		else:
			measure = InputManager.get_variable_name(f"Please enter the measurement name for question {x + 1} in the survey.")
			q_measures.append(measure)
			if measure in keyword_measures:
				return keyword_measures[measure]

	return q_measures


def make_c_files(par_id, csv_data, q_measures,
				 sensor_type="fNIRS", session_num="1"):

	exper_id = par_id[:2]
	csv_data = zip(*csv_data)
	csv_data = [list(x) for x in csv_data]
	# inserts blank rows for onset and duration
	csv_data.insert(1, [])
	csv_data.insert(1, [])

	if not os.path.exists(f"./experiment_{exper_id}_cfiles/"):
		os.mkdir(f"./experiment_{exper_id}_cfiles/")

	file_name = f"./experiment_{exper_id}_cfiles/{par_id}_{sensor_type}_conditions_s{session_num}.csv"

	with open(file_name, "w") as out_csv:
		writer = csv.writer(out_csv, delimiter=",")

		for i, row in enumerate(csv_data):
			row.insert(0, q_measures[i])
			writer.writerow(row)


def get_slice_points(indexer_list):
	# Scans question text to determine where stim is entered by experimentor.
	slice_points = []
	for i, row in enumerate(indexer_list):
		if row == slice_prompt:
			slice_points.append(i)
	return(slice_points)


def count_survey_questions(slice_points):

	num_questions = []
	for i, slice_point in enumerate(slice_points):
		if i == 0:
			x = 0
		y = slice_point
		question_num = abs((x - y))
		num_questions.append(question_num)
		x = slice_point
	return num_questions[1:]


def check_num_questions(num_questions):
	return len(set(num_questions)) <= 1


def main(col_to_drop, slice_prompt):
	check_if_download()
	file_name = str(os.listdir(f"{os.getcwd()}/MyQualtricsDownload/"))[2:-2]
	df = pd.read_csv(f"{os.getcwd()}/MyQualtricsDownload/{file_name}")
	df.drop(col_to_drop, axis=1, inplace=True)
	df.drop(1, axis=0, inplace=True)

	par_ids = df["enter_par_id"].tolist()
	num_participants = df.shape[0] - 2

	# sets participant id as index of df.
	df.set_index("enter_par_id", inplace=True)

	indexer_list = df.loc["(For Experimenter) Please Enter Participant ID."].tolist()
	slice_points = get_slice_points(indexer_list)
	num_questions = count_survey_questions(slice_points)
	questions_equal = check_num_questions(num_questions)
	if questions_equal:
		survey_length = num_questions[0]
		print(f"The Survey was {survey_length} questions long.")
		q_measures = get_q_measures(survey_length)
		print(f"The experiment so far has had {num_participants} participant(s).")
	else:
		print("Something must've happened.")
		sys.exit()

	for index, row in df.iterrows():
		if index.isnumeric():
			par_id = index

			list_row = row.tolist()
			head_cir = list_row.pop(0)

			if len(list_row) % survey_length == 0:
				task_num = int(len(list_row) / survey_length)
				csv_data = []
				for x in range(0, task_num - 1):
					start_cell = (survey_length * x)
					end_cell = (start_cell + 8)
					task_answers = list_row[start_cell:end_cell]
					task_answers.insert(0, f"Task{x + 1}")
					csv_data.append(task_answers)
				make_c_files(par_id, csv_data, q_measures)

			else:
				print("Inconsistent number of questions. Exiting Program.")
				sys.exit()


if __name__ == "__main__":
	# cols not needed in qualtrics export.
	col_to_drop = ["ResponseID", "ResponseSet", "IPAddress", "StartDate",
				   "EndDate", "RecipientLastName",	"RecipientFirstName",
				   "RecipientEmail", "ExternalDataReference", "Finished",
				   "Status", "LocationLatitude", "LocationLongitude",
				   "LocationAccuracy"]
	slice_prompt = "(For Experimenter) Please select the corresponding task number referring to the task the particip..."
	main(col_to_drop, slice_prompt)
