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
