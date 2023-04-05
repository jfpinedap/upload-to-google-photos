# Upload photos/videos to Google Photos

This is a simple python script to upload photos or videos to Google Photos.


## Obtain the OAuth 2.0 credentials and configure the OAuth consent screen for uploading files to Google Photos for a desktop app:

### Step 1: Create a Project in the Google Cloud Console

To start, go to the Google Cloud Console and create a new project.

### Step 2: Enable the Google Photos API

Once you've created your project, navigate to the API & Services Dashboard and click on the "+ Enable APIs and Services" button.

Search for the "Google Photos Library API" and enable it.

### Step 3: Set up OAuth 2.0 Credentials

Navigate to the Credentials tab in the API & Services Dashboard and click on the "+ Create Credentials" button.

Select "OAuth client ID" and choose "Desktop App" as the Application Type.

Enter a name for the OAuth 2.0 client ID, and add the authorized JavaScript origins and redirect URIs. Since this is a desktop app, you can set the authorized JavaScript origins and redirect URIs to "http://localhost".

### Step 4: Configure the OAuth Consent Screen

In the Credentials tab, click on the "OAuth consent screen" tab and fill out the required fields. This includes the app name, the authorized domains, and the privacy policy URL. You can also customize the logo and other details if you'd like.

### Step 5: Obtain the Client ID and Secret

Once you've completed the above steps, you'll be given a client ID and secret. Save these credentials in a secure location.

## Perform the .env and place it in the main folder

```.env
CLIENT_ID=<Your Client ID>
CLIENT_SECRET=<Your Client secret>
FILE_FOLDER_NAME=files
```
Notice that the images or videos to upload must be into the subfolder `files`

## Create the venv and install requirements
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Execute the upload app
```bash
python upload_photos.py
```
This will open a Google sign-in page in the user's default web browser. Once the user logs in, they will be prompted to grant your app permission to access their Google Photos.

---
That's all, I hope that helps!
