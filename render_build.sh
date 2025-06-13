#!/usr/bin/env bash
# exit on error
set -o errexit

# Cập nhật pip
pip install --upgrade pip

# Cài đặt các gói Python
pip install -r requirements.txt

# Áp dụng migrations
export FLASK_APP=wsgi:app
flask db upgrade
