#!/bin/bash

# ai_exec.sh - Wrapper to ensure mise env is loaded in non-interactive shells

# Check if mise is already loaded in this session
if [ "$MISE_FOR_AI" != "1" ]; then
    # Attempt to load mise environment
    if command -v mise &> /dev/null; then
        eval "$(mise env)"
        export MISE_FOR_AI=1
    else
        echo "⚠️ mise not found, proceeding without it..."
    fi
fi

# Execute the provided command
exec "$@"
