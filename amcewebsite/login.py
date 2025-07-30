from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Desktop import Desktop
from RPA.Excel.Files import Files
from robocorp import vault
from RPA.Tables import Tables

# from RPA.Robocorp.Vault import Vault
import pytesseract
from bs4 import BeautifulSoup
import time

warning_path = "Images/warring.png"
ok_path = "Images/Ok.png"






pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe" 

# VAULT = vault()
app = Desktop()
browser = Selenium()
excel = Files()
tables = Tables()


url = "https://acme-test.uipath.com/login"
workItem = "https://acme-test.uipath.com/work-items"
logout_url = "https://acme-test.uipath.com/logout"
# url = vault.get_secret('amce_url')

email_id = "id:email"
password_id = "id:password"

login_xpath = "//button[normalize-space(.)='Login']"
dashboard_xpath = "//h1[normalize-space(.)='Dashboard']"
workload_xpath = "//h1[normalize-space(.)='Work Items']"

email = "hello13@gmail.com"
pwd = "12345678"



@task
def login_amce():
    """The login to the amce"""
    try:

        # _secret = vault.get_secret("acme_Credential")
        browser.open_chrome_browser(url, maximized=True)
        time.sleep(3)
        browser.input_text(email_id, email)
        browser.input_text(password_id, pwd)
        browser.click_element(login_xpath)


        
        try:
           
            element_change = app.find_element(f"image:{warning_path}")
            if element_change:
                # Sort the pop "Change your password"
                ok_element = app.find_element(f"image:{ok_path}")
                app.click(ok_element)
                time.sleep(2)
                print("ok")

            else:
                pass

            workload()
            save_excel()
            logout()

        except Exception as e:
            print("The error is ", e)


    except Exception as e:
        print('The error is the ',e)


def workload():
    """This is function is about the workload"""
    try:
        browser.wait_until_element_is_visible(dashboard_xpath, timeout=10)
        browser.go_to(url=workItem)
        print("The url goes to the Work item")


    except Exception as e:
        print("The error is the ", e)

def extract_datatable():
    """This function is used to the extract data table to excel data"""
    try:
        all_data = []
        header = []
        page_number=1
        while True:
            print(f"The extracting data of page no..{page_number} ")

            html = browser.get_element_attribute("(//table)[1]", "outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table")

            if not table:
                print("The page have no table")
                break

            if not header:
                header_row = table.find("tr")
                header = [th.text.strip() for th in header_row.find_all("th")]

            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                row_data = [cell.text.strip() for cell in cells]
                all_data.append(row_data)

            #Try next button if available
            try:
                next_button = browser.find_element("//a[@aria-label='Next »']")
                if "disabled" in browser.get_element_attribute(next_button, "class"):
                    break
                browser.click_element(next_button)
                browser.wait_until_element_is_visible("//table[@class='table']", timeout=10)
                time.sleep(1)
                page_number+=1
        
            except Exception as e:
                print("No more pages found")
                break
        return[all_data, header]

    except Exception as e:
        print("The error message of the extracting data is ", e)


def save_excel():
    """This is the save excel as extracted data"""
    try:
        data = extract_datatable()
        all_data = data[0]
        header = data[1]
        data_table = tables.create_table(all_data, columns=header)
        excel.create_workbook("output/workbookItem123.xlsx", sheet_name="Work Item")
        excel.append_rows_to_worksheet(content=data_table, header=True)
        excel.delete_columns("A")
        excel.save_workbook()
        print("The data book is saved")
    except Exception as e:
        print("The error is the ", e)


def logout():
    """This is the function for the logout the website"""
    try:

        browser.go_to(url=logout_url)
        browser.close_browser()
    
    except Exception as e:
        print("The error of the log out is the ", e)
    



        


