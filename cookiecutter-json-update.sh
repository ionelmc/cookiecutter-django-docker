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

uv pip compile --allow-unsafe --quiet cookiecutter-packages.in --output-file=cookiecutter-packages.txt
update_field django_version "$(grep -oP '(?<=django==).*' cookiecutter-packages.txt | cut -d. -f1-2)"
update_field pip_tools_version "$(grep -oP '(?<=pip-tools==).*' cookiecutter-packages.txt)"
update_field pip_version "$(grep -oP '(?<=pip==).*' cookiecutter-packages.txt)"
update_field dockerfile_version "$(grep -oP '(?<="_dockerfile_version": ")(.*)(?=")' cookiecutter.json)"
update_field memcached_version "$(grep -oP '(?<="_memcached_version": ")(.*)(?=")' cookiecutter.json)"
update_field postgresql_version "$(grep -oP '(?<="_postgresql_version": ")(.*)(?=")' cookiecutter.json)"
update_field python_version "$(grep -oP '(?<="_python_version": ")(.*)(?=")' cookiecutter.json)"
update_field redis_version "$(grep -oP '(?<="_redis_version": ")(.*)(?=")' cookiecutter.json)"
update_field setuptools_version "$(grep -oP '(?<=setuptools==).*' cookiecutter-packages.txt)"
update_field ubuntu_release "$(grep -oP '(?<="_ubuntu_release": ")(.*)(?=")' cookiecutter.json)"
update_field ubuntu_version "$(grep -oP '(?<="_ubuntu_version": ")(.*)(?=")' cookiecutter.json)"
update_field uv_version "$(grep -oP '(?<=uv==).*' cookiecutter-packages.txt)"


rm cookiecutter-packages.txt

