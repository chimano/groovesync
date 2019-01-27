# groovesync 


### Setup

In `backend/services/`, add `settings.py`

```python
client_secret = '<TouchTunes API-KEY>'
```

5 environment variables are needed for the database connection
Add these to `activate` script in your virtual environment

```dosini
export DB_USERNAME="<username of the database user>"
export DB_PASSWORD="<password of the database user>"
export DB_NAME="<name of the database>"
export SPOTIFY_CLIENT_ID="<spotify client id>"
export SPOTIFY_SECRET_ID="<spotify secret id>"
```

Migrations:
```sh
# Before running migrations, make sure `backend/` is in PYTHON path
# by doing:
export PYTHONPATH='./'

# To run migrations
alembic upgrade head

# To create a migration
alembic revision -m '<name>'
```

To run Flask developement server:
```shell
# port 5000
python app.py
```

#### Data Structures
```
# in backend/services/main.py
location_songs = dict[Location -> dict[songId -> (count, playDate, artistId)]]
```

### Deploying Back-End to Production 
Deployed with `nginx`, `gunicorn`, & an AWS EC2 instance. Refer to [here](https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/) for more information on the installation process

On the instance, run Flask from `backend/` with
```sh
gunicorn app:app -b localhost:8000
```
