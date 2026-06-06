FROM ghcr.io/zaproxy/zaproxy:stable

LABEL maintainer="QA Engineering Course"

# Create policies directory
RUN mkdir -p /home/zap/policies

# Set working directory
WORKDIR /home/zap

# Expose ZAP API port
EXPOSE 8090

# Default command
CMD ["zap.sh", "-daemon", "-host", "0.0.0.0", "-port", "8090", "-config", "api.addrs.addr.name=.*", "-config", "api.addrs.addr.regex=true"]