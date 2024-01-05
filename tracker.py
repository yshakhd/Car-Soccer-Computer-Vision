import time
import cv2
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow
from math import cos, sin

stream = cv2.VideoCapture(0)

lower_yellow = np.array([20,120,120])
upper_yellow = np.array([40,255,255])

lower_blue = np.array([100,70,70])
upper_blue = np.array([125,255,255])

lower_red = np.array([0,40,50])
upper_red = np.array([15,255,255])

lower_green = np.array([70,70,70])
upper_green = np.array([80,255,150])

lower_orange = np.array([10,120,170])
upper_orange = np.array([20,255,255])

plt.ion()
fig, ax = plt.subplots(1, 2)
ax[0].set_aspect("equal")
ax[0].set_xlim(0,2)
ax[0].set_ylim(0,2)
ax[0].set_title("car orientation and ball direction")
ax[1].set_aspect("equal")
ax[1].set_xlim(0,2)
ax[1].set_ylim(0,2)
ax[1].set_title("joystick suggestion")

arrow = Arrow(1,1,1,1, color="#aa0088")
arrow2 = Arrow(1,1,1,1, color="#aa0088")

a1 = ax[0].add_patch(arrow)
a2 = ax[0].add_patch(arrow)
a3 = ax[1].add_patch(arrow2)
plt.draw()

t = False
b = False
goals_t = 0
goals_b = 0
timer = 0

def time_as_int():
    return int(round(time.time() * 100))

sg.theme("Black")

p1_col = [
    [sg.Image('p1.png', background_color='#ff1238')],
    [sg.Text("", font=('Helvetica', 480, 'bold'),key='P1', background_color='#ff1238')]
]
p2_col = [
    [sg.Image('p2.png', background_color='#378dfe')],
    [sg.Text("", font=('Helvetica', 480, 'bold'),key='P2', background_color='#378dfe')]
]
clock = [
    [sg.Text('', font=('Helvetica', 100),justification='center', key='text')],
    [sg.Button('Pause', font=('Helvetica'), key='-RUN-PAUSE-', button_color=('white', '#001480')),
     sg.Button('Reset', font=('Helvetica'), button_color=('white', '#007339'), key='-RESET-'),
     sg.Exit(button_color=('white', 'firebrick4'), key='Exit')],
    [sg.Image(filename='', key='image')],
    [sg.Canvas(key='-CANVAS-')]
]
layout = [
    [
        sg.Column(p1_col, background_color='#ff1238',element_justification='c', pad=(0, 0)),
        sg.VSeperator(pad=(0, 0)),
        sg.Column(clock, element_justification='c', pad=(0, 0)),
        sg.VSeperator(),
        sg.Column(p2_col, background_color='#378dfe',element_justification='c', pad=(0, 0))
    ]
]

window = sg.Window("Its Called (Car) Soccer", layout, location=(0, 0), keep_on_top=True, resizable=True, transparent_color='#000000')
current_time, paused_time, paused = 6050, 6050, False
start_time = time_as_int()

while True:
     # --------- Read and update window --------
    if not paused:
        event, values = window.read(timeout=10)
        current_time = start_time + 6050 - time_as_int() if current_time > 0 else 0
    else:
        event, values = window.read()
    # --------- Do Button Operations --------
    if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
        break
    if event == '-RESET-':
        paused_time = start_time = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_time = start_time + time_as_int() - paused_time
        # Change button's text
        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    
    if event in (None, sg.WIN_CLOSED):
        break

    if event == sg.TIMEOUT_EVENT:
        p1_score = 2
        p2_score = 3
        window['P1'].update(p1_score)
        window['P2'].update(p2_score)
    # --------- Display timer in window --------
    window['text'].update('{:02d}:{:02d}.{:02d}'.format((((current_time) // 100) // 60),
                                                        ((current_time) // 100) % 60,
                                                        (current_time) % 100))
    ret, frame = stream.read()
    if frame is not None:
        frame = frame[:, :-100]
    frame = cv2.resize(frame, (int(1920*.50), int(1080*.50)))
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
    window['image'].update(data=imgbytes)
    
window.close()

cv2.destroyAllWindows()