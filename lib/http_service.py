from lib.constants import Constants
import requests
import json

class HttpService(object):

    def get_supervisor_info(self, supervisor_email):
        header_obj= { Constants.CONTACT_URL_API_HEADER_KEY : Constants.CONTACT_URL_API_HEADER_VALUE }
        r = requests.get(
            Constants.CONTACT_EMAIL_URL + supervisor_email,
            headers = header_obj)
        response = json.loads(r.text)
        print("RESPONSE ...... ", response)
        print("RESPONSE STATUS...... ", r.status_code)
        return response

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
        return r.status_code
