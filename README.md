# Gabryel v1
Public mirror of Gabryel repo

## Description

**Gabryel** is an integration program between Gmail and Google Calendar, which searches for order e-mail for KL Dental Services, and creates a pickup and dropoff events in Google Calendar.

The  program leverages the python wrapper for Google's OAuth2 API to periodically get e-mails from the account.

## Installation and running

1. You can clone using git bash.

​      git clone https://www.github.com/Sunchasing/Gabryel_P.git

2. Using python >3.6, build the virtual environment by running Scripts\build_windows.ps1 with powershell.

​      powershell .\Gabrye\Scripts\build_windows.ps1

3. Upon successfully building the virtual environment, the program can be started by running main.py with the virtual environment's python executable.

​      Gabryel\venv\Scripts\python.exe Gabryel\main.py

4. When prompted, select the e-mail that will be checked and authorize the application.

## Configuration

The configurations can be found in Gabryel\config\constants.py

They configurations are as follows:

SENDER_EMAIL - The e-mail adress of the sender, e-mail not containing this will be ignored.

LOG_DIR_PATH - The OS path to where the log files will be stored.

DEBUG_MODE - Setting to True will produce more detailed logs.
