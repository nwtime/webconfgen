webconfgen
==========

Installation Instructions
-------------------------

Install the following dependencies using your prefered method.

```
python2 redis-server 
```

Install the python requirements via 

```
pip install -r requirements.txt
```

Run the database meta

```
python manage.py makemigrations && python manage.py migrate
```

Run Instructions
----------------

Edit the settings.py with your database passwords, redis-server broker, and configure the your static/ to be rendered via the STATIC_URL variable


Celery Notes
------------

To start celery, you need to run the following

```
celery -l info -A webconfgen
```
