#!/bin/sh
HTML_FILE=/usr/share/nginx/html/index.html
NGINX_CONF_FILE=/etc/nginx/conf.d/default.conf

# This is the new, more robust check.
# It checks if the variable is truly unset.
if [ -z "${BACKEND_URL+x}" ]; then
  echo "FATAL: BACKEND_URL environment variable is not set."
  exit 1
fi

echo "Configuring frontend with backend URL: ${BACKEND_URL}"
sed -i "s#{{BACKEND_URL_PLACEHOLDER}}#${BACKEND_URL}#g" $HTML_FILE

LISTEN_PORT=${PORT:-80}
echo "Configuring Nginx to listen on port: ${LISTEN_PORT}"
sed -i "s/{{PORT}}/${LISTEN_PORT}/g" $NGINX_CONF_FILE

exec "$@"