docker-compose down -v
docker system prune -f
docker-compose up -d --build
sleep 2
docker exec python_ins python like.py