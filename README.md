In `backend/services/`, add `settings.py`

```python
client_secret = '<TouchTunes API-KEY>'
```

3 environment variables are needed for the database connection
Add these to `activate` script in your virtual environment

```dosini
DB_USERNAME="<username of the database user>"
DB_PASSWORD="<password of the database user>"
DB_NAME="<name of the database>"
```

Migrations:
```
# To run migrations
alembic upgrade head

# To create a migration
alembic revision -m '<name>'
```

To run Flask server:
```shell
python app.py
```
