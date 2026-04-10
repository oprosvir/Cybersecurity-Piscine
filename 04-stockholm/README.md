python3 -m venv venv && source venv/bin/activate
deactivate

openssl rand -base64 12

hexdump -C notes.txt.ft
xxd notes.txt.ft