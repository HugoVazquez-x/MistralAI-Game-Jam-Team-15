# Use Python base image as the primary environment
FROM python:3.10-alpine AS final

# Install required dependencies for Python and Nginx
RUN apk add --no-cache nginx supervisor

# Set working directory for the API
WORKDIR /app

COPY ./requirements.txt /app
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API files into the container
COPY ./src /app
COPY ./src/config /src/config

# Copy Unity WebGL build files to Nginx HTML folder
COPY ./unity-game/Builds/WebGL /usr/share/nginx/html

# Remove the default Nginx config and add our custom one
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose only port 8080
EXPOSE 8080

# Copy supervisord config to manage both processes (Nginx & Flask)
COPY supervisord.conf /etc/supervisord.conf

# Start both services using supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
