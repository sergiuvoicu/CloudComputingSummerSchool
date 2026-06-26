#!/usr/bin/env bash
# Runs once when the codespace/devcontainer is created.
# Replays the repo README's Setup steps so the environment is deploy-ready.
set -eo pipefail

echo "▶ Installing Node/Serverless dependencies (npm ci)…"
npm ci

echo "▶ Building the Lambda layer venv (dependencies/python)…"
rm -rf dependencies/python
uv venv dependencies/python --no-managed-python
# shellcheck disable=SC1091
source dependencies/python/bin/activate
uv sync --active --locked --no-managed-python
deactivate

echo "▶ Building the local dev venv (.venv)…"
rm -rf .venv
uv venv --no-managed-python
# shellcheck disable=SC1091
source .venv/bin/activate
uv sync --active --locked --no-managed-python
deactivate

echo
echo "Toolchain:"
echo "  node    $(node --version)"
echo "  python  $(python --version)"
echo "  uv      $(uv --version)"
echo "  aws     $(aws --version 2>&1 | head -n1)"
echo "  sls     $(./node_modules/.bin/serverless --version 2>/dev/null | head -n1)"

echo
echo "▶ Verifying AWS credentials…"
if acct=$(aws sts get-caller-identity --query Account --output text 2>/dev/null); then
  echo "  ✅ AWS credentials OK — account ${acct}, region ${AWS_REGION}"
else
  echo "  ⚠️  No AWS credentials detected."
  echo "     Add Codespaces secrets AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY,"
  echo "     then rebuild the container (Cmd/Ctrl-Shift-P → Rebuild Container)."
fi

echo
echo "✅ Environment ready."
echo "   Deploy:  ./node_modules/.bin/serverless deploy --stage <your-stage> --region eu-north-1 --config serverless.yml"
echo "   Rebuild the layer after changing deps:  bash .devcontainer/post-create.sh"
