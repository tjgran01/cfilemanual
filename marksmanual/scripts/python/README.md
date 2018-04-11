# Table of Contents
1. [Overview](#overview)
2. [Scripts](#scripts)
    - [markserver.py](#markserverpy)
    - [send_mark.py](#sendmarkpy)
    - [rec_mark.py](#recmarkpy)

# Overview

This README should be used as a reference for all of the scripts located within the `/cfilemanual/markmanual/scripts/python/` directory of this project. Currently, this
section is a work in progress and will be updated as more general purpose scripts are
created to help researchers in the MIND lab (as well as other labs utilizing a conditions
file based approach for analyzing physiological data) get their data from the collection
phase to the modeling phase (you know, the fun part).

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

This file does not need any input.

#### *This script gives as output*:

A `MarkServer()` object that can be imported into other scripts for sending string information
from once device to another.

#### Notes, etc:

This script needs to be updated for better error handling. It current works on both Mac and
Windows environments, but needs to be tested to see if it will work on Linux (Ubuntu).
