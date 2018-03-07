import requests
import zipfile
import json
import io
import sys

def main():
    """Qualtrics API request. Edited slightly for better error handling. For
    more information on what this file is doing see the documentation at:
    https://api.qualtrics.com/docs/response-exports

    Args:
        None

    Returns:
        .csv export of all current survey data."""

    # setting user parameters.
    try:
    # replace address below with .txt file where your API key is stored.
        with open ("/Users/trevorgrant/api_tokens/syrqual.txt") as in_file:
            apiToken = in_file.read()[:-1]
    except FileNotFoundError:
        print("ERROR: Unable to locate an API token. Please alter 'get_qualtrics.py'",
              ": line 21 to the current location of API token. Please refer"
              " to the documentation if you are confused by this message.")
        sys.exit()

    # instructions for finding your survey ID are located at:
    # https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/
    surveyId = "SV_9BLyhlbhdzb77r7"
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
    print(downloadRequestResponse.text)

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
    main()
