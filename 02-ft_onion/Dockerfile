FROM alpine:latest

RUN apk add --no-cache nginx tor openssh

COPY srcs/nginx.conf /etc/nginx/nginx.conf
COPY srcs/www/index.html /var/www/html/index.html
COPY srcs/torrc /etc/tor/torrc
COPY srcs/sshd_config /etc/ssh/sshd_config
COPY onion_key.pub /home/onion/.ssh/authorized_keys

RUN adduser -D onion && \
    passwd -u onion && \
    chown -R onion:onion /home/onion/.ssh && \
    chmod 700 /home/onion/.ssh && \
    chmod 600 /home/onion/.ssh/authorized_keys && \
    ssh-keygen -A

CMD nginx && /usr/sbin/sshd && tor