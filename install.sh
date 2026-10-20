#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/brasga-a/openmc.git"
REPO_BRANCH="main"
DATA_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}"
if [[ "${DATA_HOME}" != /* ]]; then
    DATA_HOME="${HOME}/.local/share"
fi
APP_DIR="${DATA_HOME}/openmc"
INSTALL_DIR="${APP_DIR}/env"
BIN_DIR="${HOME}/.local/bin"

echo "==> Installing OpenMC..."
for command in python3 git; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        echo "Error: ${command} is required." >&2
        exit 1
    fi
done

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Error: Python venv support is required." >&2
    exit 1
fi

TMP_DIR="$(mktemp -d)"
BACKUP_ENV=""
INSTALL_STARTED=0
INSTALL_COMPLETE=0
cleanup() {
    if [[ "${INSTALL_STARTED}" -eq 1 && "${INSTALL_COMPLETE}" -ne 1 ]]; then
        rm -rf "${INSTALL_DIR}"
        if [[ -n "${BACKUP_ENV}" && -d "${BACKUP_ENV}" ]]; then
            mv "${BACKUP_ENV}" "${INSTALL_DIR}"
        fi
    fi
    rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "==> Fetching branch ${REPO_BRANCH}..."
git clone --depth 1 --branch "${REPO_BRANCH}" --quiet "${REPO_URL}" "${TMP_DIR}/openmc"

mkdir -p "${APP_DIR}"
if [[ -d "${INSTALL_DIR}" ]]; then
    BACKUP_ENV="$(mktemp -d "${APP_DIR}/.env-backup.XXXXXXXX")"
    rmdir "${BACKUP_ENV}"
    mv "${INSTALL_DIR}" "${BACKUP_ENV}"
fi

# Create directly at its final path: venv console-script shebangs are absolute.
INSTALL_STARTED=1
echo "==> Creating an isolated Python environment..."
python3 -m venv "${INSTALL_DIR}"
"${INSTALL_DIR}/bin/python" -m pip install --quiet "${TMP_DIR}/openmc"

mkdir -p "${BIN_DIR}"
ln -sf "${INSTALL_DIR}/bin/openmc" "${BIN_DIR}/openmc"
INSTALL_COMPLETE=1
if [[ -n "${BACKUP_ENV}" ]]; then
    rm -rf "${BACKUP_ENV}"
fi

echo "==> OpenMC installed successfully!"
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo "Note: ${BIN_DIR} is not in your PATH."
    echo "For fish: fish_add_path ~/.local/bin"
    echo 'For bash/zsh: export PATH="$HOME/.local/bin:$PATH"'
fi
echo "Run 'openmc --help' to get started."
