from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from tasks import login

browser = Selenium()



@task
def workItem():
    login()