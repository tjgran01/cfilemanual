import socket
import websocket
import serial
import sys
# import RPi.GPIO as GPIO
import time


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


def main(host):
    while True:
        ws = websocket.create_connection(host)
        while True:
            try:
                result = ws.recv()
            except websocket._exceptions.WebSocketConnectionClosedException:
                break
            if "time" in result:
                print(result)
            if "mark" in result:
                print(result)
                send_to_fnirs(data)
                send_to_biopac(data)


if __name__ == "__main__":
    host = "ws://unity-fnirs.herokuapp.com/socket.io/?EIO=4&transport=websocket"
    main(host)
