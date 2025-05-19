from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
import os
from RPA.Excel.Files import Files
import time

@task
def rpa_challange():
    #This is the rpa challenge task
    browser.configure(
        slowmo=100,
    )

    open_browser()
    download_excel()
    read_excel()
    take_screenshot()
    close_browser()

def open_browser():
    #Open the rpa challange 
    browser.goto("https://rpachallenge.com/")
    
   

def download_excel():
    #Download excel file and add specific path
    http = HTTP()
    #Crate a new folder
    download_folder = os.path.join(os.getcwd(), "Data")
    os.makedirs(download_folder, exist_ok=True)
    file_path = os.path.join(download_folder, "Challenge.xlsx")
    http.download("https://rpachallenge.com/assets/downloadFiles/challenge.xlsx", file_path, overwrite=True)


def fill_the_data_with_excel(data):
    #Fill the form with excel data
    page = browser.page()
    
    page.locator('//input[@ng-reflect-name="labelFirstName"]').fill(data["First Name"])
    page.locator('//input[@ng-reflect-name="labelLastName"]').fill(data["Last Name"])
    page.locator('//input[@ng-reflect-name="labelCompanyName"]').fill(data["Company Name"])
    page.locator('//input[@ng-reflect-name="labelRole"]').fill(data["Role in Company"])
    page.locator('//input[@ng-reflect-name="labelAddress"]').fill(data["Address"])
    page.locator('//input[@ng-reflect-name="labelEmail"]').fill(data["Email"])
    page.locator('//input[@ng-reflect-name="labelPhone"]').fill(str(data["Phone Number"]))
    page.click("//input[@type='submit']")

def read_excel():
    #Read and store excel data
    excel = Files()
    page=browser.page()
    filePath = os.path.join(os.getcwd(), "Data", "Challenge.xlsx")
    excel.open_workbook(filePath)
    worksheet = excel.read_worksheet_as_table("Sheet1", header=True)
    excel.close_workbook()
    page.click("button:text('Start')")

    for row in worksheet:
        fill_the_data_with_excel(row)


def close_browser():
    page = browser.page()
    time.sleep(10)

def take_screenshot():
    page= browser.page()
    page.screenshot(path="output/FinalOut.png")




    




    
