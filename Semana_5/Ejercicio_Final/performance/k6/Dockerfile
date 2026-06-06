FROM grafana/k6:latest

LABEL maintainer="QA Engineering Course"

# Create scripts directory
RUN mkdir -p /scripts

# Set working directory
WORKDIR /scripts

# Copy default test script if needed
COPY scripts/* /scripts/ 2>/dev/null || echo "No scripts found, will mount volume"

# Default command is handled by k6