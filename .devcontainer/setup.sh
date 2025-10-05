#!/bin/bash
# Auto-activate virtual environment for dev container

# Add automatic activation to .bashrc
echo 'if [ -f /workspaces/amidakuji/.venv/bin/activate ]; then' >> ~/.bashrc
echo '    source /workspaces/amidakuji/.venv/bin/activate' >> ~/.bashrc
echo 'fi' >> ~/.bashrc

# Also activate for current session
if [ -f /workspaces/amidakuji/.venv/bin/activate ]; then
    source /workspaces/amidakuji/.venv/bin/activate
fi