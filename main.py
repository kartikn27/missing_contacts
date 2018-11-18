import pandas as pd
import math
import requests
import json
import sys
from lib.contact import Contact
from lib.constants import *

class MissingContacts(object):

    def __init__(self, codes_file, contacts_file, required_sectors):
        self.codes_file = codes_file
        self.contacts_file = contacts_file
        self.sector_name_list = required_sectors
        self.df_codes = pd.read_excel(self.codes_file)


    def get_sector_codes(self, sector_name):
        return self.df_codes[self.df_codes['2017 NAICS US Title'] == sector_name]['2017 NAICS US   Code'].values[0]


    def get_required_sector_codes(self, sector_name_list):
        sector_code_list = []
        temp_codes = []
        required_sector_codes = []
        for sector in sector_name_list:
            sector = sector.rstrip(',')
            print('=====SECTOR ===== ', sector)
            sector_code_list.append(str(self.get_sector_codes(sector)))
        for code in sector_code_list:
            if '-' in code:
                temp_codes.append(code.split('-')[0])
                temp_codes.append(code.split('-')[1])
                sector_code_list.remove(code)
            required_sector_codes = sector_code_list + temp_codes
        return required_sector_codes


if __name__ == "__main__":
    sys.argv.pop(0)
    required_sectors = sys.argv
    print(required_sectors)
    mc = MissingContacts(CODES_FILE, CONTACTS_FILE, required_sectors)
    print(mc.get_required_sector_codes(required_sectors))








