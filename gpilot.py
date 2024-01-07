import json
import requests
import logging
import gspread

from RHUI import UIField, UIFieldType

class Gpilot():

    credentials = {
        "type": "service_account",
        "project_id": "rotorhazard",
        "private_key_id": "5d5f9b046d5e8d0d36c0235633d4fc8c996bde9b",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2PSv/ywZRAiw2\n6Hhff/XhODOZRzahafwyfQM3LCWic+68y3KZxWN7B0kYf5CXRK9L86N9WMAgB4UY\njeNo6e7ep1nWqJNXMFTNpAs9YC+8JfiqcFiMvh6UOq4yEmbbrzpZ1wJi/4m307PT\nYbrDdnTUXnkNvbSCXLqbW81gGzHVYQyw7KzzVViACUg4HCUHTLUIlTaLdbE7oVe9\nE0O+hcz1K98hTUyWEYy/++cBIUrOvo34ESrH9LQi4KZCLC89kXLNJtZzPxDdpxyx\nBBEA3BE8UZzpkHRqWu9stw2Y8CpxONJ1GFctB1wFJd5amodZqtAkal1JFgsGI/2N\nmY4X2WXlAgMBAAECggEAHmJ+poyERhd1pcYG4+1i4qVLPSA5hJo2OXjMg3Nx5u8r\nfADz352go4+oaVRDmGUUUTaTKMAWcICweVKW+xQeBrOib/71ahEd4peaZCZYbydp\nmYlXykecs5xBFQoqajCCKx6FQFpY7PR4RCNET3i9q/cAegEKSr4JQwQAbyi5m1jl\naIijXINtT2ZNVDA5P2lJyi6CHyFoNMSCdjkooKrMb1xk3ZJrmh+JS7HL7Z6nX9DZ\nfMA+pvnbvEkcXnXu/SWqy/DRKm5bJvkKWg5ZJ+51QYayuOjgyGTYqktW9plls3R0\noB1xew9lXKso7nSrDZgiXLB9ZOBpz5YVZE65nbdrdQKBgQD21p8eTAsD/WGvv3dg\nTME87IvWqbnO+inTOWzqHNJ+USRk7w8moqBWPkKaIBSXJQTXIgkKHPB4+py/p+oq\nHOr9hec2HNLOfUypSPRpWSgKhenOJkPOXUSOpYzQ+9AGqVajUc5dWL1Z75AK0SOv\nuEU2zDlOB7QUA+nKsDKBQdvJPwKBgQC9AL9fuSXJR9XlZeNbwWWOwOrXKclk3Sdp\nRgTi7M0fZ96c/OnZd/Ls0dKcknUxFitbebUcrhjayzBGqxJ/QcMos2D2UDPCnVsZ\nZJ/NvigPzZO6z63KB80j3IIKJp4DMhR1jLbbMmExMmnEaU6CrHNaNal0huYPd77l\nhOlWD+eD2wKBgED5X6sW8zNaqDMd4Ct+KMODtI+N37YmzYmnLQ83BQVxEHZtIvzV\nhAUPoHJ3jVP3z51dfSmnUnlV5prgdVgegpC3hZQN5EOsYdiRtpxgdpTGiTPViLWy\ngVBXLYj5L9oBCyg0aXDS4gzhbXYbdRxVEgsJmO/8QR+fpBPRa4nwrwz7AoGBAKYf\n9hYpIvFcVsGfYMvRnXZwUvp0HDSvvmhlxv2+rj0giybplpIzQC6v7rL4eFGA7vMk\ncvCWhfoqBnDXBRcdsnAf2uYlcJlqvhv/ugaZUZUyWNsml9awLLuMojBR6Sld52W7\nHS5lhdA8Q4MEHKH2+h0cdamauLR3yC7tODsRF6lpAoGBAKPCGfwfhTchWhg97qFK\nBS9a2q/14LvX8dMQERcNXe5n7xjzjS9IJQ3V9FuUZuLKH43+fJugGGBx2Ee7UbxR\nExrlRviYqJ8CdKU2vYdjhqrEZyrxWPwW9uNug99slR1H97yWDUSmX6+BTFeidcM/\np9g2hzeNTUp2WPlDsidIQJuE\n-----END PRIVATE KEY-----\n",
        "client_email": "rotorhazardform@rotorhazard.iam.gserviceaccount.com",
        "client_id": "104113660301695972942",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/rotorhazardform%40rotorhazard.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    def __init__(self,rhapi):
        self.logger = logging.getLogger(__name__)
        self._rhapi = rhapi
        

    def init_plugin(self,args):      
        print("starting up gpilot")
        self.init_ui(args)

    def init_ui(self,args):
        ui = self._rhapi.ui
        ui.register_panel("gpilot-import", "Google Pilots", "format")
        ui.register_quickbutton("gpilot-import", "gpilot-import-button", "Import", self.import_pilot)

    def import_pilot(self, args):
        gc = gspread.service_account_from_dict(self.credentials)
        sh = gc.open("Test Form (Responses)")
        all_records = sh.sheet1.get_all_records()
        self.save_pilot(all_records)

    def save_pilot(self, all_records):
        for record in all_records:
            pilot = {
                "name": record["Name"],
                "callsign": record["Callsign"]
            }
            existingpilot = self.check_existing_pilot(pilot)
            if not existingpilot:
                self.logger.info("Added pilot " + pilot["name"] + "-" + pilot["callsign"])
                self._rhapi.db.pilot_add(name=pilot["name"], callsign=pilot["callsign"])

    def check_existing_pilot(self,pilot):
        localpilots = self._rhapi.db.pilots
        existing = False
        for localpilot in localpilots:
            if (localpilot.name == pilot["name"] and localpilot.callsign == pilot["callsign"]):
                existing = True

        return existing
        