# Table of Contents
1. [Overview](#overview)
2. [Setting Up](#setting-up)
    - [Hardware](#hardware)
      - [The ETG-4000](#the-etg-4000)
      - [The MP-150](#the-mp-150)
    - [Running `send_marks.py`](#running-send_markspy)
    - [Running `rcev_marks.py`](#running-rcev_markspy)

# Overview

Marks are messages that are sent to physiological data files to help researchers parse what happened
when during data collection. For example, if you are running an fNIRS study and your participant is
subjected to two different conditions, one of high stress and one of low stress, it is important that
the physiological data has some reflection of the the time in which the participant was subjected to
each of those different types of stimuli. This is what is referred to as a 'mark' in the data.

These scripts can be run on both the computer that the participant is working off of (refereed to as
the stim computer), and a connected Raspberry Pi that is on the same network (the mark machine or
computer). The pipeline of how to the mark sending process works is detailed below.

1. The participant performs some action on the stimulus machine.
  - Currently, these scripts are set up to take POST requests from AJAX calls that are embedded in the
  web based stimuli. What this means is that when a participant loads a web page, leaves a web
  page, clicks on a certain link on a web page, and so on, that that page sends a message to a server
  that exists locally on the stim computer. The action takes place via the `send_marks.py` file.

2. The stim machine running the web server then takes the data and sends it to the machine
that puts the actual marks in the data (in the case of the MIND lab it is a Raspberry Pi device).
  - The data is sent through the method call `data_transfer()` of the `MarkServer()` object. This
  object is instantiated during the initialization of the `send_marks.py` script.

3. The device for sending the marks to the sensors receives the data from the stimulus computer and
sends the appropriate marks to the physiological sensors.
  - This process is accomplished by running the `rcev_marks.py` file on the machine that is
  physically attached to the physiological sensors (the mark machine).

This process should continue for all the marks involved in the study. Some things to note are that
currently the `rcev_mark.py` script only includes support for the Hitachi ETG-4000 fNIRS system and
the BIOPAC MP-150 device.

1. The `rcev_mark.py` script currently sends a marks to the ETG-4000 via USB to serial port connector
(the connector plugs into the ETG-4000's comm port).
2. The BIOPAC mark is sent as a voltage output via the Raspberry Pi's GPIO pins. It currently sends
five volts no matter what, but future work may attempt to sent different artificial voltages to create
syntactically valid marks corresponding the the fNIRS marks.

# Setting Up

## Hardware.

In order to run these scripts properly you are going to need both a stimulus computer with Internet
connection, as well as a mark machine connected to the same network as the stim computer. Both of these
machines should have port `5560` open - so that messages may be sent from the stim computer to the mark
machine on that port. If for some reason this port is in use by some other application you will need to
alter the variable `port` in both the `send_marks.py` file stored on the stim machine as well as
`rcev_marks.py` on the mark machine to reflect a port that is available for these scripts to
communicate.

### The ETG-4000:

In order to set up the ETG-4000 for marks you will first need to power on the device. When you do, you
will be greeted by a screen that looks similar to the image below:

![fNIRS_Display](https://github.com/tjgran01/cfilemanual/blob/master/marksmanual/img/fNIRS_home.jpg)

1. Once in this screen you will want to click on the button marked "Parameter Set" (outlined in red
  above).


2. A new window should pop up, shown below:

![Param_Display](https://github.com/tjgran01/cfilemanual/blob/master/marksmanual/img/param_window.jpg)

While in this window chose 'Serial' from the 'Mark In' drop down menu.

![pick_serial](https://github.com/tjgran01/cfilemanual/blob/master/marksmanual/img/pick_serial.jpg)

3. Next click on the 'External' tab in the 'Parameter' window that is currently opened.

![click_external](https://github.com/tjgran01/cfilemanual/blob/master/marksmanual/img/click_external.jpg)

4. The settings should match the image below.

![com_settings](https://github.com/tjgran01/cfilemanual/blob/master/marksmanual/img/com_settings.jpg)

5. Click OK to close the window, and ensure that the USB connection on the Raspberry Pi is connected to
COM port 2 of the ETG-4000.

![com_port](https://github.com/tjgran01/cfilemanual/blob/master/marksmanual/img/com_port.jpg)

### The MP150:

The Raspberry Pi should already be wired up to receive marks from the Raspberry Pi, but if you are
setting it up from scratch:

1. You will want to connect a ground pin on the Raspberry Pi's GPIO board to the hole labeled GND on the
MP150 device.

2. Connect any (the scripts currently use pin 5) GPIO pin on the Raspberry Pi's board to the 'Digital
I/O' '0' input on the MP150.
  - Note: **If you are using a pin other than pin 5 on the GPIO board** `GPIO.setmode(GPIO.BOARD)` **for
  numbering convention of the pins. Change the variable** `pin` **in the script** `rcev_marks.py`.

3. When creating the channels for acquisition in the AcqKnowledge software:

  -Highlight MP150 in to toolbar at the top of the page.
  -Select 'Set Up Channels' from the dropdown menu.
  -Click the 'Digital' tab at the top of the page.
  -Check the boxes for 'Acquire', 'Plot', and 'Value' for channel 'D0'.

4. Set up whatever other channels you wish to record from physiological sensors.

5. Hit start - the digital input channel should be the last channel recording on the page.

## Running `send_marks.py`:

- On the stim computer open a terminal window and navigate to the cfilemanual directory. On the stim
computer this can be down by typing:

`cd cfilemanual`.

- After navigating to the directory you will want to activate the virtual environment for python.

`source venv/bin/activate`

- After activating the virtual environment navigate the the python directory inside of the the
marksmanual:

`cd marksmanual/scripts/python`

- Finally, run the program as a flask application.

`FLASK_APP=send_marks.py flask run`

## Running `rcev_marks.py`

- Open VNC Viewer on the stim machine. (Windows Key + Typing 'VNC' in the search bar) should open the
program.

- Type the ip address of the Raspberry Pi into the address bar.

- Enter the password for the root user of the pi.

- Open a terminal window on the Raspberry Pi and navigate to the `rcv_mark` directory.

- Run the `rcev_mark.py` script.
