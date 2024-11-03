#!/bin/bash
 # Prepare for django
 python3 manage.py migrate
 # Start uwsgi
 uwsgi --ini uwsgi.ini