FROM python:3.7-alpine

# zeroc-ice
ARG ICE_VERSION=3.7.2
RUN set -ex \
  && apk add --no-cache \
    libstdc++ \
    openssl-dev \
  && apk add --no-cache --virtual .build-deps \
    bzip2-dev \
    g++ \
  && pip install --global-option=build_ext --global-option="-D__USE_UNIX98" zeroc-ice==${ICE_VERSION} \
  && apk del .build-deps \
  && find /usr/local -depth \
       \( \
         \( -type d -a \( -name test -o -name tests \) \) \
         -o \
         \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
       \) -exec rm -rf '{}' +;

# SSH server and bash
RUN apk --update add --upgrade --no-cache openssh bash

COPY entrypoint.sh /entrypoint.sh
COPY Murmur.ice /murmur-info/Murmur.ice
COPY murmur-info.py /murmur-info/murmur-info.py

RUN  chmod +x /entrypoint.sh \
	  && mkdir -p /root/.ssh \
	  && rm -rf /var/cache/apk/* /tmp/*

ENV OPENSSH_VERSION=${OPENSSH_VERSION} \
    ROOT_PASSWORD=root \
    KEYPAIR_LOGIN=false

VOLUME ["/etc/ssh"]

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
