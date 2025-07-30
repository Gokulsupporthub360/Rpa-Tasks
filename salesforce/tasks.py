from robocorp.tasks import task
# from keywords.sales_force_lip import sales_force_lip
from RPA.Salesforce import Salesforce
from RPA.JSON import JSON
from RPA.Tables import Tables
import os
import re

salesforce = Salesforce()
json = JSON()
tables = Tables()

root_file = os.getcwd()
cred = "salesforce_cred.json"
acc_import = "Dataset/account_import.json"
acc_mapp = "Dataset/account_mapping.json"

input_obj = os.path.join(root_file, acc_import)
mapping_obj = os.path.join(root_file, acc_mapp)


# sales_auth = sales_force_lip()

@task
def sales_forces():
    """This function is interact with sales force api"""
    autherized_saleforce()

    dict = {
        "Name" : "Demo",
        "NumberOfEmployees" : 100,
        "Type" : "Prospect", 
        "Industry" : "Engineering",
        "Ownership" : "Private",
        "BillingCountry" : "India",
        "BillingCity" : "Kerala",
        "Phone" : 9999999999

    }

    obj_id = create_new_account(dict)

    read_account(obj_id)

    update_dict = {
        "Website" : "www.demo123.com",
        "Tradestyle": "Akhil",
        "Phone" : 9999999900
    }
    # update_account_object(obj_id, update_dict)
    delete_user(obj_id)

def autherized_saleforce():
    path_file = os.path.join(root_file, cred)
    auth = json.load_json_from_file(path_file)
    salesforce.auth_with_token(
        username=auth["username"],
        password=auth["password"],
        api_token=auth["token"]
    )


def create_new_account(accountInformattion):
    """This function create a new user"""
    try:
        status = salesforce.create_salesforce_object(object_type="Account",object_data=accountInformattion)
        print(type(status))
        print(status)
        print("New account is created")
        return status["id"]
    except Exception as e:
        if "DUPLICATES_DETECTED" in str(e):
            print("Duplication detected extracting existing id")
            match = re.search(r"'Id':'([^']+)'", str(e))
            if match:
                exsiting_id = match.group(1)
                print(f"Using exsting account Id: {exsiting_id}")
                return exsiting_id
            else:
                print("Duplication found but can't extraction")
        else:
            raise


def read_account(account_id):
    """Read the account """
    acc_obj = salesforce.get_salesforce_object_by_id(object_type="Account", object_id=account_id)
    print(acc_obj)

def update_account_object(acccount_id, account_info):
    """This function is used to update the user values."""
    status = salesforce.update_salesforce_object(object_type="Account", object_id=acccount_id, object_data=account_info)
    print(status)

def delete_user(account_id):
    """This function is used to delete the user"""
    status = salesforce.delete_salesforce_object(object_type="Account", object_id=account_id)
    print(status) # will print True or False
    print("deleted successfully")


def create_new_contact(account_id, account_info):
    account_info["AccountId"] = account_id
    status = salesforce.create_salesforce_object(object_type="Contact", object_data=account_info)
    print(status)
    return status["id"]

def create_new_product(product_info):
    """This function is add a new product"""
    status = salesforce.create_salesforce_object(object_type="Product2", object_data=product_info)
    print(status)
    return status["id"]

def create_price_book_entry(bookdata):
    """This is function to add the price book"""
    status = salesforce.create_salesforce_object(object_type="PriceBookEntry", object_data=bookdata)
    print(status)


@task
def saleforce_app_data_loader():
    """This is function is used to mapping in the large number of data set
    which means that i have large data set which keys are anything that not depeneds on the API, 
    Those keys are mapped to orginal key set """
    autherized_saleforce()
    data_loader()


def data_loader():
    """Insert the bulk amound of data"""
    status = salesforce.execute_dataloader_insert(
        input_object=acc_import,
        mapping_object=acc_mapp,
        object_type="Account")
    print(status)

    #Will show the whether the success data into the table
    success_table = salesforce.get_dataloader_success_table()
    tables.write_table_to_csv(success_table, "output/success.csv")

    #Will show the whether the error data in to the table
    errot_table = salesforce.get_dataloader_error_table()
    tables.write_table_to_csv(errot_table, "output/error.csv")

@task
def salesforec_app_account_and_contact_relastion():
    """This function is the connect a conatct number in to the account holder"""
    autherized_saleforce()

    dict = {
        "Name" : "Demo with contact",
        "NumberOfEmployees" : 100,
        "Type" : "Prospect", 
        "Industry" : "Engineering",
        "Ownership" : "Private",
        "BillingCountry" : "India",
        "BillingCity" : "Kerala",
        "Phone" : 9999999999

    }
    obj_id = create_new_account(dict)



    c_dict = {
        "Salutation" : "Mr",
        "FirstName" : "Amal",
        "LastName" : "Krishna",
        "MobilePhone" : 7895125410,
        "Email" : "amla@gamil.com"
    }

    create_new_contact(obj_id, c_dict)

@task
def saleforce_product():
    """This function is doing related product based"""
    autherized_saleforce()
    pricebook = salesforce.get_pricebook_entries()
    print(pricebook)
    # bookid = salesforce.get_pricebook_id("RobotEye")
    # print(bookid)
    add_new_product()

def add_new_product():
    p_dict = {
        "Name" : "RobotEye",
        "ProductCode" : "AYO123",
        "Description" : "This is small electronicchip",
        "IsActive" : True,
    }

    p_id = create_new_product(p_dict)
    print(p_id)

    prcbk_id = salesforce.get_pricebook_id("Standard Price Book")
    print(prcbk_id)


    # Create  a new price book entry for the new product with a standard price 
    pr_dict = {
        "Pricebook2Id" : prcbk_id,
        "IsActive" : True,
        "Product2Id" : p_id,
        "UnitPrice" : 500
    }

    stdbook = create_price_book_entry(pr_dict)
    print(stdbook)

    prcbk_id = salesforce.get_pricebook_id(pricebook_name="Standard")
    pr_dict = {
        "Pricebook2Id" : prcbk_id,
        "IsActive" : True,
        "Product2Id" : p_id,
        "UnitPrice" : 300,
        "UseStandardPrice" : False
    }

    create_price_book_entry(pr_dict)

    product_list = salesforce.get_products_in_pricelist(pricebook_name="Wholesale")
    print(product_list)


@task
def create_opperunity():
    """This is about opperunity"""
    autherized_saleforce()
    opp_id = salesforce.create_new_opportunity(
        account_name="Demo with contact",
        opportunity_name="Robot Eye sell",
        stage_name="Prospecting",
        close_date="2024-05-20"
    )

    status = salesforce.add_product_into_opportunity(
        product_name="RobotEye",
        quantity=10,
        opportunity_id=opp_id,
        pricebook_name="Standard Price Book",
        custom_total_price=500
    )
    print("opperunity status", status)

@task
def saleforce_app_query_task():
    """This function is about the get details in the query based."""
    autherized_saleforce()
    product_table = salesforce.salesforce_query_result_as_table(sql_string=
                                                                "SELECT Name, Productcode, Description FROM Product2 WHERE Name LIKE 'ROB%'"
    )
    tables.write_table_to_csv(product_table, "output/query.csv")

