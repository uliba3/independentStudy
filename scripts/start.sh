docker-compose down
docker-compose up -d
python3 scripts/startup_db.py
docker-compose logs -f api