from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
import time
from datetime import datetime

browser = Selenium()

url = "https://www.makemytrip.com/"
close_xpath = '//span[@data-cy="closeModal"]'
flight_xpath = '//span[normalize-space(.)="Flights"]'
One_way_xpath = '//li[normalize-space(.)="One Way"]'
from_xpath = '//input[@placeholder="From"]'
to_xpath = '//input[@placeholder="To"]'
depature_xpath = '//span[normalize-space(.)="Departure"]'
return_xpath = '//span[normalize-space(.)="Return"]'
dep_date = "Fri Jun 13 2025"
dep_xpath = f"//div[@aria-label='{dep_date}']"
ret_date = "Fri Aug 01 2025"
ret_xpath = f"//div[@aria-label='{ret_date}']"
traveller_xpath = "//span[normalize-space(.)='Travellers & Class']"
adult_xpath = f'//li[@data-cy="adults-3"]'
children_xpath = '//li[@data-cy="children-2"]'
infaints_xpath = '//li[@data-cy="infants-1"]'
travel_class_xpath = '//li[@data-cy="travelClass-0"]'
apply_button = '//button[@data-cy="travellerApplyBtn"]'
spcl_fare_xpath = '//div[normalize-space(.)="Regular"]'
search_xpath = '//a[normalize-space(.)="Search"]'

@task
def makeMytrip():
    activity()

def activity():
    try:
        date_format = "%a %b %d %Y"
        dep = datetime.strptime(dep_date, date_format)
        res = datetime.strptime(ret_date, date_format)
        days = (res-dep).days
        print("Days", days)
        if days >30:
            raise ValueError("This date range is not valid")
        else:


            browser.open_chrome_browser(url, maximized=True)
            time.sleep(2)
            browser.wait_until_element_is_visible(close_xpath)
            browser.click_element(close_xpath)
            print("Close register page")
            browser.click_element(flight_xpath)
            time.sleep(2)
            print("Select the flight")
            browser.click_element(One_way_xpath)
            print("Select the one way option")


            #Select the from 
            browser.click_element("id:fromCity")
            browser.wait_until_element_is_visible(from_xpath, timeout=10)
            browser.input_text(from_xpath, "Kochi")
            browser.click_element_at_coordinates(from_xpath, xoffset=0, yoffset=60)
            time.sleep(2)
            print("From added")

            #Select To
            browser.click_element("id:toCity")
            browser.wait_until_element_is_visible(to_xpath, timeout=10)
            browser.input_text(to_xpath, "Delhi")
            browser.click_element_at_coordinates(to_xpath, xoffset=0, yoffset=60)
            time.sleep(2)
            print("To added")


            #Depature date
            browser.wait_until_element_is_visible(depature_xpath)
            browser.click_element(depature_xpath)
            time.sleep(1)
            browser.wait_until_element_is_visible(dep_xpath, timeout=10)
            browser.click_element(dep_xpath)
            time.sleep(1)
            print("Depature date added")


            #Return date 
            browser.wait_until_element_is_visible(return_xpath)
            browser.click_element(return_xpath)
            browser.wait_until_element_is_visible(ret_xpath)
            browser.click_element(ret_xpath)
            time.sleep(2)
            print("Return date added")

            #Travellers & Class
            browser.wait_until_element_is_visible(traveller_xpath)
            browser.click_element(traveller_xpath)

            #Adulit
            browser.wait_until_element_is_visible(adult_xpath)
            browser.click_element(adult_xpath)
            print("Adults seletected")
            time.sleep(2)

            #children 
            browser.wait_until_element_is_visible(children_xpath)
            browser.click_element(children_xpath)
            print("Children selected")

            #infants
            browser.wait_until_element_is_visible(infaints_xpath)
            browser.click_element(infaints_xpath)
            print("Infaints selected")

            #Travel class
            browser.wait_until_element_is_visible(travel_class_xpath)
            browser.click_element(travel_class_xpath)
            print("select the travel class")

            #Apply button
            browser.wait_until_element_is_visible(apply_button)
            browser.click_button(apply_button)
            print("Click apply button")


            #special fair
            browser.wait_until_element_is_visible(spcl_fare_xpath)
            browser.click_element(spcl_fare_xpath)
            print("Special faire select")

            #search 
            browser.wait_until_element_is_visible(search_xpath)
            browser.click_element(search_xpath)
            print("Search button clicked")
            time.sleep(10)
    
    except Exception as e:
        print("The error is", e)

    finally:
        print("The program running successfully")




