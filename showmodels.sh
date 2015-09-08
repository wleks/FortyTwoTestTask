#!/bin/bash

dt=$(date '+%d-%m-%Y');

exec 2>"$dt".dat
python manage.py showmodels
exit 0