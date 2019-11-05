import serial
import threading
import time
from serial.tools.list_ports import comports

class Arduino():
    def __init__(self, gui):
        self.gui = gui
        self.comPortInfo = None
        self.serialPort = serial.Serial(port=None, baudrate=57600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, rtscts=False)
        # self.threadPoll = threading.Thread(name='arduinoPoll', target=self.read_from_port)
        # self.threadPoll.setDaemon(True)
        self.comPortInfo = ["", "", ""]
        # self.detect_serial_port("Poisson/")

    def load_device(self, params=None):
        #self.detectSerialPort(idString)
        # self.comPortInfo =["", "", ""]
        self.comPortInfo[0] = "COM7"
        if self.comPortInfo  != None:
            try:
                self.serialPort.port = self.comPortInfo[0]
                self.serialPort.open()
            except serial.SerialException:
                #FIXME
                self.gui.log("Pb lors de l'accès à l'Arduino")
                return False
            return True
        else:
            return False

    def connect(self, port_name):
        self.comPortInfo[0] = port_name
        if self.comPortInfo  != None:
            try:
                self.serialPort.port = self.comPortInfo[0]
                self.serialPort.open()
            except serial.SerialException:
                self.gui.log("Pb lors de l'accès à l'Arduino")
                return False
            return True
        else:
            return False


    def change_com_port(self, port):
        self.comPortInfo[0] = port

    def send_command(self, command):
        self.serialPort.write(command.encode())
        # try:
        #     self.serialPort.write(command)
        # except serial.portNotOpenError:
        #     print("Port non ouvert !")

    def open_port(self, port):
        pass

    def read_result(self):
        msg = "timeout"
        msg = self.serialPort.readline()
        return msg

    def pollArduino(self):
        return self.read_result()

    def detect_serial_port(self, answer_to_detect):
        self.comPortInfo = None
        listSerialPort = comports()
        for port in listSerialPort:
            try:
                self.serialPort.port = port[0]
                self.serialPort.baudrate = 57600
                self.serialPort.parity = serial.PARITY_NONE
                self.serialPort.stopbits = serial.STOPBITS_ONE
                self.serialPort.timeout = 1
                self.serialPort.rtscts=False
                self.serialPort.open()
            except serial.SerialException:
                self.gui.log("Pb ac un port COM")
                continue
            self.send_command("?/")
            time.sleep(1)
            response = self.serialPort.readline()
            if str(response) in answer_to_detect:
                return port
           # self.serialPort = serial.Serial(port=port[0], baudrate=57600, parity=serial.PARITY_NONE,
           #                                  stopbits=serial.STOPBITS_ONE, timeout=0.5, rtscts=False)


    def detect_serial_COM_port_via_serial_number(self, serialNumber):
        self.comPortInfo = None
        listSerialPort = comports()
        for port in listSerialPort:
            if serialNumber in port[3]:
                return port[0]

    def launch_monitor(self):
        self.send_command("m/")
        self.isMonitor = True
        self.threadMonitor = threading.Thread(name='arduinoCountingMonitor', target=self.monitor)
        self.threadMonitor.start()

    def stop_monitor(self):
        self.send_command("s/")
        if self.threadMonitor.is_alive():
            self.threadMonitor.join(timeout=0.5)
        self.isMonitor = False

    def monitor(self):
        while self.isMonitor == True:
            line = self.serialPort.readline()
            if line != "":
                print(line)
                try:
                    i = int(line)
                    self.gui.nb_photon_sv.set(str(i))
                except ValueError:
                    # Handle the exception
                    print("Pb Arduino Counting Transfert - not a number")
            else:
                print("Arduino counting timeOut")
                #print (line.find("/"))


    def count(self):
        """
        Cette fonction est bloquante contrairement à monitor.
        :return:
        """
        self.send_command("c/")
        line = self.serialPort.readline()
        try:
            i = int(line)
            return i
        except ValueError:
            # Handle the exception
            print("Pb Arduino Counting Transfert - not a number")
            return 0

    def change_integration_time_callback(self, int_time):
        try:
            int_time = int(int_time)
            self.change_integration_time(int_time)
        except ValueError:
            # Handle the exception
            print("Not a valid integration time")

    def change_integration_time(self, int_time_ms):
        cmd = "i"
        if int_time_ms < 10000:
            cmd += "0"
            if int_time_ms < 1000:
                cmd += "0"
            if int_time_ms < 100:
                cmd += "0"
            if int_time_ms < 10:
                cmd += "0"

        cmd += str(int_time_ms)
        cmd += "/"
        self.send_command(cmd)