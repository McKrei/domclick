# Название Docker-образа
IMAGE_NAME = my-dash-app
# Название Docker-контейнера
CONTAINER_NAME = my-dash-app-container

# Создание и запуск контейнера
app:
	docker build -t $(IMAGE_NAME) .
	sudo docker run -d --name $(CONTAINER_NAME) --log-driver=json-file -p 8071:8050 $(IMAGE_NAME)

# Остановка и удаление контейнера
app-down:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Получение логов контейнера
app-logs:
	docker logs -f $(CONTAINER_NAME)

# Открытие оболочки в работающем контейнере
app-shell:
	docker exec -it $(CONTAINER_NAME) /bin/sh

# Перезапуск контейнера
app-restart: app-down app app-logs
