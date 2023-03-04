docker-compose down -v
docker system prune -f
docker-compose up -d --build
docker exec python_ins python like.py
docker-compose down -v
docker system prune -f