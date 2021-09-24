#!/bin/bash

rm -rf tipsytequilaapi/migrations
rm db.sqlite3
python manage.py makemigrations tipsytequilaapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata customers
python manage.py loaddata products
python manage.py loaddata ratings
python manage.py loaddata product_rating
python manage.py loaddata reviews
python manage.py loaddata product_review
python manage.py loaddata orders
python manage.py loaddata order_product
