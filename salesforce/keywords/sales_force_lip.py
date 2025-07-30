from RPA.Salesforce import Salesforce
from RPA.JSON import JSON
import os

salesforce = Salesforce()
json = JSON()

root_file = os.getcwd()
cred = "salesforce_cred"

def autherized_saleforce():
    path_file = os.path.join(root_file, cred)
    auth = json.load_json_from_file(path_file)
    salesforce.auth_with_token(
        username=auth.username,
        password=auth.password,
        api_token=auth.token
    )