API_IMAGE_NAME := api
MONITOR_IMAGE_NAME := model-monitor

API_CONTAINER_NAME := api-c
MONITOR_CONTAINER_NAME := model-monitor-c

API_PORT := 8000
MONITOR_PORT := 8501

VOLUME_NAME := app_logs
VOLUME_DIR := /logs

TAG= latest

.PHONY: build run stop clean


# build docker images
build:
	docker build -t $(API_IMAGE_NAME):$(TAG) api
	docker build -t $(MONITOR_IMAGE_NAME):$(TAG) monitoring


# run the Docker containers
run:
	docker run -d --name $(API_CONTAINER_NAME) -p $(API_PORT):$(API_PORT) -v $(VOLUME_NAME):$(VOLUME_DIR) $(API_IMAGE_NAME):$(TAG)
	docker run -d --name $(MONITOR_CONTAINER_NAME) -p $(MONITOR_PORT):$(MONITOR_PORT) -v $(VOLUME_NAME):$(VOLUME_DIR) $(MONITOR_IMAGE_NAME):$(TAG)
	
# Stop running the Docker containers
stop:
	docker stop $(API_CONTAINER_NAME)
	docker stop $(MONITOR_CONTAINER_NAME)

	docker rm $(API_CONTAINER_NAME)
	docker rm $(MONITOR_CONTAINER_NAME)


# Clean up: remove the Docker images
clean:
	docker rmi $(API_IMAGE_NAME):$(TAG)
	docker rmi $(MONITOR_IMAGE_NAME):$(TAG)