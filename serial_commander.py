import serial
import threading
import time

class SerialCommander(threading.Thread):
    def __init__(self, port, baudrate=9600, timeout=1, on_cts=None, on_dsr=None):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.stop_event = threading.Event()
        self.serial_connection = None
        self.on_cts = on_cts
        self.on_dsr = on_dsr
        self.cts = True
        self.dsr = True

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            
            print(f"Connected to {self.port} at {self.baudrate} baud.")
            self.serial_connection.setRTS(False)
            return True
        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")
            return False

    def stop(self):
        self.stop_event.set()

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Disconnected from {self.port}.")
    def run(self):
        if not self.connect():
            return

        try:
            while not self.stop_event.wait(0.01):
                cts = self.serial_connection.getCTS()
                dsr = self.serial_connection.getDSR()

                if cts != self.cts:
                    self.cts = cts
                    if self.on_cts:
                        self.on_cts(cts)
                if dsr != self.dsr:
                    self.dsr = dsr
                    if self.on_dsr:
                        self.on_dsr(dsr)
        except (serial.SerialException, OSError) as error:
            if not self.stop_event.is_set():
                print(f"Serial connection error: {error}")
        finally:
            self.disconnect()


class SerialCommanderFake():
    def __init__(self, port, baudrate=9600, timeout=1, on_cts=None, on_dsr=None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.on_cts = on_cts
        self.on_dsr = on_dsr
        self.cts = True
        self.dsr = True

    def start(self):
        print(f"Fake SerialCommander started on {self.port} at {self.baudrate} baud.")
        # Simulate CTS and DSR changes
        time.sleep(10)
        self.cts = False
        if self.on_cts:
            self.on_cts(self.cts)
        time.sleep(10)
        self.cts = True
        if self.on_cts:
            self.on_cts(self.cts)
        time.sleep(180)
        self.cts = False
        if self.on_cts:
            self.on_cts(self.cts)
        time.sleep(10)
        self.cts = True
        if self.on_cts:
            self.on_cts(self.cts)
        time.sleep(180)
        self.cts = False
        if self.on_cts:
            self.on_cts(self.cts)
        time.sleep(10)
        self.cts = True
        if self.on_cts:
            self.on_cts(self.cts)

    def join(self):
        print("Fake SerialCommander finished.")
