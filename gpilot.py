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
        ui.register_panel("gpilot-import", "Google Sheets Pilot Import", "format")
        ui.register_quickbutton("gpilot-import", "gpilot-import-button", "Import", self.import_pilot)
        gpilot_form_name = UIField(name = 'gpilot-form-name', label = 'Google Sheet Name', field_type = UIFieldType.TEXT, desc = "The name of the Google Sheet. With spaces and all. For now please make sure there is 1 col called Name and 1 called Callsign on the first sheet.")
        fields = self._rhapi.fields
        fields.register_option(gpilot_form_name, "gpilot-import")

    def import_pilot(self, args):
        self._rhapi.ui.message_notify("Beginning Google Sheets Import....")
        credentials = self.get_credentials()
        filename = self._rhapi.db.option("gpilot-form-name")
        filenamenotempty = True if filename else False
        if credentials is not None and filenamenotempty:
            gc = gspread.service_account_from_dict(credentials)
            try:
                
                sh = gc.open(filename)
                all_records = sh.sheet1.get_all_records()
                self.save_pilot(all_records)
            except Exception as x:
                print(x)
                self._rhapi.ui.message_notify("Google Sheet Import Error - See log")
                self.logger.warning("Google Sheet not found" + str(x))

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
            self._rhapi.ui.message_notify("Credentials file not found. Please refer documentation.")
            data = None
            return data

    def save_pilot(self, all_records):
        
        for idx, record in enumerate(all_records):
            pilotnumber = str(idx + 1)
            pilotname = record["Name"] if (record["Name"] and record["Name"] is not None) else "~Pilot "+ pilotnumber + " Name"
            pilotcallsign = record["Callsign"] if (record["Callsign"] and record["Callsign"] is not None) else "~Callsign "+ pilotnumber
            pilot = {
                "name": pilotname,
                "callsign": pilotcallsign
            }
            if "Phonetic" in record:
                pilotphonetic = record["Phonetic"] if (record["Phonetic"] and record["Phonetic"] is not None) else " "
                pilot["phonetic"] = pilotphonetic
            if "Colour" in record:
                pilotcolor = record["Colour"] if (record["Colour"] and record["Colour"] is not None) else "#ff0055"
                pilot["color"] = pilotcolor
            if "MGP ID" in record:
                pilotmgpid = record["MGP ID"] if (record["MGP ID"] and record["MGP ID"] is not None) else " "
            if "FPVS UUID" in record:
                pilottracksideid = record["FPVS UUID"] if (record["FPVS UUID"] and record["FPVS UUID"] is not None) else " "
            if "Country" in record:
                pilotcountry = record["Country"] if (record["Country"] and record["Country"] is not None) else " "

            existingpilot = self.check_existing_pilot(pilot)
            if not existingpilot:
                self._rhapi.db.pilot_add(name=pilot["name"],
                                         callsign=pilot["callsign"],
                                         phonetic=pilot["phonetic"],
                                         color=pilot["color"])
                self.logger.info("Added pilot " + pilot["name"] + "-" + pilot["callsign"] + " with id:"
                                 + str(self._rhapi.db.pilots[-1].id))
                current_id = self._rhapi.db.pilots[-1].id

                contains_mgp_id = False
                contains_fpvs_uuid = False
                contains_country = False
                for i in range(len(self._rhapi.fields.pilot_attributes)):
                    if self._rhapi.fields.pilot_attributes[i].name == 'mgp_pilot_id':
                        contains_mgp_id = True
                    if self._rhapi.fields.pilot_attributes[i].name == 'fpvs_uuid':
                        contains_fpvs_uuid = True
                    if self._rhapi.fields.pilot_attributes[i].name == 'country':
                        contains_country = True
                pilot_attributes = {}
                if contains_mgp_id and "MGP ID" in record:
                    pilot_attributes["mgp_pilot_id"] = pilotmgpid
                if contains_fpvs_uuid and "FPVS UUID" in record:
                    pilot_attributes["fpvs_uuid"] = pilottracksideid
                if contains_country and "Country" in record:
                    pilot_attributes["country"] = pilotcountry
                self._rhapi.db.pilot_alter(current_id, attributes=pilot_attributes)
        self._rhapi.ui.message_notify("Import complete, please refresh.")
        self._rhapi.ui.broadcast_pilots()

    def check_existing_pilot(self,pilot):
        localpilots = self._rhapi.db.pilots
        existing = False
        for localpilot in localpilots:
            if (localpilot.name == pilot["name"] and localpilot.callsign == pilot["callsign"]):
                existing = True

        return existing
        