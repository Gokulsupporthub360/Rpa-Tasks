from robocorp.tasks import task
from RPA.Desktop.Windows import Windows
import time
import re

app = Windows()

multiplyId = "id:multiplyButton"
equalId = "id:equalButton"
four_xpath = "id:num4Button"
two_xpath = "num2Button"
resultId = "id:CalculatorResults"

result_pattern = r"\b\d+\b"

@task
def desk():
    """This is the desktop app"""
    app.open_executable(executable="calc.exe", windowtitle="Calculator")
    time.sleep(5)
    elem = app.get_window_elements()
    print(elem)
    app.mouse_click(four_xpath)
    time.sleep(2)
    app.mouse_click(multiplyId)
    time.sleep(2)
    app.mouse_click(two_xpath)
    app.mouse_click(equalId)
    result = app.get_text(resultId)
    print(result['legacy_name'])
    text = result['legacy_name']
    matches = re.search(result_pattern, text)
    print(matches) if matches else print("No matches")


    