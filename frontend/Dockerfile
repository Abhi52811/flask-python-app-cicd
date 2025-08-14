# frontend/Dockerfile
# SIMPLIFIED: No entrypoint script needed.
FROM nginx:1.21.6-alpine

# Copy the corrected Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the static website files
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/

# The base Nginx image will automatically run Nginx. No CMD or ENTRYPOINT needed.