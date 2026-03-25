#!/bin/bash

# check_env.sh - Verify mise installation and shell integration

echo "Checking Mise environment..."

if command -v mise &> /dev/null; then
    echo "✅ mise is installed: $(mise --version)"
else
    echo "❌ mise is not installed in PATH."
    exit 1
fi

if [[ ":$PATH:" == *":$HOME/.local/share/mise/shims:"* ]]; then
    echo "✅ mise shims are in PATH."
else
    echo "⚠️ mise shims are NOT in PATH. You may need to add 'eval \"\$(mise activate --shims)\"' to your profile."
fi

if [[ -n "$MISE_SHELL" ]]; then
    echo "✅ mise is activated in the current shell ($MISE_SHELL)."
else
    echo "⚠️ mise is not activated in the current shell."
fi

echo "Environment check complete."
