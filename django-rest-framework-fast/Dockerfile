# Base Image
FROM python:3-alpine

# Set execution environment
COPY requirements /requirements

# Install dependencies from repository
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
            jpeg-dev \
            zlib-dev \
    && python -m venv --upgrade /ourenv \
    && /ourenv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/ourenv/bin/pip install --no-cache-dir -r /requirements/dev.txt" \
    && run_deps="$( \
            scanelf --needed --nobanner --recursive /ourenv \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $run_deps \
    && apk del .build-deps

RUN apk add --no-cache \
    curl \
    openssh \
    bash

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

ENV IN_DOCKER=True

RUN /ourenv/bin/python manage.py migrate
RUN /ourenv/bin/python manage.py collectstatic --noinput
CMD /ourenv/bin/gunicorn config.wsgi
