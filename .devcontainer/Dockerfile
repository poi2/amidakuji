# Use official Python Dev Container image as base
# This includes git and common development tools pre-installed
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Set non-interactive to suppress prompts during apt-get execution
ENV DEBIAN_FRONTEND=noninteractive

# Update system packages and install additional libraries if needed
# (No additional packages needed for this example, but can be added here)
RUN apt-get update && apt-get -y install --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv system-wide
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    mv /root/.local/bin/uvx /usr/local/bin/uvx && \
    chmod +x /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uvx

# Switch to non-root user 'vscode' used by VS Code
# Must match remoteUser setting
USER vscode
