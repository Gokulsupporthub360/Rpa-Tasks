from robocorp.tasks import task
from robocorp import browser
# from RPA.Excel.Application import Application
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
import os
import time
from RPA.Excel.Files import Files


# app = Application()
page = browser.page()
selenium = Selenium()
http = HTTP()
file = Files()

url = "https://rpachallenge.com/"
download_link = "https://rpachallenge.com/assets/downloadFiles/challenge.xlsx"
first_name = '//input[@ng-reflect-name="labelFirstName"]'
last_name = '//input[@ng-reflect-name="labelLastName"]'
email = '//input[@ng-reflect-name="labelEmail"]'
company_name = '//input[@ng-reflect-name="labelCompanyName"]'
role = '//input[@ng-reflect-name="labelRole"]'
phone = '//input[@ng-reflect-name="labelPhone"]'
address ='//input[@ng-reflect-name="labelAddress"]'
files = "C:/Users/Nimda/Documents/Rpa/Python/Rpa Task/Data/challenge.xlsx"
sheetname="Sheet1"
submit = '//input[@type="submit"]'


@task
def rpa_task():
    """
    1. open browser
    2. get excel file
    3. fill the data
    4. when complete then set complete status else incomplete
    """
    open_browser()
    # excel_download()
    write_status_col(files)
    read_excel(sheetname)
    # close_application()

def open_browser():
    """Open browser"""
    browser.goto(url)
    time.sleep(5)
    browser.configure(
        slowmo=20000
    )

def excel_download():
    """
    Download the excel file and add to a new folder
    """
    download_folder = os.path.join(os.getcwd(), "Data")
    os.makedirs(download_folder, exist_ok=True)
    http.download("https://rpachallenge.com/assets/downloadFiles/challenge.xlsx", download_folder, overwrite=True)

def write_status_col(files):
    """
    To write the col
    """
    # file.open_application(visible=True)
    file.open_workbook(files)
    file.set_active_worksheet(sheetname)
    file.set_cell_value(row=1, column=8, value="Status")
    file.set_cell_value(row=1, column=9, value="Reason")
    
    

# def close_application():
#     file.save_workbook()
    # file.quit_application()

def read_excel(sheet):
    """Read the excel"""

    datas = file.read_worksheet_as_table(sheet, header=True)
    file.set_active_worksheet(sheetname)
    row_num = 2

    for data in datas:
        success, reason = filling_page(data)
        status = "Completed" if success else "Incompleted"
        file.set_cell_value(row=row_num, column=8, value=status)
        file.set_cell_value(row=row_num, column=9, value=reason if not success else " ")
        row_num+=1

    file.save_workbook()

    file.close_workbook()



def filling_page(data):
    try:
        page.locator(first_name).fill(data['First Name'])
        page.locator(last_name).fill(data['Last Name'])
        page.locator(email).fill(data['Email'])
        page.locator(company_name).fill(data['Company Name'])
        page.locator(role).fill(data['Role in Company'])
        page.locator(phone).fill(str(data['Phone Number']))
        page.locator(address).fill(data['Address'])
        time.sleep(2)
        page.click(submit)
        return True, ""
    except Exception as e:
        print("The error is ,", e)
        return False, str(e)



