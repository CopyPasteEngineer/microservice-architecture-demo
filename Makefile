up:
	docker-compose up -d --build

down:
	docker-compose down

log-ordering:
	docker logs -f ordering-service

log-ordering-relay:
	docker logs -f ordering-relay

log-inventory:
	docker logs -f inventory-service

log-inventory-handler:
	docker logs -f inventory-msg-handler

push-message:
	docker run -it --mount type=bind,source=$(shell pwd)/demo-push-message/main.py,target=/app/main.py \
		--network=MyNetwork demo-push-message
