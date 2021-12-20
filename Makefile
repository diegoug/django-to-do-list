# -----------------------------------------------------------------------------
# development -----------------------------------------------------------------
# -----------------------------------------------------------------------------
create-network:
	docker network create django-network

start-development:
	cd docker/development/ && docker-compose up -d

stop-development:
	cd docker/development/ && docker-compose stop

build-development:
	# to do ms -------------------------------------------------
	cp services/to_do_ms/requirements.txt docker/development/build/to_do_ms/requirements.txt
	cd docker/development/build/to_do_ms/ && docker build -t "diegoug/to_do_ms_dev" .
	rm -rf docker/development/build/to_do_ms/requirements.txt
