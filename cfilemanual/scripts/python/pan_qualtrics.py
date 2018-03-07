import pandas as pd
import os

import get_qualtrics

col_to_drop = ["ResponseID", "ResponseSet", "IPAddress", "StartDate", "EndDate",
	           "RecipientLastName",	"RecipientFirstName", "RecipientEmail",
               "ExternalDataReference",	"Finished", "Status", "LocationLatitude",
               "LocationLongitude",	"LocationAccuracy"]

get_qualtrics.main()
file_name = str(os.listdir(f"{os.getcwd()}/MyQualtricsDownload/"))[2:-2]
df = pd.read_csv(f"{os.getcwd()}/MyQualtricsDownload/{file_name}")
df.drop(col_to_drop, axis=1, inplace=True)

num_participants = df.shape[0] - 2

for i, row in df.iterrows():
    if i > 1:
        participant_id = row[1]
        print(participant_id)

print(num_participants)
