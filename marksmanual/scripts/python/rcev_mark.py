##### This script is the script to be run on the Raspberry Pi.
##### This script will do nothing if run on the machine running the stimulus.
##### Read the documentation on GitHub if this is at all unclear.

import socket
import serial
import sys
import csv
import RPi.GPIO as GPIO
import time


def set_gpio_parm(pin):
    """Sets parameters for GPIO pins on Raspberry Pi.
    Args:
        None
    Returns:
        None"""

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)


def get_host_ip():
    """Opens a file in the current directory called 'server_ip.txt', and reads
    the file to find the current ip address that this script will try to connect
    to.

    Args:
        None
    Returns:
        host(str): The ip address of the host computer.
    Rasies:
        FileNotFoundError: If there is no files 'server_ip.txt' in the current
        directory."""

    try:
        with open("server_ip.txt") as in_file:
            host = in_file.read()
            return host
    except FileNotFoundError:
        return None


def get_host_ips():
    """Iterates through a list of server ips. Returns a list of potential server
    ip addresses.

    Args:
        None
    Returns:
        hosts(list): List of potential server ip addresses
    Rasies:
        FileNotFoundError: If there is no files 'server_ip.txt' in the current
        directory."""

    try:
        with open("server_ip.csv", "r") as in_csv:
            ips = csv.reader(in_csv, delimiter=",")
            hosts = [ip for ip in ips]
            return hosts
    except FileNotFoundError:
        return None


def send_to_fnirs(data):
    """Sends a string mark to the fNIRS device through the USB port the the
    serial port of the fNIRS.

    Args:
        data(str): The mark sent to the fNIRS device.
    Reutnrs:
        None"""

    port = serial.Serial("/dev/ttyUSB0",
                         baudrate=9600,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         bytesize=serial.EIGHTBITS,
                         writeTimeout = 0,
                         timeout = 10)
    # Open and close marks on fNIRS.
    port.write(data)
    time.sleep(.5)
    port.write(data)
    port.close()


def send_to_biopac(data):
    """Sends a voltage (5v) to the BIOPAC Digital Input pin through GPIO pins on
    Raspberry Pi.

    Args:
        Data(str): The type of mark being sent (not currently used).
    Returns:
        None"""

    GPIO.output(3, True)
    time.sleep(.1)
    GPIO.output(3, False)
    GPIO.output(3, True)
    time.sleep(.1)
    GPIO.output(3, False)
    print("Sent to BIOPAC")


def get_mark():
    """Recieves a mark from the machine that is being used as the server
    and then sends that mark to both the BIOPAC and the fNIRS device.

    Args:
        None
    Returns:
        None"""

    while True:
        reply = s.recv(1024)
        print(reply.decode("utf-8"))
        if reply.decode("utf-8") == "KILL":
            s.close()
            sys.exit()
        else:
            send_to_fnirs(reply)
            send_to_biopac(reply)


def main():
    """Sets up a client side socket connection and waits for data from server.
    When incoming  data is recieved, sends data to the correct senors.

    Args:
        None
    Returns:
        None"""

    pin = 5
    set_gpio_parm(pin)
    port = 5560
    host = get_host_ip()
    if not host:
        print("File 'server_ip.txt' not found. Closing program.")
        sys.exit()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print("could not connect")
        sys.exit()

    while True:
        print("Waiting for mark.. ..")
        reply = get_mark()

    s.close()


if __name__ == "__main__":
    main()
