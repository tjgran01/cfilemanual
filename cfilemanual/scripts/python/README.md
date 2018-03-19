# Table of Contents
1. [Overview](#overview)
2. [Scripts](#scripts)
    - [inputmanager.py](#inputmanagerpy)
    - [mkctemp.py](#mkctemppy)
    - [pan_qualtrics.py](#pan_qualtricspy)
    - [get_qualtrics.py](#get_qualtricspy)

# Overview

This README should be used as a reference for all of the scripts located within the `/cfilemanual/cfilemanual/scripts/python/` directory of this project. Currently, this
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

## inputmanager.py

##### Created: 3/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Sanitizing and better handling user input to avoid allowing the user to put invalid parameters into scripts in this repository.

#### What this script does:

This script currently houses one class, known as `InputManager`. This class contains methods
for handling various user facing prompts like asking a user to input an integer value,
or asking the user to respond to a yes or no question.

#### *This file takes as input*:

All of these functions take a prompt to display to a user as an argument. Some methods require
additional arguments in order to function. See the docstrings in the source for details.

#### *This script gives as output*:

Sanitized user input to avoid the user inputting values which would cause the program to halt.

#### Notes, etc:

This script will be updated in the event that scripts in this repository require different
types of user input.

## mkctemp.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Rapidly generating condition file templates with proper file names for a given experiment.

#### What this script does:

mkctemp stands for *Make Conditions Template*.

This script is a quick and dirty method for generating conditions file templates. The script
guides the user through a series of prompts, asking questions like: "How many participants
where involved in this study?", "How many sensors did you use?", etc. It's aim is to then
generate templates for the user to input values into via manual entry, or copying and pasting
from another spreadsheet export such as SurveyMonkey or Qualtrics.

If a researcher does not intend to create conditions files by hand then the output from this
script will also serve as a backbone to 'check' the marks in the data to ensure that
everything is correctly lining up. This means that a researcher should run this script first
because it will also act as a sanity checker to ensure that the automated conditions file
generation scripts are

1. Working properly and that -
2. The data fed into the system isn't inconsistent with what the experimenter is expecting.

For example -
If during the creation of this script the experimenter states that session 1 of the experiment
has 20 tasks, but the data is marked with 22 onsets, then the experimenter knows that there
might be something odd about a particular dataset, and can further examine the data to ensure
that everything is accurate.

#### *This file takes as input*:

Nothing, initially, but the script asks the user for information about their experiment
in order to produce properly named and configured conditions files. Before running you will need
to know:

- How many participants are in the experiment.
- How many sessions were there in the experiment.
- How many sensors were used in the experiment.
- What types of sensors were used in the experiment.
- Their two digit experiment ID. (i.e. if participant IDs are '71'01, '71'02, the experiment
  ID is the first two digits in the participant ID. '71')
- How many *total* tasks participants were exposed to per session of experiment.

#### *This script gives as output*:

This file will create a subdirectory in the `exports` folder filled with properly named
and formatted conditions files templates. For examples of what output of this script should
look like refer to `./exports/sample_exports/` or `./exports/sample2_exports/` and open up
the .csv files in your editor of choice.

#### Notes, etc:

It should be noted that these currently include all TLX variables. If you do not want the
script to generate these values, and wish only to have templates with 'stim', 'onset', and
'duration' values (which you do need) you can comment out lines `177 - 179` and uncomment
line `175`.

## pan_qualtrics.py

##### Created: 3/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Taking the survey data from a Qualtrics survey and putting it into a useable format for model generation - a conditions file.

#### What this script does:



#### *This file takes as input*:



#### *This script gives as output*:



#### Notes, etc:



## get_qualtrics.py

##### Created: 3/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Automated retrieval of Qualtrics data in the form of a .csv file using Qualtrics API.

#### What this script does:

This script is a helper script for the `pan_qualtrics.py` script, but it may also be used
on it's own if the user just wants to view a data export without having to sign into their
Qualtrics account. The main function of the script is to take a user's API key and survey ID and
return a .csv file with all of the response data into the current directory called named
`MyQualtricsDownload`.

As this script was only amended by the author to have better error handling and to be more modular,
a full-fledged documentation for this script can be found at:

https://api.qualtrics.com/docs/response-exports.

If you do not know your API key, survey ID, and aren't sure where to find either. Read the
documentation published at:

https://api.qualtrics.com/docs/overview

If you still have questions, concerns, feel free to contact the author of this script.

#### *This file takes as input*:

Nothing initially, but in order for this script to work you will need:

- A Qualtrics API token (There is a helper function in the script to point the program to the file
  where your API token is located.)
- A survey ID for the survey you would like to get the data from.

Neither of these variables are included in the repo because, well, it wouldn't do anyone
(especially myself) much good to give out my API Key all willy-nilly, and you're (presumably)
not interested in analyzing my experiment for me.

Information of how to obtain and store the above pieces of information can be found in via
the two urls posted in the overview section of this script.

#### *This script gives as output*:

The script will create a sub-directory in the directory in which this script is run called:
`MyQualtricsDownload`. Inside of this folder will be a .csv export of the survey data corresponding
to the surveyID used as input to the program.

#### Notes, etc:

<s>More work needs to be done to include helper functions to help the user input their survey ID
properly. For now, a user can replace the value that is hard coded into the script.</s> - **DONE**

**__DO NOT INCLUDE YOUR API TOKEN IN THIS REPOSITORY__.:

IF YOU PUBLISH YOUR API TOKEN ONLINE ANYONE WITH AN INTERNET CONNECTION WILL
HAVE ACCESS TO YOUR SURVEY DATA. THIS IS WHAT WE REFER TO IN THE BIZ AS 'BAD NEWS
BEARS' (at the very least), AND 'A FEDERAL CRIME' (at worst, but it's a pretty bad
'at worst' if I'm to be honest).**
