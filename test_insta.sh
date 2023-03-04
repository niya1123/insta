docker-compose down -v
docker system prune -f
docker-compose up -d --build
sleep 5
docker exec python_ins python test_insta_user_data.py
docker-compose down -v
docker system prune -f