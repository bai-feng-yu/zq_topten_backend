FROM nginx 
COPY ./dist/ /usr/share/nginx/html/
COPY ./ssl/ /etc/nginx/ssl/
COPY /mime.types /etc/nginx/mime.types
COPY /nginx.conf /etc/nginx/nginx.conf
COPY /nginx.conf /etc/nginx/
COPY /nginx.conf /etc/nginx/conf.d/

EXPOSE 443 80
