import pandas as pd
import os
import getpass

import get_qualtrics

# cols not needed in qualtrics export.
col_to_drop = ["ResponseID", "ResponseSet", "IPAddress", "StartDate", "EndDate",
	           "RecipientLastName",	"RecipientFirstName", "RecipientEmail",
               "ExternalDataReference",	"Finished", "Status", "LocationLatitude",
               "LocationLongitude",	"LocationAccuracy"]

if not os.path.exists(f"{os.getcwd()}/MyQualtricsDownload/"):
	apiToken = get_qualtrics.get_api_token()
	surveyId = get_qualtrics.get_survey_id(apiToken)
	get_qualtrics.main(surveyId, apiToken)

file_name = str(os.listdir(f"{os.getcwd()}/MyQualtricsDownload/"))[2:-2]
df = pd.read_csv(f"{os.getcwd()}/MyQualtricsDownload/{file_name}")
df.drop(col_to_drop, axis=1, inplace=True)
df.drop(1, axis=0, inplace=True)

print(df)

# num_participants = df.shape[0] - 2
#
# for i, row in df.iterrows():
#     if i > 1:
#         participant_id = row[0]
#         print(participant_id)
#
# print(num_participants)
