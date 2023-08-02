docker-compose down -v
docker system prune -f
docker-compose up -d --build
timeout /t 5
docker exec python_ins python like.py