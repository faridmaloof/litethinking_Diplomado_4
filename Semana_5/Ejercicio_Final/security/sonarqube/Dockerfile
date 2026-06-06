FROM sonarqube:community

LABEL maintainer="QA Engineering Course"

# Create quality gates directory
RUN mkdir -p /opt/sonarqube/quality-gates

# Expose SonarQube web interface
EXPOSE 9000

# Default command is handled by base image