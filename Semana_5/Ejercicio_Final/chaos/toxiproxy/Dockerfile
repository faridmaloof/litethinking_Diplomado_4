FROM ghcr.io/shopify/toxiproxy:latest

LABEL maintainer="QA Engineering Course"

# Expose ToxiProxy API and proxy ports
EXPOSE 8474 8475

# Default command
CMD ["toxiproxy-server", "-host", "0.0.0.0", "-port", "8474"]