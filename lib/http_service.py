from lib.constants import Constants
import requests
import json

class HttpService(object):

    """
    Summary
    -------
    Method invokes a GET request to find the contact information by his email

    Parameters
    ----------
    arg1: string
        email of the supervisor

    Returns
    -------
    JSON
        response obtained from the GET request
    """
    def get_supervisor_info(self, supervisor_email):
        header_obj= { Constants.CONTACT_URL_API_HEADER_KEY : Constants.CONTACT_URL_API_HEADER_VALUE }
        r = requests.get(
            Constants.CONTACT_EMAIL_URL + supervisor_email,
            headers = header_obj)
        response = json.loads(r.text)
        return response

    """
    Summary
    -------
    Method invokes a POST request to add new contact

    Parameters
    ----------
    arg1: object/dict
        attributes payload
    arg2: object/dict
        relationships payload        

    Returns
    -------
    JSON
        response obtained from the POST request
    """

    def post_contact_info(self, attributes_payload, relationships_payload):
        header_obj = { Constants.CONTACT_URL_API_HEADER_KEY: Constants.CONTACT_URL_API_HEADER_VALUE,
                      Constants.CONTENT_TYPE_HEADER_KEY: Constants.CONTENT_TYPE_JSON_VALUE }
        payload_obj = {
                        "data": {
                                "type": "contacts",
                                "attributes": attributes_payload,
                                "relationships": {
                                    "supervisor": { "data": relationships_payload }
                                }
                        }
                    }
        r = requests.post(
            Constants.CONTACT_POST_URL,
            data = json.dumps(payload_obj),
            headers = header_obj
        )
        response = json.loads(r.text)
        return response
