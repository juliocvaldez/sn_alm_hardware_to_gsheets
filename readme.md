# Hardware Assets to Google Sheets Python function

This python script was authored by Julio Valdez and Marlan Mitchell and intends to **connect to a UCSB ServiceNow** instance, **export the alm_hardware** data and **push it to a Google Sheet** via REST APIs.

## Prerequisites

1. **Get ServiceNow OAuth credentials**:

   1. Create new Application Registry record in ServiceNow
   2. System OAuth > Application Registry
   3. New > Create OAuth API endpoint for external clients
   4. Name it Python - alm_hardware_to_gsheets
   5. Submit

2. **Create sn_config.json** with the following format:

   ```json
   {
     "USERNAME": "odbc.user",
     "PASSWORD": "<user's password>",
     "INSTANCE": "<sn_instance>",
     "CLIENT_ID": "<sn_client_id>",
     "CLIENT_SECRET": "<sn_client_secret>"
   }
   ```

3. **Get Google OAuth credentials**:

   1. Best to follow the latest instructions from [Google Sheets API docs](https://developers.google.com/sheets/api/guides/authorizing)
   2. Once the credentials have been created, navigate to APIs & Services > Credentials
   3. Click the download button on the right of the credential you created to download a JSON fiel
   4. Save the JSON file as "google_secret.json" into the ./creds directory

   Note: google_secret.json should have the following format:

   ```json
   {
     "installed": {
       "client_id": "<google_client_id>",
       "project_id": "<google_project_id>",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
       "client_secret": "<google_client_secret>",
       "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
     }
   }
   ```

4. **Use pip install** to import following libraries:

- pysnow
- pandas
- gspread_pandas
  ```terminal
    $ sudo pip install pysnow
  ```

## Run the script

1. Open the terminal in the root directory ./sn_alm_hardware_to_gsheets
2. Run the following:
   ```terminal
     $ sudo python main.py
   ```
