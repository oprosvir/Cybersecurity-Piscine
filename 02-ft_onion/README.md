# onion service website
docker-compose exec ft_onion cat /var/lib/tor/hidden_service/hostname

# ssh into the onion service
torsocks ssh -i <private_key> -p 4242 onion@<onion_address>

# download and run Tor Browser
wget https://www.torproject.org/dist/torbrowser/15.0.3/tor-browser-linux-x86_64-15.0.3.tar.xz
tar -xvf tor-browser-linux-x86_64-15.0.3.tar.xz
mv ~/Downloads/tor-browser-linux-x86_64-15.0.3.tar.xz .
cd tor-browser
./start-tor-browser.desktop

# unsplash api key
https://ctxt.io/2/AAD4oRGLEg