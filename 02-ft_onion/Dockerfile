FROM alpine:latest

RUN apk add --no-cache nginx

COPY srcs/nginx.conf /etc/nginx/nginx.conf
COPY srcs/www/index.html /var/www/html/index.html

CMD ["nginx", "-g", "daemon off;"]