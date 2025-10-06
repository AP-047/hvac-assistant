# Stage 1: Build the React app
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --only=production

# Copy the rest of the source code and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Serve with NGINX
FROM nginx:stable-alpine

# Copy built files to NGINX's html directory
COPY --from=builder /app/build /usr/share/nginx/html

# Replace default NGINX config with the proxy config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]