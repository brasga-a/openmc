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
mkdir -p "${APP_DIR}"
TMP_ENV="$(mktemp -d "${APP_DIR}/.env.XXXXXXXX")"
BACKUP_ENV=""
cleanup() {
    rm -rf "${TMP_DIR}" "${TMP_ENV}"
}
trap cleanup EXIT

echo "==> Fetching branch ${REPO_BRANCH}..."
git clone --depth 1 --branch "${REPO_BRANCH}" --quiet "${REPO_URL}" "${TMP_DIR}/openmc"

echo "==> Creating an isolated Python environment..."
python3 -m venv "${TMP_ENV}"
"${TMP_ENV}/bin/python" -m pip install --quiet "${TMP_DIR}/openmc"

echo "==> Installing executable..."
if [[ -d "${INSTALL_DIR}" ]]; then
    BACKUP_ENV="$(mktemp -d "${APP_DIR}/.env-backup.XXXXXXXX")"
    rmdir "${BACKUP_ENV}"
    mv "${INSTALL_DIR}" "${BACKUP_ENV}"
fi
if ! mv "${TMP_ENV}" "${INSTALL_DIR}"; then
    if [[ -n "${BACKUP_ENV}" ]]; then
        mv "${BACKUP_ENV}" "${INSTALL_DIR}"
    fi
    exit 1
fi

mkdir -p "${BIN_DIR}"
ln -sf "${INSTALL_DIR}/bin/openmc" "${BIN_DIR}/openmc"
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
