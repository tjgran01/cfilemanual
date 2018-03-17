import pandas as pd
import os
import getpass

import get_qualtrics
from inputmanager import InputManager

def check_if_download():
	if not os.path.exists(f"{os.getcwd()}/MyQualtricsDownload/"):
		apiToken = get_qualtrics.get_api_token()
		surveyId = get_qualtrics.get_survey_id(apiToken)
		get_qualtrics.main(surveyId, apiToken)

def get_experiment_id(par_id):

	exper_id = par_id[:2]
	return exper_id

def make_c_files(par_ids):
	par_ids.pop(0)
	exper_id = get_experiment_id(par_ids[0])

	if not os.path.exists(f"./experiment_{exper_id}_cfiles/"):
		os.mkdir(f"./experiment_99{exper_id}_cfiles/")

	for par_id in par_ids:
		with open(f"./experiment_99{exper_id}_cfiles/{par_id}_FNIRS_conditions_s1.csv", "w") as out_csv:
			out_csv.write()

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

	slice_points = []
	for i, row in enumerate(indexer_list):
		if row == slice_prompt:
			slice_points.append(i)

	list_of_tasks = []
	for index, row in df.iterrows():
		if index.isnumeric():
			list_row = row.tolist()
			task_list = []
			for i, cell in enumerate(list_row):
				for val in slice_points:
					if i == val:
						print(cell)


	# make_c_files(par_ids)


if __name__ == "__main__":
	# cols not needed in qualtrics export.
	col_to_drop = ["ResponseID", "ResponseSet", "IPAddress", "StartDate",
				   "EndDate", "RecipientLastName",	"RecipientFirstName",
				   "RecipientEmail", "ExternalDataReference", "Finished",
				   "Status", "LocationLatitude", "LocationLongitude",
				   "LocationAccuracy"]
	slice_prompt = "(For Experimenter) Please select the corresponding task number referring to the task the particip..."
	main(col_to_drop, slice_prompt)
