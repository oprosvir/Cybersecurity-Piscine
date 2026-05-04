all: up


up:
	docker run -d -p 8000:80 gitlab.cylab.be:8081/cylab/play/sqlite-injection
	@echo ""
	@echo "[*] Test target is running at http://localhost:8000"


test:
	./vaccine.py "http://192.168.56.105/?page=member&id=1&Submit=Submit"
	./vaccine.py "http://192.168.56.105/index.php?page=searchimg&id=3&Submit=Submit"
	./vaccine.py http://localhost:8000 -X POST -d "search=1"
	./vaccine.py https://demo.testfire.net/doLogin -X POST -d "uid=admin&passw=test&btnSubmit=Login"


down:
	docker stop $$(docker ps -q --filter ancestor=gitlab.cylab.be:8081/cylab/play/sqlite-injection)
	@echo "[*] Test container stopped."

.PHONY: all up test down
