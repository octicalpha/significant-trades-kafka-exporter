FROM        python:3.7-alpine
ARG         APP_DIR=/app/
ARG         SRC_DIR=src
ARG         USER_NAME=stke

WORKDIR     ${APP_DIR}

COPY        ${SRC_DIR}                          ${APP_DIR}/${SRC_DIR}
COPY        docker-entrypoint.sh                ${APP_DIR}
COPY        ${SRC_DIR}/requirements_base.txt    ${APP_DIR}

RUN         set -ex ;\
            addgroup -g 1000 -S $USER_NAME ;\
            adduser -u 1000 -S $USER_NAME -G $USER_NAME ;\
            apk add --no-cache bash gcc musl-dev;\
            pip install -r requirements_base.txt ;\
            chmod +x docker-entrypoint.sh ;\
            rm -rf /var/lib/apt/lists/* ;\
            rm -rf /var/cache/apk/*

ENV         PATH=.:$PATH

USER        $USER_NAME

ENTRYPOINT  ["docker-entrypoint.sh"]

CMD ["run"]
