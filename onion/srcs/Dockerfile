FROM debian:bullseye

# install packages and clean downloads
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y nginx tor openssh-server && \
    apt clean

COPY www/. /var/www/html

# nginx conf
COPY nginx.conf /etc/nginx/sites-available/default

# tor conf 
COPY torrc /etc/tor/torrc

# ssh conf
RUN mkdir /var/run/sshd
RUN echo 'root:pass' | chpasswd
COPY sshd_config /etc/ssh/sshd_config

EXPOSE 443 4242

# start tor in the background and nginx in the foreground (keeps container alive)
COPY start.sh /start.sh
CMD ["bash", "/start.sh"]