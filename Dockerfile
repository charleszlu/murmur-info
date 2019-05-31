# zeroc-ice based on goozler/zeroc_ice_python: https://github.com/goozler/zeroc_ice_python
# openssh server based on hermsi/alpine-sshd: https://github.com/Hermsi1337/docker-sshd
FROM python:3-alpine

ARG ICE_VERSION=3.7.2

RUN apk add --no-cache \
    libstdc++ \
    openssh \
    bash && \
    apk add --no-cache --virtual .build-deps \
    bzip2-dev \
    openssl-dev \
    g++ && \
    pip install --no-cache-dir --global-option=build_ext --global-option="-D__USE_UNIX98" zeroc-ice==${ICE_VERSION} && \
    apk del .build-deps && \
    find /usr/local -depth \
        \( \
          \( -type d -a \( -name test -o -name tests \) \) \
          -o \
          \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
        \) -exec rm -rf '{}' +;

COPY entrypoint.sh /entrypoint.sh
COPY Murmur.ice /murmur-info/Murmur.ice
COPY murmur-info.py /murmur-info/murmur-info.py

RUN chmod +x /entrypoint.sh \
    && mkdir -p /root/.ssh \
    && rm -rf /var/cache/apk/* /tmp/*

ENV ROOT_PASSWORD root
ENV KEYPAIR_LOGIN false
ENV MURMUR_ICE_PATH /murmur-info/Murmur.ice
ENV MURMUR_HOST 127.0.0.1
ENV MURMUR_ICE_PORT 6502
ENV MURMUR_ICE_SECRET ""
ENV MURMUR_ICE_MSG_SIZE_MAX 65535
ENV EXCLUDE_KEYWORDS ""

VOLUME ["/etc/ssh"]

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
