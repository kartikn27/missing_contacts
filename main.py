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
        self.df_contacts = pd.read_csv(self.contacts_file)


    def get_sector_codes(self, sector_name):
        return self.df_codes[self.df_codes['2017 NAICS US Title'] == sector_name]['2017 NAICS US   Code'].values[0]


    def get_required_sector_codes(self, sector_name_list):
        sector_code_list = []
        temp_codes = []
        required_sector_codes = []
        for sector in sector_name_list:
            sector = sector.rstrip(',')
            sector_code_list.append(str(self.get_sector_codes(sector)))
        for code in sector_code_list:
            if '-' in code:
                temp_codes.append(code.split('-')[0])
                temp_codes.append(code.split('-')[1])
                sector_code_list.remove(code)
            required_sector_codes = sector_code_list + temp_codes
        return required_sector_codes


    def get_sector_name(self, code):
        return self.df_codes[self.df_codes['2017 NAICS US   Code'] == code]['2017 NAICS US Title'].values[0]


    def get_attributes_payload(self, contact):
        return {'first_name': contact['first_name'],
                'last_name': contact['last_name'],
                'email': contact['email'],
                'company_name': contact['company_name'],
                'industry_name': self.get_sector_name(contact['naics_sector'])}


    def start_post_contacts(self, required_sector_codes):
        df_10 = self.df_contacts.head(10)
        for index, row in df_10.iterrows():
            contacts_sector = str(row['naics_sector'])
            if contacts_sector.startswith(required_sector_codes[0]) or contacts_sector.startswith(
                    required_sector_codes[1]) or contacts_sector.startswith(
                required_sector_codes[2]) or contacts_sector.startswith(required_sector_codes[3]):
                self.create_attributes_relationships(row)


    def create_attributes_relationships(self, contact):
        attributes_payload = self.get_attributes_payload(contact)
        print(attributes_payload)
        # relationships_payload = get_relationships_payload(contact)
        # print(relationships_payload)
        # print(' ------ ----- ------')
        # contact_object = Contact(attributes_payload, relationships_payload)
        # post_contact_payload(contact_object)


if __name__ == "__main__":
    sys.argv.pop(0)
    required_sectors = sys.argv
    print(required_sectors)
    mc = MissingContacts(CODES_FILE, CONTACTS_FILE, required_sectors)
    required_sector_codes = mc.get_required_sector_codes(required_sectors)
    mc.start_post_contacts(required_sector_codes)










