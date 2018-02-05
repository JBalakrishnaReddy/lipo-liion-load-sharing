#!/usr/bin/python3
import tkinter
import tkinter.ttk
from tkinter.scrolledtext import ScrolledText
import time
import xlrd
import xlwt
import pandas
import struct
import serial
import sys
import os
# import functionalities, graphs
# print(os.getcwd())
# print(sys.path)
sys.path.append('/home/bk/PycharmProjects/OpenCV/kinters/')
# print(sys.path)
from loadcalculations.pythonsource import functionalities, graphs
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


combobox = {}
ser = serial.Serial()
result_frame_text = None
DEVICE_FILE = '/dev/ttyUSB0'
w = 0
h = 0

def add_frame(app):
    # an exclusive button at the top right for opening a serial port
    frame = tkinter.Frame(app)
    frame.config(background='lavender')
    try:
        img = tkinter.PhotoImage(file='button.png')
    except Exception as err:
        img = ''
    button_text = tkinter.StringVar()
    button = tkinter.Button(frame, textvariable=button_text, width=10, \
        command=lambda:functionalities.serial_connect(button_text, result_frame_text))
    button.image = img

    button_text.set('Connect')
    # text='serial monitor')
    label = tkinter.Label(frame, text='Comport', bg='lavender')
    global combobox
    combobox = tkinter.ttk.Combobox(frame, text='com ports', \
        postcommand=lambda:functionalities.updatecombobox(combobox))
    # self.combobox['values'] = get_comports()
    label.grid(row=0, column=0, sticky=tkinter.W)
    combobox.grid(row=0, column=1, sticky=tkinter.W)
    button.grid(row=0, column=2, sticky=tkinter.E)
    frame.pack(side=tkinter.TOP, padx=2, pady=2, fill='x')


def add_result_frame(app):
    global result_frame_text
    result_frame_text = ScrolledText(app, height=6, background='black', foreground='red')
    result_frame_text.pack(side=tkinter.BOTTOM, padx=5, pady=5, fill='x')


def add_main_frame(app):
    frame = tkinter.Frame(app)
    frame.config(background='green')
    frame.config(background='lavender')
    # child_frame = tkinter.Frame(frame, bg='yellow', height=300, width=477)
    # child_frame.grid(row=0, rowspan=200, column=1, columnspan=200)
    child_frame = tkinter.Frame(app, bg='yellow', height=300, width=500)
    child_frame.pack(side=tkinter.RIGHT, fill='both', padx=3, pady=3)
    child_frame.pack_propagate(0)

    # img = tkinter.PhotoImage(file='/home/bk/PycharmProjects/OpenCV/kinters/loadcalculations/10.jpg')
    graph_image = tkinter.PhotoImage(file='/home/bk/PycharmProjects/OpenCV/kinters/loadcalculations/graph2.png')
    add_button(frame, 0, 1, 'graph', img=graph_image, command=lambda: update_graphs(child_frame, app))
    table_image = tkinter.PhotoImage(file='/home/bk/PycharmProjects/OpenCV/kinters/loadcalculations/table.png')
    add_button(frame, 0, 0, 'table', img=table_image, command=lambda: tabulate_data(child_frame))
    add_button(frame, 0, 2, 'live feed', command=lambda: update_live_feed(child_frame))
    frame.pack_propagate(0)
    frame.pack(side=tkinter.LEFT, fill='both', padx=4, pady=4)


def show_graph(w, h):
    # w,h = frame.winfo_width(), frame.winfo_height()
    # frame.destroy()
    # print(frame.winfo_width())
    # print(frame.winfo_height())
    frame = tkinter.Frame(width=w, height=h)
    # frame.pack()
    f = pyplot.figure(figsize=(5, 3), dpi=100)
    a = f.add_subplot(111)
    a.plot([1, 2, 3], [4, 5, 6])
    canvas = FigureCanvasTkAgg(f, frame)
    canvas.show()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2TkAgg(canvas, frame)
    toolbar.update()
    canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # frame.pack()
    return frame


def update_graphs(child_frame, app):
    for child in child_frame.winfo_children():
        child.destroy()
    global ret
    global w, h
    # if child_frame is not None:
    if w is 0 or h is 0:
        w = child_frame.winfo_width()
        h = child_frame.winfo_height()
        print(w, h)
        # child_frame.destroy()
        # child_frame = None
    ret = show_graph(w, h)
    ret.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # ret.destroy()
    # print("destroyed")
    # ret.pack(app)


