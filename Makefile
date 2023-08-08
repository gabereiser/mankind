
build:
	@cd client && npm run build;
run:
	@cd gameserver && python service.py

all: build run