## To run project locally
### Initial configuration (do just once)
##### Install packages
```
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
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
