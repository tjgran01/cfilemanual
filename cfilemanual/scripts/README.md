# Table of Contents
1. [Overview](#overview)
2. [Scripts](#scripts)
    - [mkctemp.py](#mkctemppy)

# Overview

This README should be used as a reference for all of the scripts located within the `/cfilemanual/cfilemanual/scripts/` directory of this project. Currently, this
section is a work in progress and will be updated as more general purpose scripts are
created to help researchers in the MIND lab (as well as other labs utilizing a conditions
file based approach for analyzing physiological data) get their data from the collection
phase to the modeling phase (you know, the fun part).

### To Contribute to this arm of the project.

Research is a collaborative endeavor with a high rate of churn which is a good thing!
It allows teams to exchange ideas, knowledge, and domain expertise to others
throughout the research community organically! Yay! The upshot of this however is
illustrated in the example below:

> Fictitious Jim, the computer Wiz, gets another research opportunity at institution X
> (Congrats, Fictitious Jim!), leaves his previous team with a bunch of useful scripts,
> but without the knowledge of how to properly utilize them. Fictitious Jim will not
> have the time at his new position to constantly train, or explain to new team members,
> how to use these scripts, so Fictitious Jim essentially wasted his time writing good,
> generic code that could have saved future teams hours of work. Why? Because although
> Fictitious Jim is a computer wizard, he flat out stinks at commenting and documenting his code.
>
> WARNING: Don't be like Fictitious Jim.

In order to avoid a Fictitious Jim type situation at the MIND lab additional scripts,
or edits to scripts, will not be allowed into this repo without corresponding, *complete*, documentation.

This mean that for every commit a developer makes to this repo they also need to include:

1. In line comments for non-function related changes.

  - Use your head when it comes to this, if you're just printing something out, you
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

  - Dest practice is to write out what the inputs and outputs are for any function, that way
  no one has to read the function line by line to understand what it does.

3. An Update to this file, and it's table of contents.
  - Every script will have it's own section in this file, and will also have it's own link
    to that section in the TOC.

4. If using anything outside the range of the standard library, link to that documentation
as well.

If in doubt, consider your audience might be users who are wholly unfamiliar with programming.
Or, assume I (who am looking over your code), is an idiot. Which is not a wholly unfound assumption.

For questions or suggestions on formatting, etc, feel free to contact Trevor Grant at tjgran01@syr.edu.

# Scripts

## mkctemp.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Rapidly generating condition file templates with proper file names for a given experiment.

#### What this script does:

mkctemp stands for **Make Conditions Template**.

This script is a quick and dirty method for generating conditions file templates. The script
guides the user through a series of prompts, asking questions like: "How many participants
where involved in this study?", "How many sensors did you use?", etc. It's aim is to then
generate templates for the user to input values into via manual entry, or copying and pasting
from another spreadsheet export such as SurveyMonkey or Qualtrics.

#### **This file takes as input**:

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

#### **This script gives as output**:

This file will create a subdirectory in the `exports` folder filled with properly named
and formatted conditions files templates. For examples of what output of this script should
look like refer to `./exports/sample_exports/` or `./exports/sample2_exports/` and open up
the .csv files in your editor of choice.

#### Notes, etc:

It should be noted that these currently include all TLX variables. If you do not want the
script to generate these values, and wish only to have templates with 'stim', 'onset', and
'duration' values (which you do need) you can comment out lines `177 - 179` and uncomment
line `175`.
