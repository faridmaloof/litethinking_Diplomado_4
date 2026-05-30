FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css
COPY api.js /usr/share/nginx/html/api.js
COPY renderers.js /usr/share/nginx/html/renderers.js
COPY app.js /usr/share/nginx/html/app.js
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
