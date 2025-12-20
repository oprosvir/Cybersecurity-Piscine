python3 -c "import secrets; import sys; sys.stdout.write(secrets.token_hex(32))" > key.hex

pip install cryptography qrcode pillow
pip install -U cryptography qrcode pillow

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

oathtool --totp $(cat key.hex)
./ft_otp.py -k ft_otp.key