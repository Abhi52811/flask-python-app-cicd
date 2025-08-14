# frontend/Dockerfile
FROM nginx:1.21.6-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]