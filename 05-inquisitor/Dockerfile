FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpcap-dev \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install scapy

WORKDIR /app
COPY inquisitor.py .

CMD ["tail", "-f", "/dev/null"]
