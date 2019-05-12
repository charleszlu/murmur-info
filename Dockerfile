FROM goozler/zeroc_ice_python

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
