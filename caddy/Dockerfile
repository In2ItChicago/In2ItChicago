FROM caddy:2.1.1-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY *caddy-private.pem /etc/ssl/private/key.pem
COPY *caddy-public.pem /etc/ssl/certs/certificate.pem