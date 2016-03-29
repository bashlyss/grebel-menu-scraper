#!/bin/bash

WDIR=/var/www/grebel-menu-scraper
VIRTUALENV_DIR=/var/www/grebel-menu-scraper
LOG_DIR=/var/log/grebel-menu

source $VIRTUALENV_DIR/.secrets/CREDENTIALS
source $VIRTUALENV_DIR/bin/activate

cd $WDIR
env GREBEL_MENU_SETTINGS=../prod_settings.cfg ./run.py 1> $LOG_DIR/debug.log 2> $LOG_DIR/error.log
