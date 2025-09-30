FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./ 

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ ./

# Build the React app
RUN npm run build

# Use a simple web server to serve the build
FROM nginx:stable-alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]