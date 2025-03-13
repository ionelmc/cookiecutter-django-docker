# syntax=docker/dockerfile:{{ cookiecutter.__dockerfile_version }}
FROM python:{{ cookiecutter.__python_version }}-{{ cookiecutter.__debian_release }} as deps

# DEBIAN_FRONTEND=noninteractive exists to prevent tzdata going nuts.
# Maybe dpkg incorrectly detects interactive on buildkit containers?
RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    echo "deb http://apt.postgresql.org/pub/repos/apt {{ cookiecutter.__debian_release }}-pgdg main {{ cookiecutter.__postgresql_version.split('.')|first }}" > /etc/apt/sources.list.d/pgdg.list
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
    apt-get update
    apt-get install -y --no-install-recommends \
        python3-dev \
        python-is-python3 \
        libpq-dev={{ cookiecutter.__postgresql_version.split('.')|first }}.* libpq5={{ cookiecutter.__postgresql_version.split('.')|first }}.* \
        libgdal-dev \
        libtiff-dev libjpeg-dev libzip-dev libfreetype-dev \
        libwebp-dev tcl-dev tk-dev libffi-dev \
        libmemcached-dev zlib1g-dev libpcre3-dev \
        build-essential git sudo ca-certificates
EOF
RUN <<EOF bash
    set -euxo pipefail
    curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | python - --no-cache --disable-pip-version-check --upgrade --break-system-packages \
    pip=={{ cookiecutter.__pip_version }} setuptools=={{ cookiecutter.__setuptools_version }}
EOF

# This intents to be the sole Dockerfile for the project so allow building variants with different or no dependencies.
COPY --link --from=requirements-context *.txt /requirements/
ARG REQUIREMENTS
ARG CPUCOUNT=1
RUN --mount=type=cache,target=/root/.cache <<EOF bash
    set -eux
    mkdir /deps
    if [[ -n "$REQUIREMENTS" ]]; then
        python -mpip wheel --no-deps --require-hashes --wheel-dir=/deps/wheels --requirement=requirements/$REQUIREMENTS.txt
        ls -al /deps/wheels
    else
        echo 'No REQUIREMENTS defined!'
        exit 1
    fi
EOF

##################################
##################################
FROM python:{{ cookiecutter.__python_version }}-{{ cookiecutter.__debian_release }} as certs
##################################
ARG SERVER_NAME="localhost"
RUN mkdir /certs \
 && openssl req -x509 -nodes -newkey rsa:4096 -sha256 \
                -out /certs/fullchain.pem -keyout /certs/privkey.pem \
                -subj "/CN=$SERVER_NAME"

#################
#################
FROM python:{{ cookiecutter.__python_version }}-slim-{{ cookiecutter.__debian_release }}
#################
RUN test -e /etc/apt/apt.conf.d/docker-clean # sanity check

RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    apt-get update
    apt-get install -y --no-install-recommends \
        curl software-properties-common gpg-agent
    echo "deb http://apt.postgresql.org/pub/repos/apt {{ cookiecutter.__debian_release }}-pgdg main {{ cookiecutter.__postgresql_version.split('.')|first }}" > /etc/apt/sources.list.d/pgdg.list
    echo "deb http://nginx.org/packages/mainline/debian/ {{ cookiecutter.__debian_release }} nginx" > /etc/apt/sources.list.d/nginx.list
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
    curl http://nginx.org/keys/nginx_signing.key | gpg --dearmor > /etc/apt/trusted.gpg.d/nginx.org.gpg
    apt-get update
    apt-get install -y --no-install-recommends \
        strace ltrace gdb lsof locate net-tools htop iputils-ping dnsutils \
        nano vim tree less telnet socat byobu \
        rsync moreutils \
        graphviz \
        dumb-init \
        libpq5={{ cookiecutter.__postgresql_version.split('.')|first }}.* postgresql-client-{{ cookiecutter.__postgresql_version.split('.')|first }} \
        python3-dbg \
        python3-gdal gdal-bin \
        python-is-python3 \
        libmemcached11 libpcre3 \
        sudo ca-certificates \
        nginx \
        gettext \
        tzdata
