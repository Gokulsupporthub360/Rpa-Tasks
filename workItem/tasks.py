from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from bs4 import BeautifulSoup
from RPA.Excel.Files import Files
from RPA.Tables import Tables
import time


selenium = Selenium()
files = Files()
tables = Tables()

email = "hello13@gmail.com"
pwd = "12345678"


url ="https://acme-test.uipath.com/login"
login_xpath = "//h1[contains(normalize-space(), 'Login')]"
email_xpath = "//input(id:email)"
password_xpath = "//input(id:password)"
login_xpath  = "//button[@type='submit']"
dashboard_xpath = "//h1[contains(normalize-space(), 'Dashboard')]"
work_item_xpath = "//button[contains(normalize-space(), 'Work Items')]"
work_item_heading_xpath = "//h1[contains(normalize-space(), 'Work Items')]"

@task
def workItem():
    """
    Work item table download from the website
    """
    open_website()
    navigate_work_item()
    save_excel()
    filter_data()

def open_website():
    """
    Open website 
    """
    selenium.set_selenium_speed("100")
    selenium.open_chrome_browser(url, maximized=True)
    selenium.wait_until_element_is_visible(login_xpath, timeout=10)
    print("Login page found")
    selenium.input_text_when_element_is_visible("id:email", email)
    selenium.input_text_when_element_is_visible("id:password",pwd)
    selenium.click_button(login_xpath)

def navigate_work_item():
    """
    Navigate to the work item
    """
    selenium.wait_until_element_is_visible(dashboard_xpath, timeout=10)
    time.sleep(5)
    selenium.click_element(work_item_xpath)
    time.sleep(10)
    print("navigate work item success")

def extracting_table():
    """
    Extracting table 
    """

    selenium.wait_until_element_is_visible(work_item_heading_xpath, timeout=10)
    print("Work item is present")

    all_data = []
    headers = []
    page_number = 1

    while True:
        print(f"processing page {page_number}...")
        html = selenium.get_element_attribute("(//table)[1]", "outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table')
        print("table found success")

        if not table:
            print("No table found")
            break

        #Extract header once 
        if not headers:
            header_row = table.find("tr")
            headers = [th.text.strip() for th in header_row.find_all("th")]

        #Extract row
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            row_data = [cell.text.strip() for cell in cells]
            all_data.append(row_data)

        # Try to click "Next »" if available
        try:
            next_button = selenium.find_element("//a[@aria-label='Next »']")
            if 'disabled' in selenium.get_element_attribute(next_button, "class"):
                break   # If no next button then stop

            selenium.click_element(next_button)
            selenium.wait_until_element_is_visible("//table[@class='table']", timeout=10)
            page_number+=1
        except Exception:
            print(f"No more paper found")
            break
        # print(all_data)

    return all_data, headers

def save_excel():
    """
    Getting data from extracted data and use for excel activities
    """
    all_data, header = extracting_table()
    data_table=tables.create_table(all_data, columns=header)
    print(type(data_table))
    files.create_workbook("output/workitem.xlsx", sheet_name="work")
    files.append_rows_to_worksheet(data_table, header=True)
    files.save_workbook()
    files.close_workbook()
    # filtered_data = tables.filter_table_by_column(data_table, column="Type", operator="==", value="WI1")
    # print(filtered_data)
    

    # print(worksheet)
def filter_data():
    files.open_workbook("output/workitem.xlsx")
    files.set_active_worksheet("work")
    work_sheet =files.read_worksheet_as_table(header=True)
    # filter_data = tables.filter_table_by_column(work_sheet, column="WIID", operator="==", value="105457521")
    # print(filter_data)


@task
def navigate_to_vendor():
    """Navigate to the vendor deatils"""
    open_website()
    time.sleep(10)
    selenium.click_element("//button[contains(normalize-space(),'Vendors')]")
    time.sleep(5)
    selenium.click_element("//a[normalize-space()='Search for Vendor']")
    time.sleep(10)
    vendor_xpath = "//h1[contains(normalize-space(), 'Vendors')]"
    selenium.wait_until_element_is_visible(vendor_xpath,timeout=10)
    selenium.click_element("id:buttonShowAll")
    time.sleep(6)
    save_excel_vendor()
    each_vendor_search()


def vendor_details():
    """Extract vendor table"""
    
    # vendor_hending_xpath = "//h1[contains(normalize-space(), 'Vendors-Search Results')]"
    # selenium.wait_until_element_is_visible(vendor_hending_xpath, timeout=10)

    try:
        all_data = []
        header = []
        
        html = selenium.get_element_attribute("//table[@class='table']", "outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")

        if not table:
            print("No table found")

        #Extract header
        if not header:
            header_row = table.find("tr")
            header= [th.text.strip() for th in header_row.find_all("th")]
        
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            row_data = [cell.text.strip() for cell in cells]
        
            all_data.append(row_data)
        return all_data, header
    except Exception as e:
        print("The problem is ", e)




def save_excel_vendor():
    """Save these data to the excel sheet"""
    time.sleep(2)
    all_data , header = vendor_details()
    data_table = tables.create_table(all_data, columns=header)


    files.create_workbook("output/vendor list.xlsx")
    files.append_rows_to_worksheet(data_table, header=True)
    files.save_workbook()
    files.close_workbook()


def each_vendor_search():
    """Get the details from the table and add data to the sheet"""
    vendor_back = "//a[normalize-space()= 'Vendors']"

    files.open_workbook("output/vendor list.xlsx")
    worksheet = files.read_worksheet_as_table("Sheet", header=True)

    selenium.click_element(vendor_back)

    for workid in worksheet:
        try:
            selenium.input_text(("id:vendorTaxID"),workid["Tax ID"])
            selenium.click_element("id:buttonSearch")
            time.sleep(5)
            print("success")
            append_excel_sheet(workid["Vendor"])
            time.sleep(2)
            selenium.click_element(vendor_back)
        except Exception as e:
            print("No more vendor present")
            break

def fetch_each_vendor_deatils():
    """Fetch all data from the each vendor"""
    try:
        all_data =[]
        header = []
        row_data = []

        html = selenium.get_element_attribute("//table[@class='table']", "outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")


        if not table:
            print("There is no table")
        
        if not header:
            header_row = table.find("tr")
            header = [th.text.strip() for th in header_row.find_all("th")]
        
        try:
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                row_data = [cell.text.strip() for cell in cells]
                all_data.append(row_data)
        except Exception:
            print("Their is no row")
        

        return all_data, header
    except Exception as e:
        print("The error is,", e)


def append_excel_sheet(sheet_name):
    """Append each details to the sheet"""

    all_data , header = fetch_each_vendor_deatils()

    if not all_data:
        print("No data found")
        return


    data_table = tables.create_table(all_data, columns=header)
    files.open_workbook("output/vendor list.xlsx")
    files.create_worksheet(sheet_name)
    files.append_rows_to_worksheet(data_table,name=sheet_name, header=True)
    files.save_workbook()
    files.close_workbook()

    
    


