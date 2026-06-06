FROM mitmproxy/mitmproxy:9.0.1

LABEL maintainer="QA Engineering Course"

# Install Python dependencies
RUN pip install watchdog

# Copy mitmproxy addons
COPY mitmproxy/addons/ /home/mitmproxy/addons/

# Copy example rules to the container
COPY mitmproxy/config/rules/ /home/mitmproxy/config/rules/

# Set working directory
WORKDIR /home/mitmproxy

# Create config directory for rules
RUN mkdir -p /home/mitmproxy/config/rules

# Expose ports
EXPOSE 8080 8081

# Start mitmweb with our addon, binding to all interfaces
CMD ["mitmweb", "--listen-host", "0.0.0.0", "--listen-port", "8080", "-s", "/home/mitmproxy/addons/interceptor.py", "--web-host", "0.0.0.0", "--web-port", "8081"]