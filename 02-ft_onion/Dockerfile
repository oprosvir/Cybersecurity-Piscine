FROM alpine:latest

RUN apk add --no-cache nginx tor

COPY srcs/nginx.conf /etc/nginx/nginx.conf
COPY srcs/www/index.html /var/www/html/index.html
COPY srcs/torrc /etc/tor/torrc

CMD nginx && tor