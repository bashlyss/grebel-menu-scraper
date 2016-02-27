#!/bin/bash
# This script will install the menu scraper into your environment so
# it is able to run.  Note that you must have pip installed to run this script
virtualenv -p $(which python3) .
. bin/activate

pip3 install -r requirements.txt

# Any further steps we want in the future
# - directory for output files
# - email/phone number for alerts once implemented, etc
