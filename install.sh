#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/brasga-a/openmc.git"
INSTALL_DIR="${HOME}/.local/share/openmc/env"
BIN_DIR="${HOME}/.local/bin"

echo "==> Installing OpenMC..."

# 1. Check dependencies
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed. Please install Python 3 first." >&2
    exit 1
fi

if ! command -v git >/dev/null 2>&1; then
    echo "Error: git is not installed. Please install git first." >&2
    exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Error: python3-venv is not available. Please install the python3-venv package for your distribution." >&2
    exit 1
fi

# 2. Clone repository to a temporary directory
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

echo "==> Fetching source code from ${REPO_URL}..."
git clone --depth 1 --quiet "${REPO_URL}" "${TMP_DIR}/openmc"

# 3. Create isolated virtual environment
echo "==> Setting up isolated Python environment at ${INSTALL_DIR}..."
rm -rf "${INSTALL_DIR}"
mkdir -p "$(dirname "${INSTALL_DIR}")"
python3 -m venv "${INSTALL_DIR}"

# 4. Install OpenMC and its dependencies via pip
echo "==> Installing packages..."
"${INSTALL_DIR}/bin/pip" install --quiet --upgrade pip
"${INSTALL_DIR}/bin/pip" install --quiet "${TMP_DIR}/openmc"

# 5. Symlink executable to ~/.local/bin
mkdir -p "${BIN_DIR}"
ln -sf "${INSTALL_DIR}/bin/openmc" "${BIN_DIR}/openmc"

echo ""
echo "==> OpenMC installed successfully!"

if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo ""
    echo "Note: ${BIN_DIR} is not in your PATH."
    echo "Add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\${HOME}/.local/bin:\${PATH}\""
fi

echo "Run 'openmc --help' to get started."
