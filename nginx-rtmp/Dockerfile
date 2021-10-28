FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y \
        wget \
        git \
        build-essential \
        ffmpeg \
        libpcre3 \
        libpcre3-dev \
        libssl-dev \
        zlib1g-dev

RUN git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git

ARG NGINX_VERSION=1.20.1
RUN wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
    tar -xf nginx-${NGINX_VERSION}.tar.gz

WORKDIR nginx-${NGINX_VERSION}

RUN ./configure \
        --prefix=/usr/local/nginx \
        --with-http_ssl_module \
        --add-module=../nginx-rtmp-module && \
    make -j 1 && \
    make install

RUN mkdir -p /nginx/hls
RUN mkdir -p /nginx/rec
RUN useradd -ms /bin/bash nginx
RUN chown -R nginx:nginx /usr/local/nginx/
RUN chown -R nginx:nginx /nginx/hls
RUN chown -R nginx:nginx /nginx/rec

COPY scripts/entrypoint.sh scripts/entrypoint.sh
RUN chown -R nginx:nginx scripts/entrypoint.sh
RUN chmod +x scripts/entrypoint.sh
# USER nginx
# ENTRYPOINT /usr/local/nginx/sbin/nginx -g 'daemon off;'
ENTRYPOINT [ "scripts/entrypoint.sh" ]