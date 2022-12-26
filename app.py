from time import sleep
from PySimpleGUI import (
    theme,
    Text,
    Button,
    InputText,
    Window,
    WIN_CLOSED,
)

from threading import Thread

from ExtractDef import AppExtract, ConvertToExcel

DICT_TEMP = {}

# All the stuff inside your window.

def PositionWidgets():

    return [
        [
            Text('Welcome To ...')
        ],
        [
            Text('You Search'), 
            InputText(key="-InputKey-"),
        ],
                [
            Text('Number Result'), 
            InputText(key="-InputNumberResult-"),
        ],
        [
            Text('Lang'), 
            InputText(key="-InputLang-"),
        ],
         [
            Text('Name File'), 
            InputText(key="-InputNameFile-"),
        ],
        [
            Button('Search'), 
            Button('Convert'),
            Button('Closed'),
        ] 
    ]



import concurrent.futures

def foo(TextSearch,NumResults,Lang):
    global DICT_TEMP
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(AppExtract, TextSearch,NumResults,Lang)
        DICT_TEMP = future.result()
        future.cancel()


def ConfirmButtonDisable(window, key):
    global DICT_TEMP
    while True:
        if DICT_TEMP != {}:
            BlockedAlterDesBlocked(window, key, False)
            break
        print(DICT_TEMP)
        sleep(1)

def BlockedAlterDesBlocked(window, UpdateList, BlockDesBlock):
    for iterUpdateList in UpdateList:
        window[iterUpdateList].update(disabled=BlockDesBlock)

def GuiExe(Title:str):
    global DICT_TEMP
    theme('DarkAmber')   # Add a touch of color
    layout = PositionWidgets()
    window = Window(Title, layout)
    blocked = [
        "Search",
        "Convert",
        "Closed"
    ]
    while True:
        event, values = window.read()
        if event == "Search":
            TextSearch = values['-InputKey-']
            NumResults = int(values['-InputNumberResult-'])
            Lang  = values['-InputLang-']
            try:
                Thread(target = foo, args = (TextSearch,NumResults,Lang,)).start()
                BlockedAlterDesBlocked(window, blocked, True)
                Thread(target=ConfirmButtonDisable, args=(window,blocked)).start()
            except:
                pass
            

        if event == "Convert":
            InputNameFile = values["-InputNameFile-"]
            try:
                Thread(target = ConvertToExcel, args = (InputNameFile,DICT_TEMP,)).start()
                BlockedAlterDesBlocked(window, blocked, True)
                Thread(target=ConfirmButtonDisable, args=(window,blocked)).start()
            except:
                pass

        if event == WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

    window.close()

if __name__ == "__main__":
    GuiExe(Title = "Extract Numbers")