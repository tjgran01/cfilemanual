# Table of Contents
1. [Overview](#overview)
2. [Scripts](#scripts)
    - [markserver.py](#markserverpy)
    - [send_marks.py](#sendmarkspy)
    - [rec_mark.py](#recmarkpy)

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
  - This process is accomplished by running the `rec_marks.py` file on the machine that is physically attached to the physiological sensors. This device (in our case Raspberry Pi) with be referred to as
  the mark machine for the rest of these documents.

This process should continue for all the marks involved in the study. Some things to note are that
currently the `rec_mark.py` script only includes support for the Hitachi ETG-4000 fNIRS system.

1. The `rec_mark.py` script currently sends a marks to that device via a USB to serial port connector
(it plugs into the ETG-4000's comm port).
2. The BIOPAC mark is sent as a voltage output via the Raspberry Pi's GPIO pins. It currently sends
five volts no matter what, but future work may attempt to sent different artificial voltages to create
syntactically valid marks.

### To Contribute to this arm of the project.

Research is a collaborative endeavor with a high rate of churn - which can be a great thing -
It allows teams to exchange ideas, knowledge, and domain expertise to others
throughout the research community organically! Yay! There is an upshot to this, however,
illustrated by the example below.

> Fictitious Jim, the computer Wiz, gets another research opportunity at institution X
> (Congrats, Fictitious Jim!), leaves his previous team with a bunch of useful scripts,
> but without the knowledge of how to properly utilize them. Fictitious Jim will not
> have the time at his new position to constantly train, or explain to new team members,
> how to use these scripts. Fictitious Jim kind of just wasted his time writing good,
> generic code that could have saved future teams hours of work. Why? Because although
> Fictitious Jim is a computer wizard, he flat out stinks at commenting and documenting his code.
>
> WARNING: Don't be like Fictitious Jim.

In order to avoid a Fictitious Jim type situation at the MIND lab: additional scripts,
or edits to scripts, will not be allowed into this repo without corresponding, *complete*,
documentation.

This means that for every commit a developer makes to this repo they also need to include:

1. In line comments for non-function related changes.

  - Use your head when it comes to this, if you're just printing something out you
    probably don't exhaustive documentation, but things like indexing certain elements
    in lists should probably include an in line comment explaining what you are grabbing
    from a list because it is not always clear.

  - You don't need to comment every single line, but should highlight what certain sections
    of the code are doing. Do these four lines process textual data? Comment it. Do these
    six lines check to make sure what the user inputed, and what data is actually in the data
    consistent? Comment it.

2. Docstrings for function related changes.

  - Every single function must include an INFORMATIVE docstring to be submitted to this repo.
   No matter how clear you think your code is, always assume it isn't. Comments and
   docstrings are quite literally free.

  - Best practice is to write out what the inputs and outputs are for any function, that way
  no one has to read the function line by line to understand what it does.

  - Don't be like this repo's author and try to name functions and variables with names
  that make sense. `foo`s and `bar`s can go `foobar` themselves.

3. An Update to this file, and it's table of contents.

  - Every script will have it's own section in this file, and will also have it's own link
    to that section in the TOC.

4. If using anything outside the range of the standard library, link to that documentation
as well.

If in doubt, consider your audience might be users who are wholly unfamiliar with programming.
Or, assume I (who am looking over your code), am an idiot. Which is not a wholly unfound assumption.

For questions or suggestions on formatting, etc, feel free to contact Trevor Grant at tjgran01@syr.edu.

# Scripts

## markserver.py

##### Created: 3/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creates a socket object that listens for one client to connect to. Once connected, the object sends string information to the client.

#### What this script does:

This script works by creating a socket object that waits until it is connected to before
transferring any data. Once created, the object will print to the console that a socket
bind in complete. After binding, the object will continue to listen for a connection on
port 5560, once that connection is received, the object is able to use the `data_transfer()`
method to send string data to the client device.

#### *This file takes as input*:

This file does not need any input. Though it's primary use is that it is imported into the
`send_marks.py` script, rather than being ran on it's own.

#### *This script gives as output*:

A `MarkServer()` object that can be imported into other scripts for sending string information
from once device to another.

#### Notes, etc:

This script needs to be updated for better error handling. It current works on both Mac and
Windows environments, but needs to be tested to see if it will work on Linux (Ubuntu).

## send_marks.py

##### Created: 3/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creates a Flask web server that is able to receive POST requests from incoming JQuery AJAX calls. It then sends the data payload from the POST requests to another machine (Raspberry Pi), to send the marks to all of the sensors.

#### What this script does:

This script works by first spinning up a local Flask web server. The site can be viewed at
the local ip address on port 5000. The site is used only for the purposes of being able to
receive HTTP requests from web based stimuli, and to translate those requests into method
calls that send the payload of the HTTP request to a client device.

To run this script you will want to invoke flask in the command line. In order to do this type:

OSX / Linux:

`FLASK_APP=send_marks.py flask run`

Windows:

NOTE: As this project currently stands - it does not work in Windows Environments.

`>> set FLASK_APP=send_marks.py`
`>> flask run`

#### *This file takes as input*:

This file does not need any input.

#### *This script gives as output*:

This file does not give any output.

#### Notes, etc:

This script should be run on the machine that the stimulus is being presented to the
participant on. Once it begins, you will want to then run `rev_mark.py` on the machine
that is sending the marks to the devices. Once a connection is established, the stimulus
machine should send all of the relevant marks to the machine sending the marks to the
physiological sensors.

## rcev_marks.py

##### Created: 4/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creates a socket object on a client device that connects to host, listens for incoming information (marks), and sends those marks to the relevant physiological sensors.

#### What this script does:

This script works by first attempting to connect to a machine on the same network
as the device that is presenting the stimulus. It will look for the server's ip address in a
`.txt` file located in the directory in which this script is run named `server_ip.txt`. After
finding the server's ip address it will connect to the server device on port 5560.

Once connection is established this script will wait for incoming information from the server.
Once it is given information this script will send that information out the the relevant
physiological sensors through various output methodologies.

Currently this script can send information to the HITACHI ETG-4000 though a serial port, as
well as the BIOPAC MP400 though electrical signals sent though a Raspberry Pi's GPIO pins.

#### *This file takes as input*:

There needs to be a valid ip address to the host machine (the machine running the stimulus)
contained within the `server_ip.txt` file in the directory in which this script is run. Both
machines involved in the marking need to be on the same network, and need port 5560 avilable.
This script will fail if `send_marks.py` is not currently running on the stimulus computer.

#### *This script gives as output*:

This script does not give any output.

#### Notes, etc:

Better error handling needs to be created for this script. `server_ip.txt` should be replaced
with `server_ips.csv`, and should store multiple ip address from which this script can cycle
through to try to establish connection. Further things should be done in the BIOPAC function
as well - perhaps it is worth trying to code marks that would appear as syntactically different
on the fNIRS device to be coded as different voltages by the BIOPAC marks.
