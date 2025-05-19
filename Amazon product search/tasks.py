from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
import time

file = Files()
selenium = Selenium()


url = "https://www.amazon.in/TheGiftKart-ShockProof-Samsung-Electroplated-Transparent/dp/B0D6BDZVC6/ref=srd_d_psims_d_sccl_1_2/260-4899243-2037043?pd_rd_w=BIhmU&content-id=amzn1.sym.6b3aa144-fd3f-4cac-9ae1-ac2407bcccc2&pf_rd_p=6b3aa144-fd3f-4cac-9ae1-ac2407bcccc2&pf_rd_r=MYGY702CX12B0ZBSKVH0&pd_rd_wg=yMzD9&pd_rd_r=a6dd9c82-13c1-4644-8de5-4d1bc7074892&pd_rd_i=B0D6BDZVC6&th=1"
search_term = "Wireless Mouse"
search_bar = "id:twotabsearchtextbox"
file.create_workbook("output/amazon_excel112.xlsx",)


@task
def amazon_product_search():
    """
    1. Open aamazon web browser
    2. search a product
    3. get list of product name and price 
    4 Append to the workbook
    """
    open_website(search_term)

def open_website(search_term):
    selenium.open_chrome_browser(url, maximized=True)
    time.sleep(20)
    selenium.input_text("id:twotabsearchtextbox", search_term)
    selenium.click_button('id:nav-search-submit-button')
    selenium.wait_until_page_contains(search_term,timeout=10)
    time.sleep(50)
    products = []

    for i in range(1,6):
        try:
            #Text scarpping
            name_xpath = f'(//h2[@class="a-size-medium a-spacing-none a-color-base a-text-normal"])[{i}]'
            price_tag = f'(//span[@class="a-price-whole"])[{i}]'
            name = selenium.get_text(name_xpath)
            price = selenium.get_text(price_tag)
            products.append({"Product Name": name, "Price":price})

        except Exception as e:
            print("Error {i}", e)
    
    selenium.close_browser()


    # Excel activities
    file.create_workbook("output/amazon_excel.xlsx",)
    file.append_rows_to_worksheet(products, header=True)
    file.save_workbook()


@task



def list_of_search():
    """
    1. Open browser
    2. List of item search
    3. create a excel
    """
    items = ["wireless mouse", "washing machine", "hp laptop"]

    selenium.open_chrome_browser(url, maximized=True)
    time.sleep(10)
    for item in items:
        try:

            selenium.input_text("id:twotabsearchtextbox", item)
            selenium.click_button("id:nav-search-submit-button")
            time.sleep(2)
            selenium.wait_until_page_contains(item)
            products = []
            for i in range(1,6):
                try:
                    name_xpath = f'(//h2[@class="a-size-medium a-spacing-none a-color-base a-text-normal"])[{i}]'
                    price_xpath = f'(//span[@class="a-price-whole"])[{i}]'
                    product_name =selenium.get_text(name_xpath)
                    # product_name ="selenium.get_text(name_xpath)"
                    price = selenium.get_text(price_xpath)
                    products.append({"Product Name":product_name, "Price": price})
                except Exception as e:
                    print("The search item error", e)

            #Excel create 
            file.create_worksheet(item, content=products, header=True)
            
        except Exception as e:
            print("The items error is ", e)
        
    selenium.close_browser()
    file.save_workbook()



