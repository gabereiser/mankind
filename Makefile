
all: clean deps build run

deps:
	@cd client && npm install && cd ../gameserver && pip install -r requirements.txt && cd ..
clean:
	@rm -rf client/node_modules && rm -rf client/dist && rm -rf gameserver/public/*
build:
	@cd client && npm run build && cp -r dist/* ../gameserver/public/;
run:
	@cd gameserver && python service.py

.PHONY: deps build clean run

