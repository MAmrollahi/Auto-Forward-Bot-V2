#!/bin/sh
# Simple start script — ensure this file is executable (chmod +x start.sh)
# It delegates to the Python entrypoint which imports the bot package.
set -e
cd "$(dirname "$0")"
exec python3 main.py