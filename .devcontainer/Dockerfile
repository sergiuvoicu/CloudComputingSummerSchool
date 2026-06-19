# syntax=docker/dockerfile:1
#
# Toolchain image for the Cloud Computing lab devcontainer.
# Contains ONLY the toolchain (Python 3.13, Node 20, uv, AWS CLI).
# The repo's JS/Python deps are installed at container-create time from the
# repo's lockfiles (package-lock.json, uv.lock) via devcontainer.json's
# postCreateCommand.
#
# amd64-only: GitHub Codespaces VMs are always x86_64, so a single-arch
# image is all that's needed.
#
# Build and push in step 3:
#   docker build -t ghcr.io/<owner>/ccss-devcontainer:1.0 .
#   docker push   ghcr.io/<owner>/ccss-devcontainer:1.0

# Debian + system CPython 3.13 (matches repo .python-version) + non-root user.
FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# System packages: curl/unzip for the AWS CLI installer; gnupg for NodeSource.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl unzip gnupg \
 && rm -rf /var/lib/apt/lists/*

# --- Node 20 LTS (NodeSource) ---
# serverless 3.40 runs on Node 20; Node 18 is EOL.
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && rm -rf /var/lib/apt/lists/* \
 && node --version && npm --version

# --- AWS CLI v2 (x86_64) ---
RUN curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
 && unzip -q /tmp/awscliv2.zip -d /tmp \
 && /tmp/aws/install \
 && rm -rf /tmp/aws /tmp/awscliv2.zip \
 && aws --version

# --- uv (Python package/venv manager) ---
# The base already provides the system CPython 3.13 the repo targets, so the
# README's `uv ... --no-managed-python` commands work verbatim (uv uses the
# interpreter on PATH instead of downloading its own).
# Pin the uv tag for reproducible builds (replace :latest).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv --version && python --version
