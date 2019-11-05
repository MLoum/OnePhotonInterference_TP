from .Device import Device

import serial
import threading
from serial.tools.list_ports import comports


"""
ELL8 ROTARY STAGE 360° Continuous
rotation
262144
(40000H)
Closed: linear
2048 imp/mm
2

262144 pulse par revolution (360°) so that 1° is approximatevely 728 pulses.
"""

class ThoralbsElliptec_Rotation(Device):

    def __init__(self):
        self.address = 0
        self.nb_of_pulse_per_revolution = 262144
        self.nb_of_pulse_per_degree = self.nb_of_pulse_per_revolution / 360.0
        pass

    def get_info(self):
        msg = str(self.address) + "in"
        self.send_cmd(msg)

    def get_status(self):
        msg = str(self.address) + "gs"
        self.send_cmd(msg)

        ans = 0
        if ans == 0:
            return ans, "OK, no error"
        elif ans ==1:
            return ans, "Communication time out"
        elif ans ==2:
            return ans, "Mechanical time out"
        elif ans ==3:
            return ans, "Command error or not supported"
        elif ans ==4:
            return ans, "Value out of range"
        elif ans ==5:
            return ans, "Module isolated"
        elif ans ==6:
            return ans, "Module out of isolation"
        elif ans ==7:
            return ans, "Initializing error"
        elif ans ==8:
            return ans, "Thermal error"
        elif ans ==9:
            return ans, "Busy"
        elif ans ==10:
            return ans, "Sensor Error (May appear during self test. If code persists there is an error)"
        elif ans ==11:
            return ans, "Motor Error (May appear during self test. If code persists there is an error)"
        elif ans ==12:
            return ans, "Out of Range (e.g. stage has been instructed to move beyond its travel range)"
        elif ans ==13:
            return ans, "Over Current error"
        else:
            return ans, "Reserved"

    def search_frequency(self):
        # motor 1
        msg = str(self.address) + "s1"
        self.send_cmd(msg)
        # Wait for OK cmd.

        # motor 2
        msg = str(self.address) + "s2"
        self.send_cmd(msg)
        # Wait for OK cmd.

        # Save the value.
        self.save_user_data()

    def save_user_data(self):
        msg = str(self.address) + "us"
        self.send_cmd(msg)
        # Test OK


    def go_home(self):
        # by default clockwise.
        msg = str(self.address) + "ho0"
        self.send_cmd(msg)
        # wait for “0PO00000000”

    def move_absolute(self, angle_deg):
        nb_of_pulses = int(angle_deg * self.nb_of_pulse_per_degree)
        msg = str(self.address) + "ma" + str(nb_of_pulses)

    def move_relative(self, angle_deg, is_clockwise=True):
        """
        Position is a long type (32 bit signed, 2’s complement)
        Use “in” command to get number of pulses per engineering units (mm or degrees).
        :param angle_deg:
        :return:
        """
        nb_of_pulses = int(angle_deg * self.nb_of_pulse_per_degree)
        if not is_clockwise:
            nb_of_pulses = -nb_of_pulses
        msg = str(self.address) + "mr" + str(nb_of_pulses)

    def stop(self):
        pass

    def get_pos(self):
        msg = str(self.address) + "gp"


    def send_cmd(self):
        pass

    def wait_for_answer(self):
        self.is_waiting_serial = True
        self.thread_wait_answer = threading.Thread(name='thread_wait_answer', target=self.wait_answer_thread_fct)
        self.thread_wait_answer.start()

    def stop_waiting_for_answer(self):
        if self.thread_wait_answer.is_alive():
            self.thread_wait_answer.join(timeout=0.5)
        self.is_waiting_serial = False

    def wait_answer_thread_fct(self):
        while self.is_waiting_serial == True:
            line = self.serialPort.readline()
            if line != "":
                print(line)
                try:
                    i = int(line)
                    # self.add_point_to_history(int(i))
                    # self.current_value_sv.set(str(i))
                except ValueError:
                    # Handle the exception
                    print("")
            else:
                print("Elliptec motor timeOut")
                # TODO Log !
                #print (line.find("/"))


    def create_GUI(self):
        pass


