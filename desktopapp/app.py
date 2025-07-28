from robocorp.tasks import task
from RPA.Desktop import Desktop
from RPA.Excel.Files import Files
import pytesseract
import time

app = Desktop()
excel = Files()

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

input_file = "C:/Users/Gokul/Documents/RPA_Python/desktopapp/Input/DoubleUI-Transactions.xlsx"

cashIn_label_xpath = "Images/DoubleUi/cashIn_label.png"
onusCheck_path = "Images/DoubleUi/onUscheck.png"
notOnusCheck_path = "Images/DoubleUi/not_on_us_check.png"
accept_path = "Images/DoubleUi/accept.png"
cashInbox_path = "Images/DoubleUi/cashInbox.png"
transaction_path = "Images/DoubleUi/transaction_action.png"
account_path = "Images/DoubleUi/account.png"
deposite_path = "Images/DoubleUi/deposite.png"

double_app = "C:/Users/Gokul/Downloads/Input Methods and Input activities_Part 1/DoubleUI/DoubleUI.exe"


@task
def double():
    """This is the process to be interact the double ui application"""
    try:
        app.close_application("C:/Users/Gokul/Downloads/Input Methods and Input activities_Part 1/DoubleUI/DoubleUI.exe")
    except:
        pass

    try:
        app.open_application(double_app)
        time.sleep(5)
        datas = read_excel()

        deposite_region = app.find_element(f"image:{deposite_path}")
        app.click(deposite_region)

        row = 2
        col = 3
        col_acc =4
        

        excel.open_workbook(input_file)
        excel.set_active_worksheet("Sheet1")
        excel.set_cell_value(row=1, column=4, value="Account Number")
        excel.save_workbook()

        
        #Itrating the excel data
        for index,data in enumerate(datas):
            print(f"Row index is {index+1}: {data}")

            #Transaction Number
            region = app.find_element(f"image:{transaction_path}")
            print(f"The region of the transaction is {region}")

            moved_region = app.move_region(region, 92, 0)
            tansaction_text = app.read_text(moved_region)
            print("Tranaction Number is ",tansaction_text)

            # Account number

            account_region = app.find_element(f"image:{account_path}")
            print(f'The region of account number {account_region}')

            moved_region = app.move_region(account_region, 85, 0)
            print("Moved....",moved_region)
            app.take_screenshot("output/dt3.png", moved_region)

            # wider_region = app.resize_region(moved_region, 282,174,343,195) 
            wider_region = app.resize_region(moved_region,left=9, right=20, bottom=10)
            account_text = app.read_text(wider_region)

            
            excel.set_cell_value(row=row, column=col, value= tansaction_text)
            excel.set_cell_value(row=row, column=col_acc, value= account_text)
            excel.save_workbook()
            row +=1


            # Cash in
            cashIn_locator = app.find_element(f"image:{cashIn_label_xpath}")
            app.click_with_offset(cashIn_locator,x=100)
            app.type_text(str(data['CashIn']), enter=True)

            # On us check
            onUsCheck_locator = app.find_element(f"image:{notOnusCheck_path}")
            app.click_with_offset(onUsCheck_locator, x=100)
            app.type_text(str(data['OnUsCheck']), enter=True)
            time.sleep(5)
            print('Success')

            #Apply button
            locator = app.find_element(f"image:{accept_path}")
            print(locator)
            app.click(locator)
            # app.click(f"image:{accept_path}")
            # app.click(f"image:{accept_path}")
        excel.close_workbook()
        app.close_application(double_app)
        print("The application is closed successfully")


    except Exception as e:
        print("The error is the ",e)

def read_excel():
    """This function is used for the read the excel data"""
    excel.open_workbook(input_file)
    excel.set_active_worksheet("Sheet1")
    data = excel.read_worksheet_as_table(header=True)
    excel.close_workbook()
    return data