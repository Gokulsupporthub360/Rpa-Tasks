from robocorp.tasks import task
from RPA.Word.Application import Application
import time
import os
from RPA.Browser.Selenium import Selenium


word = Application()
file_path = "C:/Users/Nimda/Downloads/sample_word.docx"
browser = Selenium()
url = "https://rpachallenge.com"

src_text = "Window-Eyes"
dest_test = "Mac  - eyes"
text = "This is the last line."

xpath = "//input[@name='searchStr']"

@task
def word_application():
    """This task is doing for the word application activities"""
    read_all_text(file_path)
    replace_text_word(file_path, src_text, dest_test)
    export_as_pdf(file_path, text)
   

def read_all_text(file_path):
    """This function used to read all text from the word application"""
    word.open_application(visible=True)
    word.open_file(file_path)
    content = word.get_all_texts()
    time.sleep(3)
    print(content)
    word.quit_application()

def replace_text_word(file_path, serc_text, dest_text):
    """This function is used for the replace a word from the word document and replace and save it new document."""
    word.open_application(visible=True)
    word.open_file(file_path)
    word.replace_text(serc_text, dest_text)
    word.save_document_as(os.getcwd()+"/"+"Sample document.docx")
    time.sleep(3)
    word.quit_application()


def export_as_pdf(file_path, text):
    """This function used for the add a extra line at the end of the word file and 
    this document is converted as pdf"""
    word.open_application(visible=True)
    word.open_file(file_path)
    word.write_text(text, end_of_text=True)
    word.save_document_as(os.getcwd() + "/" + "Sample_Updated.docx")
    word.export_to_pdf(os.getcwd()+"/"+"Samplepdf.pdf")
    word.quit_application()


@task
def rpa_challange_word():
    """This task is used to goto broswer rpa site and go to the movie search and write to a new word"""
    open_and_set_browser(url)


def open_and_set_browser(url):
    browser.open_chrome_browser(url, maximized=True)
    time.sleep(2)
    browser.click_link("//a[text()='Movie Search']")
    browser.input_text(xpath, "batman")
    time.sleep(2)
    browser.click_button('//button[text()="Find"]')
    time.sleep(10)
    for i in range(1, 2):
        try:
            # Close any open card reveal
            if browser.does_page_contain_element("//div[contains(@class, 'card-reveal') and contains(@style, 'block')]"):
                browser.click_element('//i[text()="close"]')
                time.sleep(1)

            # Scroll into view and wait for the element
            icon_xpath = f"(//i[text()='more_vert'])[{i}]"
            browser.wait_until_element_is_visible(icon_xpath, timeout=10)
            browser.scroll_element_into_view(icon_xpath)
            time.sleep(1)

            # Click to expand
            browser.click_element(icon_xpath)
            time.sleep(2)

            # Extract full text after reveal
            title_xpath = f"(//span[@class='card-title grey-text text-darken-4'])[{i}]"
            body_xpath = f"(//p[@_ngcontent-c3])[{i}]"

            title = browser.get_text(title_xpath)
            body = browser.get_text(body_xpath)

            print("Title:", title)
            print("Description:", body)

            word.open_application(visible=True)
            word.create_new_document()
            word.write_text(title)
            word.write_text("\n")
            word.write_text(body, end_of_text=True)
            word.save_document()
            word.quit_application()

            # Close the card
            browser.click_element('//i[text()="close"]')
            time.sleep(1)

        except Exception as e:
            print(f"Error on card {i}: {e}")
