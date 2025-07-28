from robocorp.tasks import task
from RPA.Desktop.Windows import Windows
from RPA.Desktop import Desktop
import time
import pytesseract




win = Windows()
app = Desktop()

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

appname = "DoubleUI"

cashIn_path = "Images/DoubleUi/cashin.png"
cashIn_label_xpath = "Images/DoubleUi/cashIn_label.png"
cashIn_box_path = "Images/DoubleUi/cashin.png"
onusCheck_path = "Images/DoubleUi/onUscheck.png"
notOnusCheck_path = "Images/DoubleUi/not_on_us_check.png"
accept_path = "Images/DoubleUi/accept.png"
cashInbox_path = "Images/DoubleUi/cashInbox.png"
transaction_path = "Images/DoubleUi/transaction_action.png"
tns_path = "Images/DoubleUi/tns_action.png"
number_path = "Images/DoubleUi/number.png"

region_tns_number = 690,350,760,332

@task
def double():
    try:
        app.close_application("C:/Users/Gokul/Downloads/Input Methods and Input activities_Part 1/DoubleUI/DoubleUI.exe")
    except:
        try:

            app.open_application("C:/Users/Gokul/Downloads/Input Methods and Input activities_Part 1/DoubleUI/DoubleUI.exe")
            time.sleep(5)

            locator = app.find_elements(f"image:{cashInbox_path}")
            print(locator)
            print("scuccess")

            locator = app.find_element(f"image:{cashIn_label_xpath}")
            print(locator)
            app.click_with_offset(f"image:{cashIn_label_xpath}", x=100)
            time.sleep(1)
            app.type_text("5000", enter=True)
            print("locator fofund")
            locator = app.find_element(f"image:{onusCheck_path}")
            print(locator)
            app.click_with_offset(f"image:{onusCheck_path}", x=100)
            time.sleep(1)
            app.type_text("200", enter=True)
            locator = app.find_element(f"image:{notOnusCheck_path}")
            print(locator)
            app.click_with_offset(f"image:{notOnusCheck_path}", x=100)
            time.sleep(1)
            app.type_text("100", enter=True)
            print("Enter is success")
            locator = app.find_element(f"image:{accept_path}")
            app.click(f"image:{accept_path}")

            text = app.read_text(f"image:{accept_path}")
            print(text)



            region = app.find_element(f"image:{transaction_path}")
            print("Region found:", region)

            moved_region = app.move_region(region, 92,0)
            print(moved_region)
            tans_num = app.read_text(moved_region)
            print("tansNO",tans_num)
            app.take_screenshot("output/gt1.png",moved_region)
            # text = app.read_text(info_region)
            # print(text)

            # text = app.read_text(f"image:{transaction_path}")
            # print(text)

         
        except Exception as e:
            print("The error is the ", e)



  