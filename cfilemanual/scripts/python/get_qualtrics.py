import requests
import zipfile
import json
import io
import os
import sys
import time

from inputmanager import InputManager


def get_survey_information(apiToken, dataCenter="ca1"):
    """Prints a list of the current survey names and corresponding Ids and asks
    the user which survey they want to recieve an export from.

    Args:
        apiToken(str): A string of characters that allows allows authentication
        when querying the Qualtrics API.
        dataCenter(str): Data center arguement for Qualtrics API.
    Returns:
        surveyID(str): A unique ID corresponding the to survey the user wants to
        retreieve survey responses for.
        Bool(False): If a surveyId isn't selected or found."""

    baseUrl = f"https://{dataCenter}.qualtrics.com/API/v3/surveys"

    headers = {
        "x-api-token": apiToken,
        }

    response = requests.get(baseUrl, headers=headers)
    try:
        survey_info = json.loads(response.text)['result']['elements']
    except KeyError:
        print(json.loads(response.text))
        print("You are presenting an invalid API token to qualtrics. "
              "Please make sure that your API token exactly matches"
              "the token listed on the Qualtrics account and try again.")
        sys.exit()

    print("\nBelow are the surveys listed under your qualtrics account:\n")
    print("-" * 80)
    if len(survey_info) == 0:
        print("There are no surveys associated with your Qualtrics account.")
        print("Quitting this program.. .. ..")
        sys.exit()

    for i, survey in enumerate(survey_info):
        print(f"{i + 1}. - Survey Name: {survey['name']}")
        print(f"Survey ID: {survey['id']}")
        print("-" * 80)

    prompt = ("Which survey would you like to export? \n(indicate the survey by typing the number listed next to the survey): ")
    survey_response = InputManager.get_numerical_input(prompt, (len(survey_info)))
    surveyId = survey_info[survey_response - 1]['id']
    if surveyId:
        prompt = "Would you like to save this as your default survey? \n(Answering yes will save the id to '/.ids/surveyid.txt')"
        ans = InputManager.get_yes_or_no(prompt)
        if ans:
            if not os.path.exists(f"{os.getcwd()}/.ids/"):
                os.mkdir(f"{os.getcwd()}/.ids/")
            with open (f"{os.getcwd()}/.ids/surveyid.txt", "w") as out_file:
                out_file.write(surveyId)
        return surveyId
    return False


def get_survey_id(apiToken):
    """Attemps to find surveyId in a local file. If it cannot it calls
    'get_survey_information'.

    Args:
        apiToken(str): A string of characters that allows allows authentication
        when querying the Qualtrics API.
    Returns:
        surveyID(str): A unique ID corresponding the to survey the user wants to
        retreieve survey responses for.
        Bool(False): If a surveyId isn't selected or found.
    Rasies:
        FileNotFoundError: if there is currently not a file that stores the surveyId."""

    try:
        with open(f"{os.getcwd()}/.ids/surveyid.txt") as in_file:
            surveyId = in_file.read()
            return surveyId
    except FileNotFoundError:
        print("ERROR: Unable to locate '/ids/surveyid.txt'.")
        surveyId = get_survey_information(apiToken)
        if surveyId:
            return surveyId
        return False


def get_api_fpath():
    """Allows user to manually import filepath that and contains their API token.

    Args:
        None
    Returns:
        api_fpath(str): location of the file containing user's API key.
        Bool (False): If user does not want to manually enter the filepath."""

    ans = InputManager.get_yes_or_no("Would you like to manually enter the filepath where your API token is located?: (Y/n): ")

    if ans:
        fpath = InputManager.get_valid_fpath("Please enter a valid filepath: ")
        return fpath

    return False


def get_api_token():
    """Attempts to locate a file that contains the user's API Token for their
    Qualtrics account.

    Args:
        None
    Returns:
        apiToken(str): A string of characters that allows allows authentication
        when querying the Qualtrics API.
    Rasies:
        FileNotFoundError: If there is no file with the API key in it, or if the
        file is in the wrong place. This function rasies the above and quits the
        program."""

    api_fpath = "/home/mindlab/cfilemanual/.api_token.txt"

    try:
    # replace address below with .txt file where your API key is stored.
        with open (api_fpath) as in_file:
            # [2:-1] removes extra whitespace.
            apiToken = in_file.read()[2:-1]
            return apiToken
    except FileNotFoundError:
        print("\n ERROR: Unable to locate an API token. \n")
        while True:
            api_fpath = get_api_fpath()
            if api_fpath:
                try:
                    with open (api_fpath) as in_file:
                        apiToken = in_file.read()[:-1]
                        return apiToken
                except:
                    print("ERROR: Unable to locate an API token. Please alter 'get_qualtrics.py'",
                          ": line 25 to the current location of API token. Please refer"
                          " to the documentation if you are confused by this message.\n")
                    break
            print("ERROR: Unable to locate an API token. Please alter 'get_qualtrics.py'",
                  ": line 126 to the current location of API token. Please refer"
                  " to the documentation if you are confused by this message.\n")
            break

        sys.exit()


def main(surveyId, apiToken, fileFormat="csv", dataCenter="ca1"):
    """Qualtrics API request. Edited slightly for better error handling. For
    more information on what this file is doing see the documentation at:
    https://api.qualtrics.com/docs/response-exports

    Args:
        surveyID(str): A unique ID corresponding the to survey the user wants to
        retreieve survey responses for. instructions for finding your survey ID are located at:
        https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/
        apiToken(str): A string of characters that allows allows authentication
        when querying the Qualtrics API.
    Returns:
        .csv export of all current survey data."""

    # Setting static parameters
    requestCheckProgress = 0
    progressStatus = "in progress"
    baseUrl = f"https://{dataCenter}.qualtrics.com/API/v3/responseexports/"
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
        }

    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl,
                                               data=downloadRequestPayload,
                                               headers=headers)
    progressId = downloadRequestResponse.json()["result"]["id"]

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while requestCheckProgress < 100 and progressStatus is not "complete":
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + progressId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers,
                                       stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")
    print('Complete')


if __name__ == "__main__":
    apiToken = get_api_token()
    surveyId = get_survey_id(apiToken)
    if not apiToken or not surveyId:
        print("ERROR: Missing either apiToken or surveyId. Cannot generate export.")
        sys.exit()
    main(surveyId, apiToken)
