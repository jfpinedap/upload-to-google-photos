import json
import time

from decouple import config
from google.auth.transport.requests import AuthorizedSession
from google_auth_oauthlib.flow import InstalledAppFlow

from src.get_paths import get_file_paths
from src.log_conf import logger
from src.read_register import create_uploaded_images_report

# Get the values of .evn variables from the environment
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
file_folder_name = config("FILE_FOLDER_NAME")


register = {"uploaded": [], "error": []}

idx_from = 0
idx_to = -1
time_sleep = 1.8

# perform the image/photo path list
file_paths = (
    get_file_paths(file_folder_name)[idx_from:idx_to]
    if idx_to > idx_from
    else get_file_paths(file_folder_name)
)


# Set up the OAuth2 flow
appflow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
        }
    },
    scopes=["https://www.googleapis.com/auth/photoslibrary"],
)

# Get authorization from user
creds = appflow.run_local_server(port=0)

# Set up authorized session
authed_session = AuthorizedSession(creds)


def send_image(file_path: str):
    # Upload the image
    url = "https://photoslibrary.googleapis.com/v1/uploads"
    response = authed_session.post(
        url,
        data=open(file_path, "rb"),
        headers={
            "Content-type": "application/octet-stream",
            "X-Goog-Upload-Content-Type": "image/jpeg",
            "X-Goog-Upload-Protocol": "raw",
        },
    )

    # Create the media item
    url = "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"
    response = authed_session.post(
        url,
        json={
            "albumId": None,
            "newMediaItems": [
                {
                    "description": "",
                    "simpleMediaItem": {
                        "fileName": file_path,
                        "uploadToken": response.content.decode("utf-8"),
                    },
                }
            ],
        },
    )

    response_json = response.json()

    logger.info(response_json)
    if response_json:
        status = (
            response_json.get("newMediaItemResults")[0].get("status").get("message")
        )
        return status == "Success" or status == "OK"
    else:
        return False


if __name__ == "__main__":
    with open("total_register.json", "r") as f:
        total_register = json.load(f)

    uploaded_images = total_register.get("uploaded", [])

    for num, file_path in enumerate(file_paths, start=1):
        try:
            logger.info(f"File num: {num} - {file_path}")
            if file_path in uploaded_images:
                logger.info(f"This image has already updated: {file_path}")
                continue
            if send_image(file_path):
                key = "uploaded"
            else:
                key = "error"
            register[key].append(file_path)
            time.sleep(time_sleep)
        except Exception as e:
            logger.info(e)
            logger.info(f"Upload failed for file: {file_path}")
            register["error"].append(file_path)
            continue
        finally:
            with open(f"registers/register_{idx_from}-{idx_to}.json", "w") as f:
                # Use the json module to dump the list to the file
                json.dump(register, f)

    create_uploaded_images_report()
