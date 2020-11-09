FROM haproxy:1.7

# copy haproxy configuration into the container
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# copy ssl certificate into the container
COPY private/* /private/

# create haproxy user & group
RUN groupadd haproxy && useradd -g haproxy haproxy

# HAProxy requires /var/lib/haproxy/run/haproxy/ to be created before it's run
RUN mkdir -p /var/lib/haproxy/run/haproxy/

EXPOSE 80
EXPOSE 443