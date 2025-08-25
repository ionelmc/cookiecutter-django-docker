#!/bin/bash
set -euxo pipefail
shopt -s extglob

update_field() {
    set +x
    field="$1"
    value="$2"
    cookiecutter_json=$(cat cookiecutter.json | jq ._$field=\"$value\" | jq ".__prompts__.$field=\"$field (latest=$value)\"" )
    echo "$cookiecutter_json" > cookiecutter.json
    set -x
}

python_version="$(grep -oP '(?<="_python_version": ")(.*)(?=")' cookiecutter.json)"

update_field python_version $python_version
update_field dockerfile_version "$(grep -oP '(?<="_dockerfile_version": ")(.*)(?=")' cookiecutter.json)"
update_field memcached_version "$(grep -oP '(?<="_memcached_version": ")(.*)(?=")' cookiecutter.json)"
update_field postgresql_version "$(grep -oP '(?<="_postgresql_version": ")(.*)(?=")' cookiecutter.json)"
update_field redis_version "$(grep -oP '(?<="_redis_version": ")(.*)(?=")' cookiecutter.json)"
update_field debian_release "$(grep -oP '(?<="_debian_release": ")(.*)(?=")' cookiecutter.json)"


update_package() {
    field="$1"
    package="$2"

    uv pip compile --python=python$python_version --upgrade --resolution=highest <(echo $package) --output-file=cookiecutter-packages.txt
    update_field $field "$(grep -oPm1 '(?<='$package'==).*' cookiecutter-packages.txt)"
}

update_package django_version django
update_package pip_tools_version pip-tools
update_package pip_version pip
update_package setuptools_version setuptools
update_package uv_version uv

rm cookiecutter-packages.txt

