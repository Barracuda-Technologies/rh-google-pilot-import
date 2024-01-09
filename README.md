# Google Sheets Pilot Import for RotorHazard FPV Timing System
This plugin allows race directors to import pilots directly from Google Sheets or Google Forms(indirectly) into RotorHazard. Before being able to import pilots, race directors are required to follow a few steps to obtain credentials from Google which allows Rotorhazard and Google sheets to connect. These steps only need to be done once.

## Setup Steps
### 1. Google Cloud Project - 1 time setup.
1. Visit https://cloud.google.com
2. Create a new project and give it a name
3. With newly created project selected, click on APIs and Services
4. In the top search bar, search for **Google Drive** and press enter
5. Enable Google Drive
6. In the top search bar, search for **Google Sheets** and press enter
7. Enable Google Sheet
8. On the left side bar, click on **"Credentials"**.
9. Click on Manage Service Accounts on the right followed by **"+ CREATE SERVICE ACCOUNT"** at the top
10. Enter a service account name and thats it. Copy the generated service email address and click done. Step 2 and 3 are not required
11. Once back on the main page, the service account status will be Enabled. On the far right, click on the 3 dots and select manage keys
12. Click on Add Key -> Create New Key -> Select JSON -> Create.
13. Save the newly created JSON file on desktop and rename it to credentials.json

### 2. Google Sheets
1. Head over to https://drive.google.com
2. Create a Google sheets anywhere.
3. Give it a name. Any name. e.g: Pilot Registration Form
4. For the current version of the plugin, create collumns called "Name" and "Callsign". These are mandatory. Any other collumns can be created but wont be picked up by the plugin.
5. Hit the "Share" button at the top right corner and enter teh service email address from step 10 in section 1 above.
6. Hit done and that's.

### 3. The plugin
1. SSH into the timer.
2. Copy the plugin files into the ``` ~/RotorHazard/src/server/plugins``` directory with the following cmd lines or download latest from: https://github.com/Barracuda-Technologies/rh-google-pilot-import/releases
```
cd ~
sudo rm -r RotorHazard/src/server/plugins/googlepilot
wget https://github.com/Barracuda-Technologies/rh-google-pilot-import/archive/refs/tags/v1.0.0.zip -O temp.zip
unzip temp.zip
mv rh-google-pilot-import-1.0.0 RotorHazard/src/server/plugins/googlepilot
rm temp.zip
```
4. Intall a required library for Google Sheets to work in the timer with the following cmd line:
```
pip install gspreads
```
4. Copy over the credentials.json file from step 13 in section 1 above to the newly created plugin folder.
5. Restart the Pi and a new section called Google Pilots will appear in the Format page. 
