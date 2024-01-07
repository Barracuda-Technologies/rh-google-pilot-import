import json
import logging
import gspread
import os
from RHUI import UIField, UIFieldType

class Gpilot():

    CONST_CREDENTIALS = 'credentials.json'

    def __init__(self,rhapi):
        self.logger = logging.getLogger(__name__)
        self._rhapi = rhapi
        
    def init_plugin(self,args):      
        self.logger.info("Starting Google Pilot plugin")
        self.init_ui(args)

    def init_ui(self,args):
        ui = self._rhapi.ui
        ui.register_panel("gpilot-import", "Google Pilots", "format")
        ui.register_quickbutton("gpilot-import", "gpilot-import-button", "Import", self.import_pilot)
        gpilot_form_name = UIField(name = 'gpilot-form-name', label = 'Google Sheet Name', field_type = UIFieldType.TEXT, desc = "The name of the Google Sheet. With spaces and all.")
        fields = self._rhapi.fields
        fields.register_option(gpilot_form_name, "gpilot-import")

    def import_pilot(self, args):
        credentials = self.get_credentials()
        filename = self._rhapi.db.option("gpilot-form-name")
        filenamenotempty = True if filename else False
        if credentials is not None and filenamenotempty:
            gc = gspread.service_account_from_dict(credentials)
            try:
                
                sh = gc.open(filename)
                all_records = sh.sheet1.get_all_records()
                self.save_pilot(all_records)
            except:
                self.logger.warning("File not found")

    def get_credentials(self):
        here = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(here, self.CONST_CREDENTIALS)
        
        try:
            f = open(filename)
            data = json.load(f)
            f.close()
            return data
        except:
            self.logger.warning("Credentials file not found")
            data = None
            return data

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
        