docker-compose down -v
docker system prune -f
docker-compose up -d --build
sleep 5
docker exec python_ins python create_gmail.py
docker-compose down -v
docker system prune -f