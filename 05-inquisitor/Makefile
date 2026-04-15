all: up 

up:
	docker compose up --build -d
	@echo "Containers running. Enter attacker with:"
	@echo "  docker exec -it inquisitor bash"

info:
	@echo "FTP Server IP: $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-server)"
	@echo "FTP Server MAC: $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-server)"
	@echo "FTP Client IP: $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client)"
	@echo "FTP Client MAC: $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-client)"
	@echo "Inquisitor IP: $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inquisitor)"
	@echo "Inquisitor MAC: $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' inquisitor)"

help:
	docker exec inquisitor python inquisitor.py --help

run:
	$(eval SERVER_IP := $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-server))
	$(eval SERVER_MAC := $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-server))
	$(eval CLIENT_IP := $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client))
	$(eval CLIENT_MAC := $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-client))
	docker exec -it inquisitor python inquisitor.py $(CLIENT_IP) $(CLIENT_MAC) $(SERVER_IP) $(SERVER_MAC)

down:
	docker compose down

clean:
	docker compose down --rmi all --remove-orphans

re: clean up

.PHONY: all up info help run down clean re