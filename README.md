In `backend/services/`, add `settings.py`

```python
client_secret = '<TouchTunes API-KEY>'
```

3 environment variables are needed for the database connection
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

To run Flask server:
```shell
python app.py
```

#### Data Structures
```
# in backend/services/main.py
location_songs = dict[Location -> dict[songId -> (count, playDate, artistId)]]
```

### Deploying to Back-End to Production 
Deployed with `nginx`, `gunicorn`, & and EC2 instance. Refer to (here)[https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/] for more information on the installation process

On the instance, run Flask from `backend/`
```sh
gunicorn app:app -b localhost:8000
```
