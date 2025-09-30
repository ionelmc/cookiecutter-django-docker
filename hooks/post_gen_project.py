import glob
import os
import random
import shutil
import subprocess
from os.path import join

try:
    from click.termui import secho
except ImportError:
    warn = note = print
else:
    def warn(text):
        for line in text.splitlines():
            secho(line, fg="magenta", bold=True)


    def note(text):
        for line in text.splitlines():
            secho(line, fg="yellow", bold=True)


def unlink_if_exists(path):
    if os.path.exists(path):
        os.unlink(path)


def replace_content(filename, what, replacement):
    with open(filename) as fh:
        content = fh.read()
    with open(filename, 'w') as fh:
        fh.write(content.replace(what, replacement))


if __name__ == "__main__":
    print("""
################################################################################
################################################################################

    You have succesfully created `{{ cookiecutter.repo_name }}`.

################################################################################

    You've used these cookiecutter parameters:
{% for key, value in cookiecutter.items()|sort %}
        {{ "{0:26}".format(key + ":") }} {{ "{0!r}".format(value).strip("u") }}
{%- endfor %}

    See .cookiecutterrc for instructions on regenerating the project.

""")
    if os.name == 'nt':
        replace_content('.env-windows', 'd:\projects\{{ cookiecutter.repo_name }}', os.getcwd())
    if not glob.glob('requirements/*.txt'):
        warn('+ ./test.sh requirements')
        subprocess.check_call(['./test.sh', 'requirements'])
    if not os.path.exists('.git'):
        warn('+ git init')
        subprocess.check_call(['git', 'init'])

{%- if cookiecutter.worker == "rq" %}
    os.unlink(join('src', '{{ cookiecutter.django_project_name }}', 'celery.py'))
{%- elif cookiecutter.worker == "celery" %}
    os.unlink(join('docker', 'python', 'worker.ini'))
{%- else %}
    os.unlink(join('src', '{{ cookiecutter.django_app_name }}', 'tasks.py'))
    os.unlink(join('src', '{{ cookiecutter.django_project_name }}', 'celery.py'))
    os.unlink(join('docker', 'python', 'worker.ini'))
{%- endif %}
    if os.path.exists('.isort.cfg'):
        os.unlink('.isort.cfg')
    if os.path.exists('setup.cfg'):
        os.unlink('setup.cfg')

    if os.path.exists(join('deploy', '{{cookiecutter.deploy_name}}', '.env')):
        os.unlink(join('deploy', '{{cookiecutter.deploy_name}}', '.env-sample'))
    else:
        os.rename(join('deploy', '{{cookiecutter.deploy_name}}', '.env-sample'), join('deploy', '{{cookiecutter.deploy_name}}', '.env'))

    if not os.path.exists('.env'):
        warn("You don't have an .env file yet. The default linux one is being copied for you...")
        note('+ cp .env-linux-osx .env')
        shutil.copy('.env-linux-osx', '.env')

{%- if cookiecutter.docker_lock %}
    note('+ docker lock generate --update-existing-digests --dockerfile-recursive --composefiles=docker-compose.common.yml')
    subprocess.check_call(['docker', 'lock', 'generate', '--update-existing-digests', '--dockerfile-recursive', '--composefiles=docker-compose.common.yml'])
    note('+ docker lock rewrite --tempdir .')
    subprocess.check_call(['docker', 'lock', 'rewrite', '--tempdir', '.'])
    note('+ docker lock verify --update-existing-digests')
    subprocess.check_call(['docker', 'lock', 'verify', '--update-existing-digests'])
{%- endif %}

    note('+ pre-commit autoupdate')
    subprocess.check_call(['pre-commit', 'autoupdate'])

    warn("""
################################################################################

    The project is ready!

        cd {{ cookiecutter.repo_name }}

    To get started make sure you have the appropriate platform .env file:

        cp .env-linux-osx .env
          or
        cp .env-windows .env

    To update concrete requirements (.txt files):

        ./test.sh requirements

    To run tests:

        ./test.sh

    To build the project:

        docker compose build --pull

    You can bring up the project with:

        docker compose up

    Install pre-commit hooks with:

        pre-commit install --install-hooks --overwrite

    Or if you have prek installed:

        prek install --install-hooks --overwrite
    """)
