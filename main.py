import pandas as pd
import math
import sys
import xlrd
from validate_email import validate_email
from lib.contact import Contact
from lib.constants import Constants
from lib.http_service import HttpService

# Main class MissingContacts handles the all the work flows for the application
class MissingContacts(object):

    """
    constructor for the class
    Initialized objects are :
      1. self.codes_files: path to the sector codex XLS file
      2. self.contacts_file:  path to the missing contacts csv file
      3. self.sector_name_list: list of sectors passed as command line arguments
      4. self.df_codes: Pandas DataFrame for sector codes info
      5. self.df_contacts: Pandas DatFrame for contacts info
    """
    def __init__(self, codes_file, contacts_file, required_sectors):
        self.codes_file = codes_file
        self.contacts_file = contacts_file
        self.sector_name_list = required_sectors
        self.df_codes = pd.read_excel(self.codes_file)
        self.df_contacts = clean_dataframe(pd.read_csv(self.contacts_file))

    """
    Parameters
    ----------
    arg1: int
        name of the sector
    
    Returns
    -------
    int
        code of the sector
    """
    def get_sector_codes(self, sector_name):
        if self.df_codes[self.df_codes['2017 NAICS US Title'] == sector_name].empty:
            print(' ---- SECTOR CODE NOT FOUND FOR ' + sector_name + ' ---- ')
            return None
        else:
            return self.df_codes[self.df_codes['2017 NAICS US Title'] == sector_name]['2017 NAICS US   Code'].values[0]

    """
    Parameters
    ----------
    arg1: list/Array
        list of all the names of the required sectors

    Returns
    -------
    list/Array:    
        list of all the codes of the required sectors
    """
    def get_required_sector_codes(self, sector_name_list):
        sector_code_list = []
        temp_codes = []
        required_sector_codes = []
        for sector in sector_name_list:
            code = self.get_sector_codes(sector)
            if code is not None:
                sector_code_list.append(str(self.get_sector_codes(sector)))
        for code in sector_code_list:
            if '-' in code:
                temp_codes.append(code.split('-')[0])
                temp_codes.append(code.split('-')[1])
                sector_code_list.remove(code)
            required_sector_codes = sector_code_list + temp_codes
        return required_sector_codes

    """
    Parameters
    ----------
    arg1: int
        code of the sector

    Returns
    -------
    string
        name of the sector
    """
    def get_sector_name(self, code):
        return self.df_codes[self.df_codes['2017 NAICS US   Code'] == code]['2017 NAICS US Title'].values[0]

    """
    Summary
    -------
    Generates an object for the attributes, which is part of the POST contact payload 

    Parameters
    ----------
    arg1: object
        one contact object/Dictionary        

    Returns
    -------
    Object/dictionary which will be part of the attributes object in POST contact request
    """
    def get_attributes_payload(self, contact):
        if(validate_email(contact['email'])):
            return {"first_name": clean_str(contact['first_name']),
                    "last_name": clean_str(contact['last_name']),
                    "email": contact['email'],
                    "company_name": clean_str(contact['company_name']),
                    "industry_name": clean_str(self.get_sector_name(contact['naics_sector']))}

    """
    Summary
    -------
    Generates an object for the relationships, which is part of the POST contact payload 
    If the supervisor email is NULL or blank, empty object is returned
    If supervisor email exists, a GET request is invoked to find the `id`
        If `id` is found and object with `id` is returned
        Else blank object is returned 
    
    Parameters
    ----------
    arg1: object
        one contact object/Dictionary        

    Returns
    -------
    Object/dictionary which will be part of the relationships object in POST contact request
    """
    def get_relationships_payload(self, contact):
        if isinstance(contact['supervisor_email'], (float)) and math.isnan(contact['supervisor_email']):
            return {}
        elif contact['supervisor_email'] == '':
            return {}
        else:
            response = HttpService.get_supervisor_info(self, contact['supervisor_email'])
            if len(response['data']) > 0:
                return {'id': response['data'][0]['id']}
            else:
                return {}

    """
    Summary
    -------
    This method loops through all the rows for required sectors in the CSV 
    It checks if the sector to be looked start with the sector ids of the sectors passed through argv
    It checks for all the valid sector ids which are obtained from sector passed through argv
    If the sector id in csv STARTSWITH any of the valid sector ids, it is further processed
    
    Parameters
    ----------
    arg1: list
        list of required parent sector ids    
    """
    def start_post_contacts(self, required_sector_codes):
        #df_10 = self.df_contacts.head(10)
        print(' .... MISSING CONTACTS ARE BEING ADDED TO THE SERVER .... ')
        for index, row in self.df_contacts.iterrows():
            contacts_sector = str(row['naics_sector'])
            if contacts_sector.startswith(tuple(required_sector_codes)):
                self.create_attributes_relationships(row)
        print(' .... MISSING CONTACTS HAVE BEEN ADDED TO THE SERVER .... ')

    """
    Summary
    -------
    Method calls the method which creates attributes and relationships payload 
    Further is instantiates the Contact class and assigns the obtained attributes and relationships
     
    Parameters
    ----------
    arg1: object
        one contact object/Dictionary    
    """
    def create_attributes_relationships(self, contact):
        attributes_payload = self.get_attributes_payload(contact)
        relationships_payload = self.get_relationships_payload(contact)
        contact_object = Contact(attributes_payload, relationships_payload)
        self.post_contact_payload(contact_object)

    """
    Summary
    -------
    Method passes the attributes and relationships obtained from Contact getter to POST contact service
    
    Parameters
    ----------
    arg1: Contact Class Object
        one Contact object
    """
    def post_contact_payload(self, contact_object):
        attributes = contact_object.get_attributes()
        relationships = contact_object.get_relationships()
        response = HttpService.post_contact_info(self, attributes, relationships)
        print('Contact with email ' +  response['data']['attributes']['email'] + ' has been added to the server!')

"""
Summary
-------
Removes the leading and trailing whitespaces from the string 

Parameters
----------
arg1: string

Returns
-------
string
"""
def clean_str(value):
    return value.strip()

"""
Summary
-------
Returns the Pandas dataframe by removing the rows where the email id NULL 
    
Parameters
----------
arg1: Pandas dataframe        

Returns
-------
Pandas dataframe
"""
def clean_dataframe(df):
    return pd.DataFrame.dropna(df, subset=['email'])


"""
ENTRY POINT OF THE APPLICATION
required sectors are received from command line arguments
MissingContacts is instantiated
"""
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(' ---- NO SECTOR NAMES ARE PASSED AS COMMAND LINE ARGUMENTS ---- ')
        sys.exit()
    else:
        sys.argv.pop(0)
        required_sectors = sys.argv
        required_sectors = [clean_str(sector) for sector in required_sectors]
        mc = MissingContacts(Constants.CODES_FILE, Constants.CONTACTS_FILE, required_sectors)
        required_sector_codes = mc.get_required_sector_codes(required_sectors)
        mc.start_post_contacts(required_sector_codes)

