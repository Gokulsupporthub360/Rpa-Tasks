from robocorp.tasks import task
from RPA.Word.Application import Application
import time
import os


word = Application()
file_path = "C:/Users/Nimda/Downloads/sample_word.docx"

src_text = "Window-Eyes"
dest_test = "Mac  - eyes"
text = "This is the last line."

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


