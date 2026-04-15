echo "Kreiram mrezu i volumen..."
docker network create student-net || true
docker volume create recipes_db_data || true
echo "Buildam image-ove..."
docker-compose build