from robocorp.tasks import task
from RPA.Assistant import Assistant

assistant = Assistant()

@task
def padded_element_with_background():
    assistant.open_container(padding=20, background_color="blue500")
    assistant.open_column()
    assistant.add_text("Sample text")
    assistant.add_text_input(name="TLanguage")
    assistant.open_column()
    assistant.add_text(text="Select caption file")
    assistant.add_file_input(label="Choose your file", name="Caption", file_type=None, source="output/source")


    assistant.add_radio_buttons(name="Gender", options=["Male", "Female"])
    assistant.add_submit_buttons(buttons="SUBMIT")
    assistant.close_column()
    assistant.close_column()
    assistant.close_container()
    response = assistant.run_dialog()
    print("Form response:", response)