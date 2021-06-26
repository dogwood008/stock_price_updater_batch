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

RUN mkdir -p /opt/sync
WORKDIR /opt/sync
COPY ./main.py /opt/sync/
COPY ./__init__.py /opt/sync/
COPY ./Pipfile /opt/sync/
COPY ./Pipfile.lock /opt/sync/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile --python=$(which python) --site-packages

CMD python /opt/sync/main.py