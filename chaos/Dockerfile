FROM python:3.7-alpine

ADD requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps libffi-dev openssl-dev gcc python3-dev musl-dev && \
    apk add tzdata git tar && \
    echo "Europe/London" >  /etc/timezone && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps && \
    rm -rf /tmp/* /root/.cache

VOLUME ["/var/log/chaostoolkit"]

ARG EXPERIMENT_URL = /tmp/experiment.json

COPY ${EXPERIMENT_URL} experiment.json

ENTRYPOINT ["/usr/local/bin/chaos","run","${EXPERIMENT_URL}"]
CMD ["--help"]
