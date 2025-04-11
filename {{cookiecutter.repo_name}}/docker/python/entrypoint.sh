#!/bin/bash
set -euxo pipefail
mkdir -p /var/app/run /var/app/static /var/app/media /var/app/logs
chown -R app:app /var/app || true

# Copy files in the /etc/app volume. Note that the "/" suffix is significant.
rsync --itemize-changes --ignore-existing --recursive --links /etc/app-defaults/ /etc/app
rsync --itemize-changes --backup --info=backup --checksum --suffix=".$(date +'%Y%m%d%H%M%S')~" --recursive /etc/app-latest/ /etc/app

set +x
if [[ -n "${DJANGO_COLLECTSTATIC:-}" ]]; then
  set -x
  pysu app django-admin collectstatic --noinput --clear -v0
  set +x
fi
if [[ -n "${DJANGO_DB_MIGRATE:-}" ]]; then
  set -x
  holdup --verbose "pg://$DJANGO_DB_USER:$DJANGO_DB_PASSWORD@$DJANGO_DB_HOST:$DJANGO_DB_PORT/$DJANGO_DB_NAME"
  pysu app django-admin migrate --noinput --fake-initial
  set +x
fi
set -x
exec "$@"
