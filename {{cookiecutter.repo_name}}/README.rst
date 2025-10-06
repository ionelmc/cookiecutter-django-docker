{{ "=" * cookiecutter.name|length }}
{{ cookiecutter.name }}
{{ "=" * cookiecutter.name|length }}

{{ cookiecutter.short_description|wordwrap(119) }}

Development
===========

Upon cloning the project for the first time

Set up your environment
-----------------------

Select ``.env-linux-osx`` or ``.env-windows`` (depending on your OS) and rename to ``.env``.

Change the file according to the comments in the example file.

Docker Compose will refuse to build the project if a .env file is missing.

This project setup assumes you have followed the
`Docker post-installation steps <https://docs.docker.com/engine/install/linux-postinstall/>`_ and you can access the Docker daemon without
sudo.


Managing requirements
---------------------

Python requirements are managed with uv - abstract requirements are in ".in" files while concrete requirements (pins) are in ".txt"
files.

There is a shim to update all the files correctly (using uv installed in a correct environment) - just run::

    ./test.sh requirements

Running the application
-----------------------

For one-off commands::

    docker compose run --rm web pysu app yourcommand

To start the project::

    docker compose up

Alternatively you can do this to avoid stopping containers unnecesarily::

    docker compose up -d
    docker compose logs -f


You can then access application in browser via http://localhost:80

Custom compose files
--------------------

To run the app with different compose files, use the -f argument to override whatever is set in the .env file, e.g::

    docker compose -f docker-compose.yml -f docker-compose.johnny.yml up

Alternatively you can edit your ``.env`` file to use ``docker-compose.johnny.yml``.

Migrations
----------

Don't forget to run migrations!

You may either run it as an one-off::

    docker compose run --rm web pysu app django-admin migrate

Or exec a command inside the web container (if it already runs)::

    docker compose exec web pysu app django-admin migrate

.. warning::

    Note that if you don't include the ``pysu app`` part you might get root-owned files all over the place.

Creating migrations
```````````````````

To create migrations is recommended to use ``./test.sh`` as it always runs in a clean environment that won't ever
confuse the migration generator::

    ./test.sh django-admin makemigrations

Reseting the database
`````````````````````

If migrations have been recreated run this to drop all your tables and data, and recreate everything from scratch::

    docker compose build
    # make sure pg is up (other services not needed)
    docker compose up -d pg
    # kill all connections (so we can drop the database)
    docker compose exec pg psql --username=app -c "select pg_terminate_backend(pid) from pg_stat_activity where datname='app' and pid <> pg_backend_pid()"
    # drop 'n recreate
    docker compose exec pg dropdb --username=app app
    docker compose exec pg createdb --username=app app
    # get the database back in an usable state
    docker compose run --rm web pysu app django-admin migrate
    docker compose run --rm web pysu app django-admin createsuperuser

Windows specifics
-----------------

Docker supports Windows 10 natively, with some caveats of course. Don't forget to:

* Use the correct .env file (copy .env-windows .env)
* Share the drive containing the project in docker's "Shared Drive" settings.

  * If it doesn't work, or it breaks down later use "Reset credentials".
  * Make sure you use your correct Windows username (Docker might not fill in the correct default).

Under the hood docker will run a HyperV vm and use Windows Sharing (smbmount probably) thus it will be slow, symlinks won't
work and the permission system is a bit loose. Good luck!
