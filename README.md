# reddit-backend
Backend for a simple reddit clone written using DRF.

- default database backend is sqlite (no dbms setup needed)
- jwt authenticaiton
- see api docs at `/swagger`

## Local Deployment:
- working directory for following commands should be <PROJ_LOCATION>/reddit_backend/

### setup server:
Create virtual environment (Optional):
```commandline
python3 -m venv .venv
. .venv/bin/activate.sh  # use the activate script corresponding to your shell environment e.g. activate.fish for fish shell  
```

Install dependencies and migrate database:
```commandline
pip install -r requirements.txt
python manage.py migrate
```

Run server:
```commandline
python manage.py runserver
```
