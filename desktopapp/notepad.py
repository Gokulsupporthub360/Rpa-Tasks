from robocorp.tasks import task
from RPA.Desktop import Desktop
from RPA.Desktop.Windows import Windows
import time

app = Desktop()
win = Windows()

file_path = "Images/Notepad/file.png"
open_path = "Images/Notepad/open.png"


@task
def notepad():
    """This process is run for the note pad application"""
    note = app.open_application("Notepad")
    time.sleep(2)
    app.press_keys("cmd","up")
    time.sleep(2)
    app.click(f"image:{file_path}")
    time.sleep(2)
    app.click(f"image:{open_path}")
    print("Open button clicked")
    app.close_application(note)
    print("This application is closed successfully")


@task
def win_app():
    """This process is used for the win app"""
    win.open_executable(executable="notepad.exe", windowtitle="*", wildcard=True)
    time.sleep(2)
    win.send_keys("{cmd+UP}")
    # win.send_keys("cmd", "up")
    # win.send_keys("{cmd+up}")
    # time.sleep(2)
    win.mouse_click(f"image:{file_path}")
    time.sleep(2)

