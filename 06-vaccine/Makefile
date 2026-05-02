PYTHON  = python3
SCRIPT  = vaccine.py
TARGET  = http://localhost:8000
ARGS    ?=

# ── Run the tool ────────────────────────────────────────────────────────────────────
# Usage examples:
#   make run ARGS="http://localhost:8000 -X POST"
#   make run ARGS="http://localhost:8000/item?id=1"
#   make run ARGS="http://localhost:8000 -X POST -o results.json"
run:
	$(PYTHON) $(SCRIPT) $(ARGS)

# ── Spin up the local vulnerable test target ──────────────────────────────────
# Starts a SQLite-backed intentionally vulnerable web app on port 8000.
# Source: gitlab.cylab.be:8081/cylab/play/sqlite-injection
test:
	docker run -d -p 8000:80 gitlab.cylab.be:8081/cylab/play/sqlite-injection
	@echo ""
	@echo "[*] Test target is running at http://localhost:8000"
	@echo "[*] Run the scanner with:"
	@echo "    make run ARGS=\"$(TARGET) -X POST\""
	@echo "    make run ARGS=\"$(TARGET) -X GET\""

# ── Stop and remove the test container ──────────────────────────────────────
stop:
	docker ps -q --filter ancestor=gitlab.cylab.be:8081/cylab/play/sqlite-injection | xargs -r docker stop | xargs -r docker rm
	@echo "[*] Test container stopped."

.PHONY: run test stop