def update_live_feed(frame):
    frame.update_idletasks()
    for child in frame.winfo_children():
        child.destroy()
    new_f = tkinter.Frame(frame, background='navajo white', width=frame.winfo_width(), height=frame.winfo_height())
    canvas_current = tkinter.Canvas(new_f, bg='navajo white')
    frame.update_idletasks()
    canvas_current.grid(row=0, column=0, padx=5, pady=5)
    frame.update_idletasks()
    canvas_voltage = tkinter.Canvas(new_f, bg='navajo white')
    canvas_voltage.grid(row=2, column=0, padx=10, pady=10)

    lipo_current = tkinter.Label(canvas_current, text='lipo current', bg=canvas_current['bg'])
    liion_current = tkinter.Label(canvas_current, text='liion current', bg=canvas_current['bg'])
    total_current = tkinter.Label(canvas_current, text='total current', bg=canvas_current['bg'])
    lipo_voltage = tkinter.Label(canvas_voltage, text='lipo voltage', bg=canvas_current['bg'])
    liion_voltage = tkinter.Label(canvas_voltage, text='liion voltage', bg=canvas_current['bg'])

    lipo_current_reading = tkinter.Label(canvas_current, text='lipo current', bg=canvas_current['bg'])
    liion_current_reading = tkinter.Label(canvas_current, text='liion current', bg=canvas_current['bg'])
    total_current_reading = tkinter.Label(canvas_current, text='total current', bg=canvas_current['bg'])
    lipo_voltage_reading = tkinter.Label(canvas_voltage, text='lipo voltage', bg=canvas_current['bg'])
    liion_voltage_reading = tkinter.Label(canvas_voltage, text='liion voltage', bg=canvas_current['bg'])

    lipo_current.grid(row=1, column=1, padx=10, pady=10)
    liion_current.grid(row=2, column=1, padx=10, pady=10)
    total_current.grid(row=3, column=1, padx=10, pady=10)
    lipo_voltage.grid(row=4, column=1, padx=10, pady=10)
    liion_voltage.grid(row=5, column=1, padx=10, pady=10)

    lipo_current_reading.grid(row=1, column=2)
    liion_current_reading.grid(row=2, column=2)
    total_current_reading.grid(row=3, column=2)
    lipo_voltage_reading.grid(row=4, column=2)
    liion_voltage_reading.grid(row=5, column=2)
    # print('canvas width', canvas_current.winfo_width(), canvas_current['width'])
    new_f['height'] = frame.winfo_height()
    new_f['width'] = frame.winfo_width()
    new_f.pack(fill='both', expand=True)


def tabulate_data(frame):
    for child in frame.winfo_children():
        child.destroy()
    c_f = tkinter.Frame(frame, bg='cyan', width=frame.winfo_width(), height=frame.winfo_height())
    c_f.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    frame.update_idletasks()
    #c_f.pack_propagate(0)
    canv = tkinter.Canvas(c_f, width=c_f.winfo_width(), height=c_f.winfo_height(), bg=c_f['bg'])
    canv.create_text(200,150,text="Work in Progress")
    canv.pack()


def add_button(parent, location_x, location_y, text='button', img=None, side=tkinter.W, command=None):
    if img is None:
        butt = tkinter.Button(parent, borderwidth=2, height=5, width=10, relief=tkinter.RAISED, text=text, command=command)
    else:
        butt = tkinter.Button(parent, borderwidth=2, compound=tkinter.CENTER, padx=3, pady=3, image=img, command=command)
        butt.image = img
    butt.grid(row=location_y,column=location_x,sticky=side)


def dissolve_packet(packet):
    if len(packet) == 14 and packet.startswith(b'!:'):
        readings = {'lipo_current': 0, 'liion_current': 0, 'total_current': 0,
                    'lipo_voltage': 0, 'liion_voltage': 0}
        _, a, b, c, d, e = struct.unpack('<hhhhhh', packet)
        readings['lipo_current'] = str(a * (1000/55))
        readings['liion_current'] = str(b * (1000/55))
        readings['total_current'] = str(c * (1000/55))
        readings['lipo_voltage'] = str(d * (1.5/15.2))
        readings['liion_voltage'] = str(e * (1.5/15.2))
        return True, readings
    else: return False, False


def update_data():
    ser = serial.Serial(DEVICE_FILE, 115200)
    data = ser.read(ser.in_waiting)
    ret, dis_data = dissolve_packet(data)
    if ret is True:
        print(dis_data)


def main():
    app = tkinter.Tk()
    app.title = 'Load calculator'
    #app.geometry('500x438')
    add_frame(app)

    add_result_frame(app)
    app.update()
    add_main_frame(app)
    app.resizable(False,False)
    # app.protocol("WM_DELETE_WINDOW", app.destroy)
    app.mainloop()


if __name__ == "__main__":
    main()

