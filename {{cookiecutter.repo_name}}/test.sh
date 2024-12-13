#!/bin/bash
set -euxo pipefail

if [[ "$@" == "--help" || "$@" == "-h" ]]; then
    set +x
    echo "
Usage: ./test.sh command-to-run arguments

Examples:

- run the default (pytest):

    ./test.sh

- run pytest with arguments:

    ./test.sh pytest -k mytest

- make migrations:

    ./test.sh django-admin makemigrations

- do interactive stuff:

    ./test.sh bash

- update the requirements (also automatically run if you don't have any requirements/*.txt):

    ./test.sh requirements

- disable building:

    NOBUILD=1 ./test.sh

- disable service teardown (faster but less safe runs):

    NOCLEAN=1 ./test.sh
"
    exit 0
fi

export COMPOSE_PROJECT_NAME="test{{ cookiecutter.compose_project_name }}"
export COMPOSE_FILE=docker-compose.test.yml

USER="${USER:-$(id -nu)}"
if [[ "$(uname)" == "Darwin" ]]; then
    USER_ID=1000
    GROUP_ID=1000
else
    USER_ID="$(id -u "$USER")"
    GROUP_ID="$(id -g "$USER")"
fi
BUILD_ARGS="--build-arg USER_ID=$USER_ID --build-arg GROUP_ID=$GROUP_ID --build-arg BUILDKIT_INLINE_CACHE=1"

if [[ -z "$(find requirements -maxdepth 1 -name '*.txt' -print -quit)" ]] || [[ "$*" == "requirements" ]]; then
    set -x
    docker compose build $BUILD_ARGS requirements
    mkdir -p .home/requirements
    chown -R $USER_ID .home/requirements
    docker compose run --rm --user=$USER_ID requirements
    if [[ "$*" == "requirements" ]]; then
        exit
    fi
    set +x
fi

if [[ "${1:-}" == "docker" ]]; then
    set -x
    exec "$@"
elif [[ "${1:-}" == "build" ]]; then
    shift
    set -x
    exec docker compose build $BUILD_ARGS "$@"
fi

if [[ -z "${NOBUILD:-}" ]]; then
    docker compose build $BUILD_ARGS
fi

set -x

if [[ -z "$*" ]]; then
    set -- pytest
fi

homedir=$(dirname ${BASH_SOURCE[0]})/.home
if [[ ! -e $homedir ]]; then
    # create it here so Docker don't create with root ownership
    mkdir $homedir
fi

function cleanup() {
    echo "Saving logs to docker-compose.log"
    docker compose logs --no-color &> docker-compose.log
    echo "Cleaning up ..."
    docker compose down && docker compose rm -fv
}
if [[ -n "${NODEPS:-}" ]]; then
    exec docker compose run -e NODEPS=yes --no-deps --rm --user=$USER_ID test "$@"
else
    if [[ -z "${NOCLEAN:-}" ]]; then
        trap cleanup EXIT
        cleanup || echo "Already clean :-)"
    fi
    docker compose run --rm --user=$USER_ID test "$@"
fi
