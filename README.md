# Start Up 🚀

create `.env` file as `.env.sample`

```bash 
docker compose up --build -d
```

### import Data to DB 📊

```bash 
python manage.py import_data Dexu_challenge_samples.csv
```


### Create User

```bash 
docker compose exec web python manage.py createsuperuser
```

