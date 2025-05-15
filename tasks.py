import time
from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF

@task
def maria_task():
    """This is sample task for python robocorp"""
    browser.configure(
        slowmo=100,

    )
    open_browser()
    logIn()
    
    # fill_the_data()
    download_excel_file()
    fill_data_with_excel()
    take_screenshot()
    export_to_pdf()


    logOut()

def open_browser():
    #This is opening a browser using goto function
    browser.goto("https://robotsparebinindustries.com/")

def logOut():
    #Keep wait for the 10 sec in the brower before close
    time.sleep(10)
    page = browser.page()
    page.click("button:text('Log out')")
    print("Log out success")

def logIn():
    #Login the browser
    page= browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")

def fill_the_data():
    #Fill data based on the table
    # fill fun use the manually fill data
    # Drop down list select using  select_option
    page = browser.page()
    page.fill("#firstname", "Amal")
    page.fill("#lastname", "Aman")
    page.select_option("#salestarget", "15000")
    page.fill("#salesresult", "123")
    page.click("button:text('Submit')")

def download_excel_file():
    #Download excel file using the link, The overwrite is not allowed to again downaloding
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)

def fill_data_with_excel():
    #Read excel file and fill in the sale form
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet= excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()
    for row in worksheet:
        fill_and_submit_form(row)

def fill_and_submit_form(sales_rep):
    #Fill the form based on the excel sheet
    page=browser.page()
    page.fill("#firstname", sales_rep["First Name"])
    page.fill("#lastname", sales_rep["Last Name"])
    page.select_option("#salestarget", str(sales_rep["Sales Target"]))
    page.fill("#salesresult", str(sales_rep["Sales"]))
    page.click("button:text('Submit')")

def take_screenshot():
    """The robocorp.browser module provides the page.screenshot() function to help us with this step.
      We give it a path where to save the image file. 
      This function will take a screenshot of the current view."""
    page = browser.page()
    page.screenshot(path="output/salesSummary.png")

def export_to_pdf():
    # Creating a pdf report as per the web report(html)
    page = browser.page()
    pdf=PDF()
    sales_results_html = page.locator("#sales-results").inner_html()
    pdf.html_to_pdf(sales_results_html,"output/salesReport.pdf")




   

