## To run project locally
### Initial configuration (do just once)
##### Install packages
```
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib rabbitmq-server
```
##### Create a database and configure it
```bash
sudo su - postgres
psql
```
```postgresql
CREATE DATABASE resume_storage;
CREATE USER resume_user WITH PASSWORD 'resume_password';
ALTER ROLE resume_user SET client_encoding TO 'utf8';
ALTER ROLE resume_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE resume_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE resume_storage TO resume_user;
```
##### Install python packages
```
python3 -m venv ./env
source env/bin/activate
pip install -r requirements.txt
```
### Run project
```
source env/bin/activate
python manage.py migrate
python manage.py runserver
celery -A resume worker --loglevel=INFO
```
* Make sure postgres and rabbitmq are running
* Change (if necessary) FILE_PATH_FIELD_DIRECTORY in settings.py to a directory where cv files are stored
* To upload a CV (an example of a format can be found in this repository) make a POST request with a filepath
```
curl -X POST -F "cv_file=@cv_example.pdf;type=application/pdf" 127.0.0.1:8000/api/upload/
```
