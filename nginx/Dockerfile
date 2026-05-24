FROM nginx:alpine

# pg / my（对应 conf.d 下文件名，不含 .conf 后缀）
ARG NGINX_SITE=pg
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf.d/${NGINX_SITE}.conf /etc/nginx/conf.d/site.conf

# 避免与 site.conf 抢 80 端口；静态资源由 compose 挂载 dist
RUN rm -f /etc/nginx/conf.d/default.conf \
    && mkdir -p /usr/share/nginx/html
