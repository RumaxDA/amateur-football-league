FROM dhi.io/node:24-alpine3.22-dev AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm npm ci

COPY . .
RUN npm run build 

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

COPY --from=builder /app/dist/*/browser /usr/share/nginx/html

RUN echo 'server { \
    listen 8080; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html; \
    try_files $uri $uri/ /index.html; \
    } \
    }' > /etc/nginx/conf.d/default.conf

RUN chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 8080