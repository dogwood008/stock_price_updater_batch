FROM python:3.9.5-slim-buster
LABEL maintainer="dogwood008"

ARG WEBDAV_SERVER_ADDRESS
ARG KABU_PLUS_ID
ARG KABU_PLUS_PW
ARG DIST

ENV MOUNTPOINT /mnt/kabuplus
ENV WEBDAV_SERVER_ADDRESS ${WEBDAV_SERVER_ADDRESS}
ENV KABU_PLUS_ID ${KABU_PLUS_ID}
ENV KABU_PLUS_PW ${KABU_PLUS_PW}
ENV DIST ${DIST}
ENV WORKDIR /opt/sync
WORKDIR ${WORKDIR}

# https://linux.just4fun.biz/?Ubuntu/WebDAV%E3%82%92%E4%B8%80%E8%88%AC%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%A7%E7%89%B9%E5%AE%9A%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%81%AB%E3%83%9E%E3%82%A6%E3%83%B3%E3%83%88%E3%81%99%E3%82%8B%E6%89%8B%E9%A0%86
# https://l-w-i.net/t/ubuntu/davfs2_001.txt
RUN apt update && \
      apt install -y davfs2 rsync && \
      echo "${WEBDAV_SERVER_ADDRESS} ${KABU_PLUS_ID} ${KABU_PLUS_PW}" >> /etc/davfs2/secrets && \
      chmod 600 /etc/davfs2/secrets && \
      chown root:root /etc/davfs2/secrets && \
      echo "${WEBDAV_SERVER_ADDRESS} ${MOUNTPOINT} davfs user,noauto 0 0" >> /etc/fstab && \
      mkdir -p ${MOUNTPOINT}

COPY ./Pipfile /opt/sync/
COPY ./Pipfile.lock /opt/sync/

WORKDIR ${WORKDIR}
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile --python=$(which python) --site-packages

ENV DRYRUN='--dry-run'
COPY ./main.py /opt/sync/
COPY ./__init__.py /opt/sync/
COPY cmd.sh /opt/cmd.sh
CMD mount ${MOUNTPOINT} && /bin/bash /opt/cmd.sh