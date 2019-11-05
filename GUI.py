from __future__ import print_function
import tkinter as tk
from tkinter import ttk
from hardware import Arduino
from tkinter import font

from tkinter import filedialog




import threading

# Built-in modules
import logging
import threading
import time



class OnePhotonGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.onQuit)
        self.arduino = Arduino.Arduino(self)
        self.padx = 10
        self.nb_evt = 0
        self.evt_vals = []
        self.create_gui()


    def run(self):
        self.root.title("py Poisson")
        self.root.deiconify()
        self.root.mainloop()


    def create_gui(self):
        self.arduino_frame = tk.LabelFrame(self.root, text="Arduino")
        ttk.Label(self.arduino_frame, text="Nom port COM").grid(row=0, column=0, padx=self.padx)
        self.arduino_com_sv = tk.StringVar(value='COM6')
        ttk.Entry(self.arduino_frame, textvariable=self.arduino_com_sv, justify=tk.CENTER, width=7).grid(row=0, column=1)
        ttk.Button(self.arduino_frame, text="Connexion", width=25, command=self.connect_arduino).grid(row=0,
                                                                                                            column=2,
                                                                                                            padx=self.padx)
        self.arduino_connected_sv = tk.StringVar(value='NON')
        ttk.Label(self.arduino_frame, textvariable=self.arduino_connected_sv).grid(row=0, column=3, padx=self.padx)

        self.arduino_frame.pack(side="top", fill="both", expand=True)

        self.cmd_frame = tk.LabelFrame(self.root, text="Commande")

        ttk.Label(self.cmd_frame, text="Tps intégration (ms)").grid(row=0, column=0, padx=self.padx)
        self.int_time_sv = tk.StringVar(value='100')
        ttk.Entry(self.cmd_frame, textvariable=self.int_time_sv, justify=tk.CENTER, width=7).grid(row=0, column=1)
        ttk.Button(self.cmd_frame, text="Changer", width=25, command=self.change_int_time).grid(row=0, column=2, padx=self.padx)

        self.cmd_frame.pack(side="top", fill="both", expand=True)

        self.launch_stop_frame = tk.LabelFrame(self.root, text="Start/Stop")
        self.launch_stop_frame.pack(side="top", fill="both", expand=True)
        ttk.Button(self.launch_stop_frame, text="Compter", width=14, command=self.launch_monitor).grid(row=0, column=0,                                                                                               padx=self.padx)
        ttk.Button(self.launch_stop_frame, text="Stop", width=14, command=self.stop_monitor).grid(row=0, column=1,
                                                                                          padx=self.padx)
        self.launch_stop_frame.pack(side="top", fill="both", expand=True)

        helv36 = font.Font(family='Helvetica', size=36, weight='bold')
        self.result_frame = tk.LabelFrame(self.root, text="")
        self.result_frame.pack(side="top", fill="both", expand=True)
        ttk.Label(self.result_frame, font=("Calibri",56), text="nbre photon : ").grid(row=0, column=0, padx=self.padx)
        self.nb_photon_sv = tk.StringVar(value='0')
        ttk.Entry(self.result_frame, textvariable=self.nb_photon_sv, font=("Calibri",56), justify=tk.CENTER, width=7).grid(row=0, column=1)


    def change_int_time(self):
        int_time = int(self.int_time_sv.get())
        self.arduino.change_integration_time_callback(int_time)


    def launch_monitor(self):
        self.arduino.launch_monitor()

    def stop_monitor(self):
        self.arduino.stop_monitor()

    def connect_arduino(self):
        r = self.arduino.connect(self.arduino_com_sv.get())
        if r is True:
            self.arduino_connected_sv.set("OK")
            self.change_int_time()
            self.launch_monitor()
            self.stop_monitor()
        else:
            self.arduino_connected_sv.set("NON")

    def onQuit(self):
        # paramFile = open('param.ini', 'w')
        # paramFile.write(self.saveDir)
        self.root.destroy()
        self.root.quit()


    def log(self, text):
        pass
        # self.text_log.insert(tk.END, text + "\n")