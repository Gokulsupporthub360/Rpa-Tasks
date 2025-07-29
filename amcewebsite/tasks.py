from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from bs4 import BeautifulSoup
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.Desktop import Desktop
import time
import os

# os.environ["TESSERACT_CMD"] = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

excel = Files()
browser = Selenium()
tables = Tables()
app = Desktop()

url = "https://acme-test.uipath.com/login"
search_url = "acme-test.uipath.com/invoices/search"



userName = "hello13@gmail.com"
password = "12345678"

loginHead_xpath = "//h1[normalize-space(.)='Login']"
login_button = "//button[normalize-space(.)='Login']"
dashboard_xpath = "//h1[normalize-space(.)='Dashboard']"
invoice_head_xpath = "//h1[normalize-space(.)='Invoices']"
diaplay_all_invoice_button = "//button[normalize-space(.)='buttonShowAll']"
invoice_seach_xpath = "//h1[normalize-space(.)='Invoices-Search Results']"
invoice_searchResult_xpath = "//h1[normalize-space(.)='Invoices-Search Results']"

vendor_tax_id_xpath = "//table[@class='table']/tbody/tr[2]/td[2]"
invoice_item_xpath = "//table[@class='table']/tbody/tr[2]/td[3]"
total_xpath = "//table[@class='table']/tbody/tr[2]/td[4]"
date_xpath = "//table[@class='table']/tbody/tr[2]/td[5]"




login_id = "id:email"
password_id = "id:password"
diaplay_invoice_id = "id:buttonShowAll"
invoicenumber_id = "id:invoiceNumber"
searchButton_id = "id:buttonSearch"

sheet_path = "C:/Users/Gokul/Documents/RPA_Python/amcewebsite/workitem_input.xlsx"

error_path = "Images/Error.png"
ok_button = "Images/okButton.png"



@task
def amce_web():
    """Extract the invoice details"""
    login()
    select_search_invoice()
    # display_all_invoice()
    # search_all_invoice()
    excel.open_workbook(sheet_path)
    excel.set_active_worksheet("Sheet1")
    datas = excel.read_worksheet_as_table(header=True)
    # excel.close_workbook()
    updated_data = []

    for row in datas:
        invoice_number = row["Invoice Number"]
        search_invoice(invoice_number)
        extracted = extract_data()

        # Merge original row and new data
        row.update(extracted)
        updated_data.append(row)

    # Overwrite the worksheet with updated data
    excel.append_rows_to_worksheet(updated_data, header=True)
    excel.save_workbook()
    excel.close_workbook()


def login():
    """This function is used for the login the amce website"""
    browser.open_chrome_browser(url, maximized=True)
    browser.wait_until_element_is_visible(loginHead_xpath, timeout=10)
    browser.input_text(login_id, userName)
    browser.input_text(password_id, password)
    browser.click_element(login_button)
    time.sleep(5)
    app.highlight_elements(f"image:{error_path}")
    time.sleep(1)
    app.highlight_elements(f"image:{ok_button}")
    time.sleep(1)
    elemn = app.wait_for_element(f"image:{ok_button}", timeout=5, interval=0.5)
    app.click(elemn, action="double_click")
    time.sleep(1)
    region_string = "region:823,326,64,38"
    # result = app.read_text()
    # print(result)
    # time.sleep(1)
    # app.click(region_string, action="click")
    # print("click")
    # elem = app.find_elements(f"image:{ok_button}")
    # print(elem)

def select_search_invoice():
    """Search the invoice button"""
    # browser.wait_until_element_is_visible(dashboard_xpath, timeout=10)
    browser.go_to(search_url)

def search_invoice(invoiceNumber):
    """Search by the each invoice number"""
    browser.wait_until_element_is_visible(invoice_head_xpath, timeout=10)
    browser.input_text(invoicenumber_id,invoiceNumber)
    browser.click_element(searchButton_id)

def extract_data():
    """Extract all data using the invoice number"""
    # browser.wait_until_element_is_visible(invoice_searchResult_xpath)
    vendor_tax_id = browser.get_text(vendor_tax_id_xpath)
    invoice_item = browser.get_text(invoice_item_xpath)
    total = browser.get_text(total_xpath)
    date =browser.get_text(date_xpath)
    print(vendor_tax_id)
    print(invoice_item)
    print(total)
    print(date)
    select_search_invoice()
    return {
        "Vendor Tax ID": vendor_tax_id,
        "Invoice Item": invoice_item,
        "Total": total,
        "Date": date
    }



                                                        




def display_all_invoice():
    """This function is used for the get all invoice data"""
    browser.wait_until_element_is_visible(invoice_head_xpath, timeout=10)
    browser.click_element(diaplay_invoice_id)
    time.sleep(2)
    


def search_all_invoice():
    """Exctract all invoice data """
    # browser.wait_until_element_is_visible(invoice_seach_xpath, timeout=10)
    all_data = []
    header = []
    page_number = 1
    print(f"Processing page {page_number}...")
    html = browser.get_element_attribute("//table[1]", "outerHTML")
    soup = BeautifulSoup(html,  "lxml")
    table = soup.find("table")

    #If table not found
    if not table:
        print("This page have no page found please re check")
        # break

    # If no header
    if not header:
        header_row = table.find("tr")
        header = [th.text.strip() for th in header_row.find_all("th")]

    #Extract data
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        all_data.append(row_data)
    
    #Save to excel
    data_table = tables.create_table(all_data, columns=header)
    excel.create_workbook("output/workitem.xlsx", sheet_name="Sheet1")
    excel.append_rows_to_worksheet(data_table, header=True)
    excel.save_workbook()
    print('Data exctraction is completed')
    excel.close_workbook()
    # while True:
        # print(f"Processing page {page_number}...")
        # html = browser.get_element_attribute("//table[1]", "outerHTML")
        # soup = BeautifulSoup(html,  "lxml")
        # table = soup.find("table")

        # #If table not found
        # if not table:
        #     print("This page have no page found please re check")
        #     break

        # # If no header
        # if not header:
        #     header_row = table.find("tr")
        #     header = [th.text.strip() for th in header_row.find_all("th")]

        # #Extract data
        # for row in table.find_all("tr")[1:]:
        #     cells = row.find_all("td")
        #     row_data = [cell.text.strip() for cell in cells]
        #     all_data.append(row_data)
        
        # #Save to excel
        # data_table = tables.create_table(all_data, columns=header)
        # excel.create_workbook("output/workitem.xlsx", sheet_name="Sheet1")
        # excel.append_rows_to_worksheet(data_table, header=True)
        # excel.save_workbook()
        # print('Data exctraction is completed')
        # excel.close_workbook()










                                                        