
# Google Sheets Pilot Import for RotorHazard FPV Timing System
This plugin allows race directors to import pilots directly from Google Sheets or Google Forms(indirectly) into RotorHazard. Before being able to import pilots, race directors are required to follow a few steps to obtain credentials from Google which allows Rotorhazard and Google sheets to connect. These steps only need to be done once.

## Setup Steps
There are 3 steps to get this plugin going. First is to create the credential file and service account in Google Cloud. This only needs to be done once. Step 2 is to simply grant access to the service account from the Google Sheets and finally step 3 is to install this plugin itself and most importantly copy the Google credentials.json file into the Plugin folder within RotorHazard. Steps are listed below. There is an installation guide video available as well at the following link:

https://youtu.be/eYu2nZQnT6c

### 1. Google Cloud Project - 1 time setup.
1. Visit https://cloud.google.com
2. Create a new project and give it a name. It could be any name such as your chapter or club name. e.g. _My Drone Race Club_
3. With newly created project selected, click on APIs and Services
4. In the top search bar, search for **Google Drive API** and press enter
5. Click **enable** Google Drive
6. In the top search bar, search for **Google Sheets API** and press enter
7. Click **enable** Google Sheet
8. On the left side bar, click on **"Credentials"**.
9. Click on **Manage Service Accounts** on the right followed by **"+ CREATE SERVICE ACCOUNT"** at the top
10. Enter a service account name and thats it. Copy the generated service email address and click done. Step 2 and 3 are not required
    
    <img width="590" alt="google-pilot-03" src="https://github.com/Barracuda-Technologies/rh-google-pilot-import/assets/17153870/485dde55-7689-40d1-a463-4df384a2d09b">

12. Once back on the main page, the service account status will be Enabled. On the far right, click on the 3 dots and select manage keys
13. Click on Add Key -> Create New Key -> Select JSON -> Create.
14. Save the newly created JSON file on desktop and rename it to "credentials.json"

### 2. Google Sheets
1. Head over to https://drive.google.com
2. Create a Google sheets anywhere.
3. Give it a name. Any name. e.g: Pilot Registration Form
4. For the current version of the plugin, create columns called "Name" and "Callsign". These are mandatory. Any other columns can be created but wont be picked up by the plugin.
5. Hit the "Share" button at the top right corner and enter teh service email address from step 10 in section 1 above.
6. Hit done and that's.

### 3. The plugin 
1. Install through the "Community Plugins" area within RotorHazard. Alternately, copy the `pilots_from_google_sheets` directory from inside `custom_plugins` into the plugins directory of your RotorHazard data directory.
2. Copy over the "credentials.json" file from step 14 in section 1 above to the plugin folder.
3. Restart the Pi and a new section called Google Pilots will appear in the Format page.

<img width="899" alt="google-pilot-02" src="https://github.com/Barracuda-Technologies/rh-google-pilot-import/assets/17153870/cbdc7b7f-d9a4-4235-a67e-51bb62aea984">

## User Guide
1. Create a new google sheet page or a new Google Form which sends results to a Google Sheet. Give the Google Sheet a name or take note of the given name. e.g: ***Registration Form***
2. Make sure there are columns called:
   * Name
   * Callsign

3. The following columns are optional and the plugin will pull the values from this sheet if the fields are available in RotorHazard. Some fields are created by other plugins e.g. MultiGP ID =  https://github.com/i-am-grub/MultiGP_Toolkit
   * Pilot color
   * Pilot Phonetic
   * Pilot Country
   * Pilot MultiGP ID
   * Pilot FPVScores UUID

3. Click on the **Share** button on the top right corner of the sheet and enter the service email address created in Section 1 of the Setup Guide above. Click done.
4. Start up RotorHazard and head over the format page. Under hte panel **Google Pilot Import**, enter the name of the Google sheet created in step 1. e.g: ***Registration Form***
5. Hit the import button and the pilot names and callsigns will be imported automatically.

> [!NOTE]
> If name and callsign already exist in the RotorHazard database, this pilot will be skipped. Only new pilots will be added. No removal is done. 