EOF

ARG TZ={{ cookiecutter.timezone }}

# Force a sensible default encoding (affects terminal output and filename handling).
# See: https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/uwsgi/
# Note that for en_US.UTF-8 you need to install and compile locales, seems overkill...
ENV LANG=C.UTF-8

ENV TZ=$TZ
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata
RUN <<EOF bash
    set -euxo pipefail
    curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | python - --no-cache --disable-pip-version-check --upgrade --break-system-packages \
        uv=={{ cookiecutter.__uv_version }}
EOF

RUN --mount=type=bind,from=deps,src=/deps,target=/deps <<EOF bash
    set -eux
    if [[ -e /deps/wheels ]]; then
        uv pip install \
            --link-mode=copy \
            --compile-bytecode \
            --no-python-downloads \
            --system \
            --reinstall \
            --no-build \
            --upgrade --no-index --no-deps --break-system-packages /deps/wheels/*
    else
        echo 'No wheels built!'
        exit 1
    fi
EOF
# Adds a new user named python and add it to the list of sudoers. Will be able to call sudo without the password.
# This is more geared to development (eg: match user's UID) than production (where you shouln't need any sudo/home).
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN <<EOF bash
    set -eux
    groupadd --gid $GROUP_ID app
    useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home app
    echo "app ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
EOF

ENV PYTHONUNBUFFERED=x
ENV PYTHONFAULTHANDLER=x

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

ARG DJANGO_SECRET_KEY="n/a"
ARG SERVER_NAME="localhost"
ENV SERVER_NAME=$SERVER_NAME

RUN mkdir -p /app /var/app/logs /var/app/static /var/app/run /etc/app /etc/app-defaults /etc/app-latest \
             /shared/$SERVER_NAME/etc /shared/$SERVER_NAME/logs \
 && chown -R app:app /app /var/app/logs /var/app/run

ENV PYTHONPATH=/app/src
# Using 'EOF' instead of EOF to prevent substitutions on $
RUN <<'EOF' bash
    set -eux
    pth_location=$(python -c 'print(__import__("sysconfig").get_path("purelib"))')
    mkdir -p $pth_location
    echo /app/src > $pth_location/app.pth
EOF
RUN ln -sf /proc/self/fd/2 /var/app/logs/error.log \
 && ln -sf /proc/self/fd/2 /shared/$SERVER_NAME/logs/error.log \
 && ln -sf /proc/self/fd/1 /shared/$SERVER_NAME/logs/access.log

WORKDIR /app

# Note that the trailing slash is significant.
COPY --link entrypoint.sh /
COPY --link uwsgi.ini /etc/app-latest/
{%- if cookiecutter.worker == "rq" %}
COPY --link worker.ini /etc/app-latest/
{%- endif %}
COPY --link nginx.conf /etc/app-latest/
COPY --link nginx.site /etc/app-latest/
COPY --link yacron.yml /etc/app-latest/
COPY --link --from=certs --chmod=0644 /certs/* /etc/app-defaults/

ARG SERVER_NAME="localhost"
RUN <<EOF bash
    set -euxo pipefail
    envsubst '\$SERVER_NAME' < /etc/app-latest/nginx.site | sponge /etc/app-latest/nginx.site
EOF
RUN cp /etc/app-defaults/fullchain.pem /etc/app-defaults/chain.pem \
 && ln -sf /etc/app/nginx.conf /etc/nginx/nginx.conf \
 && cp /etc/nginx/mime.types /etc/app-latest \
 && chmod -R go+r /etc/app

COPY --link --from=src-context . /app/src

RUN python -mcompileall /app/src

ARG DJANGO_COLLECTSTATIC
RUN <<EOF bash
    set -eux
    if [[ -n "$DJANGO_COLLECTSTATIC" ]]; then
        __strict_env__=false django-admin collectstatic --noinput --clear -v0
    fi
EOF

ENTRYPOINT ["/entrypoint.sh"]
