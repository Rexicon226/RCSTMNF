import requests
import webbrowser
import PySimpleGUI as sg
import time
import ctypes
import os
import win32process
from pymem import Pymem

pm = Pymem('TMForever.exe')

def time_as_int():
    return int(round(time.time() * 100))

def openmap():
    IDUrl = (requests.get('https://tmnf.exchange/trackrandom')).url
    IDLoc = IDUrl.rfind("/")
    IDUrl = list(IDUrl)
    ID = IDUrl[IDLoc + 1:len(IDUrl)]
    ID = ''.join(ID)
    print(ID)
    webbrowser.open('https://tmnf.exchange/trackplay/' + ID)

sg.theme('Black')
def font(x):
    return ('TechnicBold', x)

right_button = [
    [sg.Button('X', key='Quit', button_color=('red'), size=(2,1))],
]

layout = [
          [sg.Text('RCS', font=font(17), justification='l', expand_x=True), sg.Column(right_button, element_justification='right', expand_x=True)],
          [sg.Button('Start Random Map Challenge', key='-RUN-PAUSE-', button_color=('#880808'), size=(22,1))],
          [sg.HorizontalSeparator()],
          [sg.Text('', size=(6, 1), font=font(25), justification='left', key='text'), sg.Button('Next Map', key="nextmap", button_color=('#57E964'))],
          [sg.HorizontalSeparator()],
          [sg.Text('', font=font(13), key='skips'), sg.Button('Skip', key='Skip', button_color=('blue'))],
          [sg.HorizontalSeparator()],
          [sg.Text('', key='finished', font=font(15), justification='c', expand_x=True)]]

window = sg.Window('Sinon\'s Sporadic Snaking Selector', layout,
                   no_titlebar=True,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(2, 2),
                   finalize=True,
                   alpha_channel=0.9)

current_time, paused_time, paused, skips = 0, 0, True, 1
mapsFinished = 0
previous_timer = ''
startedChallenge = False
start_time = time_as_int()
timer_val = [0] * 1
window['skips'].update(str(skips) + ' skip(s) remaining')
startUpdate = '{:02d}:{:02d}'.format(60 - (1000 // 100) // 60, 00 -(0 // 100) % 60)
window['text'].update(startUpdate)
window['finished'].update("Maps Finished: " + str(mapsFinished))
while True:
    previous_timer = timer_val[0]
    timer_val = pm.read_string(14096536, 7)
    timer_list = list(timer_val)

     # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time
    else:
        event, values = window.read()

       # --------- Do Button Operations --------
    if event in (sg.WIN_CLOSED, 'Quit'):        # ALWAYS give a way out of program
        break
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
            start_time = time_as_int()
            skips = 1
            window['skips'].update(str(skips) + ' skip(s) remaining')
            startedChallenge = False
            mapsFinished = 0
        else:
            openmap()
        window['-RUN-PAUSE-'].update('Start Random Map Challenge' if paused else 'Stop Random Map Challenge')
    if(timer_list[0] == "-") & (previous_timer == "-"):
        startUpdate = '{:02d}:{:02d}'.format(60 - (1000 // 100) // 60, 00 -(0 // 100) % 60)
    if(timer_list[0] == "0") & (previous_timer == "-"):
        if(startedChallenge == False):
            startedChallenge = True
            start_time = time_as_int()
            current_time = 0

        # Change button's text
    elif event == 'Skip':
        if paused == False:
            if(skips == 1):
                skips = 0
                window['skips'].update(str(skips) + ' skip(s) remaining')
                openmap()
    elif event == 'nextmap':
        mapsFinished = mapsFinished + 1
        openmap()

    # --------- Display timer in window --------
    updateTime = '{:02d}:{:02d}'.format(59 - (current_time // 100) // 60, 59 -(current_time // 100) % 60)
    if(current_time > 360000):
        start_time = time_as_int()
        current_time = 0
        paused = not paused
        updateTime = startUpdate
        window['text'].update("TIME UP")
        window['-RUN-PAUSE-'].update('Start Random Map Challenge' if paused else 'Stop Random Map Challenge')
    window['text'].update(updateTime if not paused else startUpdate)
    window['finished'].update("Maps Finished: " + str(mapsFinished))