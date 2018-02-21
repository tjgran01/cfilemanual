# Table of Contents
1. [Overview](#Overview)
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
> have the time at his new position to constantly train, or explain how to use these scripts,
> so Fictitious Jim essentially wasted his time writing good, generic code that could have
> saved future teams hours of work. Why? Because though Fictitious Jim is a computer
> wizard, he flat out stinks at commenting and documenting his code.

In order to avoid a Fictitious Jim type situation at the MIND lab additional scripts,
or edits to scripts will not be allowed into this repo without corresponding **complete** documentation. This mean that for every commit a developer makes to this repo:

1. In line comments for non-function related changes.
  - Use your head when it comes to this, if you're just printing something out, you
    probably don't exhaustive documentation, but things just a indexing certain elements
    in lists should probably include an in line comment explaining what you are grabbing
    from a list.
  - You don't need to comment every single line, but should highlight what certain sections
    of the code are doing. Do these four lines process textual data?
2. Docstrings for function related changes.
  - Every single function must include an INFORMATIVE docstring to be submitted to this repo.
   No matter how clear you think your code is, always assume it isn't. Comments and
   docstrings are quite literally free.
3. An Update to this file, and it's table of contents.
  - Every script will have it's own section in this file, and will also have it's own link
    to that section in the TOC.
4. If using anything outside the range of the standard library, link to that documentation
as well.

If in doubt, consider your audience might be users who are wholly unfamiliar with programming.
For questions on formatting, etc, feel free to contact Trevor Grant at tjgran01@syr.edu.

# Scripts

## mkctemp.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Created for: Rapidly generating condition file templates with proper file names for a given experiment.

#### Overview:
