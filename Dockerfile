FROM goozler/zeroc_ice_python

RUN apk --update add --upgrade --no-cache openssh bash tzdata

# openssh server based on hermsi/alpine-sshd: https://github.com/Hermsi1337/docker-sshd
COPY entrypoint.sh /entrypoint.sh
COPY Murmur.ice /murmur-info/Murmur.ice
COPY murmur-info.py /murmur-info/murmur-info.py

RUN  chmod +x /entrypoint.sh \
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
