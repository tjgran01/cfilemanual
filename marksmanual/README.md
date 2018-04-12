# Table of Contents
1. [Overview](#overview)
2. [Setting Up](#setting_up)

# Overview

Marks are messages that are sent to physiological data files to help researchers parse what happened
when during data collection. For example, if you are running an fNIRS study and your participant is
subjected to two different conditions, on of high stress and one of low stress, it is important that
the physiological data has some reflection of the the time in which the participant was subjected to
each of those different types of stimuli. This is where these scripts come in handy. These scripts can
be run on both the computer that the participant is working off of (refereed to as the stim computer),
and a connected Raspberry Pi that is on the same network. The pipeline of how to mark sending process
works is indicated below.

1. The participant performs some action on the stimulus machine.
  - Currently, these scripts are set up to take POST requests from AJAX calls that are embedded in the
  web based stimuli. What this means simply is that when a participant loads a web page, leaves a web
  page, clicks on a certain link on a web page, and so on, that that page sends a message to a server
  that exists locally on the stim computer. The action takes place via the `send_marks.py` file.

2. The stim machine running the web server then takes the data sends and pipes it to the machine
that puts the actual marks in the data (in the case of the MIND lab it is a Raspberry Pi device).
  - The data is sent through the method call `data_transfer()` of the `MarkServer()` object that is
  instantiated during the initialization of the `send_marks.py` script.

3. The device for sending the marks to the sensors receives the data from the stimulus computer and
sends the appropriate marks to the physiological sensors.
  - This process is accomplished by running the `rcev_marks.py` file on the machine that is physically attached to the physiological sensors. This device (in our case Raspberry Pi) with be referred to as
  the mark machine for the rest of these documents.

This process should continue for all the marks involved in the study. Some things to note are that
currently the `rcev_mark.py` script only includes support for the Hitachi ETG-4000 fNIRS system.

1. The `rcev_mark.py` script currently sends a marks to that device via a USB to serial port connector
(it plugs into the ETG-4000's comm port).
2. The BIOPAC mark is sent as a voltage output via the Raspberry Pi's GPIO pins. It currently sends
five volts no matter what, but future work may attempt to sent different artificial voltages to create
syntactically valid marks.

# Setting Up

In order to run these scripts properly you are going to need both a stimulus computer with Internet
connection, as well as a mark machine connected to the same network as the stim computer. Both of these
machines should have port `5560` open - so that messages may be sent from the stim computer to the mark
machine on that port. If for some reason this port is in use by some other application you will need to
alter the variable `port` in both the `send_marks.py` file stored on the stim machine as well as
`rcev_marks.py` on the mark machine to reflect a port that is available for these scripts to
communicate.

## The ETG-4000 fNIRS device:

In order to set up the ETG-4000 for marks you will first need to power on the device. When you do, you
will be greeted by a screen that looks similar to the image below:

1. Once in this screen you will want to click on the button marked "Parameter Set" (outlined in red
  above).
2. A new window should pop up, shown below:

While in this window chose 'Serial' from the 'Mark In' downdown menu.

3. Next click on the 'External' tab in the 'Parameter' window that is currently opened.

4. The settings should match the image below.

5. Click okay, and ensure that the USB connection on the Raspberry Pi is connected to COM port 2 of the
ETG-4000.

## The MP150 BIOPAC device:



In the top dropdown menu, you will want to set the
