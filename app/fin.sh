#!/bin/bash
flask db init
flask db migrate -m 'users table'
flask db upgrade
flask run