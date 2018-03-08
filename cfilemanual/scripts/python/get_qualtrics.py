import requests
import zipfile
import json
import io
import sys

from inputmanager import InputManager

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

    try:
    # replace address below with .txt file where your API key is stored.
        with open ("/Users/trevorgrant/api_tokens/syrqual.txt") as in_file:
            # [:-1] removes extra whitespace.
            apiToken = in_file.read()[:-1]
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
                  ": line 25 to the current location of API token. Please refer"
                  " to the documentation if you are confused by this message.\n")
            break

        sys.exit()


def main(surveyId, apiToken):
    """Qualtrics API request. Edited slightly for better error handling. For
    more information on what this file is doing see the documentation at:
    https://api.qualtrics.com/docs/response-exports

    Args:
        surveyID(str): A unique ID corresponding the to survey you want to retreieve
        survey responses for. instructions for finding your survey ID are located at:
        https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/
        apiToken(str): A string of characters that allows allows authentication
        when querying the Qualtrics API.
    Returns:
        .csv export of all current survey data."""

    # setting export parameters
    fileFormat = "csv"
    dataCenter = 'ca1'

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
    surveyId = "SV_9BLyhlbhdzb77r7"
    apiToken = get_api_token()
    main(surveyId, apiToken)
