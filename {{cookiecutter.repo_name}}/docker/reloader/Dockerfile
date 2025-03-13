# syntax=docker/dockerfile:{{ cookiecutter.__dockerfile_version }}
FROM python:{{ cookiecutter.__python_version }}-slim-{{ cookiecutter.__debian_release }}

# Note: this uses python (debian) as the base instead of a more lightweight image
# like alpine because fswatch ain't in alpine and we want to use it instead
# of inotifywait which only supports Linux
# (iow: to support Docker for Windows and other setups with strange storage)

RUN test -e /etc/apt/apt.conf.d/docker-clean # sanity check

RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    apt-get update
    apt-get install -y --no-install-recommends \
                    fswatch docker.io docker-compose-v2 dumb-init
EOF
WORKDIR /app

COPY start.sh /

ENTRYPOINT ["dumb-init"]
CMD ["/start.sh"]
