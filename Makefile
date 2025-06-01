IMAGE_NAME=house-price-api
build:
	docker build -t $(IMAGE_NAME) .
run:
	docker run -p 8000:8000 $(IMAGE_NAME)
test:
	docker run -e MODE=test $(IMAGE_NAME)
clean:
	docker rmi $(IMAGE_NAME) || true
retrain:
	docker run -it $(IMAGE_NAME) python ml/train_model.py
stop:
	docker ps -q --filter "ancestor=$(IMAGE_NAME)" | xargs -r docker stop