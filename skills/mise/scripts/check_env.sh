#!/usr/bin/env bash
# check_env.sh - Verify mise installation, configs, Pattern 1 (Shims), and Pattern 2 (mise exec) readiness

# Enable nullglob across bash and zsh to safely count files
shopt -s nullglob 2>/dev/null || setopt NULL_GLOB 2>/dev/null

echo "Checking Mise environment configuration..."

P1_ACTIVE=false
P2_READY=false

# 1. Base CLI availability
echo "[1/4. Mise CLI Installation]"
if command -v mise &> /dev/null; then
    echo "  ✅ mise CLI is installed: $(mise --version 2>/dev/null || mise --version)"
    P2_READY=true
else
    echo "  ❌ mise CLI is not found in PATH."
    echo ""
    echo "[Agent Action Directive]"
    echo "  👉 Error: Mise CLI is not installed. Fall back to system default binaries or notify the user."
    exit 1
fi

# 2. Config files discovery (Handles first-time setup & custom config paths)
echo "[2/4. Active Configuration Files]"
CONFIG_COUNT=0
while read -r cfg_raw _; do
    [ -z "$cfg_raw" ] && continue
    cfg_file="${cfg_raw/#\~/$HOME}"
    echo "  📁 Config found: $cfg_file"
    CONFIG_COUNT=$((CONFIG_COUNT + 1))
done < <(mise config ls --no-header 2>/dev/null)

if [ "$CONFIG_COUNT" -eq 0 ]; then
    echo "  ℹ️ No active config file detected (First-time setup). You can create one with: mise use <tool>@<version>"
fi

# 3. Dynamic Shims resolution (Handles macOS/Linux, custom MISE_DATA_DIR / XDG paths)
echo "[3/4. Pattern 1 - Shims Mode (Recommended for clean native commands)]"
SHIMS_DIR=""
# Calling `mise activate --shims` lets mise dynamically output the export command for current platform
SHIMS_EXPORT=$(MISE_OFFLINE=1 mise activate --shims 2>/dev/null)
if [[ "$SHIMS_EXPORT" == *"PATH="* ]]; then
    # Parse `export PATH="/path/to/shims:$PATH"` using pure parameter expansion
    SHIMS_DIR="${SHIMS_EXPORT#*PATH=\"}"
    SHIMS_DIR="${SHIMS_DIR#*PATH=}"
    SHIMS_DIR="${SHIMS_DIR%%:*\"*}"
    SHIMS_DIR="${SHIMS_DIR%%:*}"
    SHIMS_DIR="${SHIMS_DIR%\"}"
    SHIMS_DIR="${SHIMS_DIR%\'}"
fi

# Pure fallback if CLI activation output was empty (Check from highest to lowest probability)
if [ -z "$SHIMS_DIR" ]; then
    if [ -d "$HOME/.local/share/mise/shims" ]; then
        SHIMS_DIR="$HOME/.local/share/mise/shims"
    elif [ -n "$XDG_DATA_HOME" ] && [ -d "$XDG_DATA_HOME/mise/shims" ]; then
        SHIMS_DIR="$XDG_DATA_HOME/mise/shims"
    elif [ -n "$MISE_DATA_DIR" ]; then
        SHIMS_DIR="$MISE_DATA_DIR/shims"
    elif [ -n "$MISE_SHIMS_DIR" ]; then
        SHIMS_DIR="$MISE_SHIMS_DIR"
    else
        SHIMS_DIR="$HOME/.local/share/mise/shims"
    fi
fi

# Detect user shell to give tailored recommendations (e.g. macOS zsh vs Linux bash)
USER_SHELL_NAME=$(basename "${SHELL:-bash}")
case "$USER_SHELL_NAME" in
    zsh)
        ACTIVATE_CMD='eval "$(mise activate zsh --shims)"'
        RC_FILE="~/.zprofile (non-interactive/login shell — NOT ~/.zshrc)"
        ;;
    bash)
        ACTIVATE_CMD='eval "$(mise activate bash --shims)"'
        RC_FILE="~/.profile (non-interactive/login shell — NOT ~/.bashrc)"
        ;;
    fish)
        ACTIVATE_CMD='mise activate fish --shims | source'
        RC_FILE="~/.config/fish/config.fish (fish sources this file for both login and non-login shells)"
        ;;
    *)
        ACTIVATE_CMD='eval "$(mise activate --shims)"'
        RC_FILE="your shell's non-interactive/login profile"
        ;;
esac

if [[ ":$PATH:" == *":$SHIMS_DIR:"* ]]; then
    shims_files=("$SHIMS_DIR"/*)
    if [ -d "$SHIMS_DIR" ] && [ -e "${shims_files[0]}" ]; then
        TOOL_COUNT=${#shims_files[@]}
        echo "  ✅ Pattern 1 is ACTIVE: Shims directory is in PATH ($SHIMS_DIR) with $TOOL_COUNT tool shims."
        P1_ACTIVE=true
    else
        echo "  ⚠️ Pattern 1 is INCOMPLETE: Shims directory is in PATH ($SHIMS_DIR), but empty. Run 'mise reshim' to generate shims."
    fi
else
    echo "  ℹ️ Pattern 1 is NOT configured: '$SHIMS_DIR' is not in PATH."
    echo "     👉 Add '$ACTIVATE_CMD' to your $RC_FILE to enable Pattern 1."
fi

# 4. Check Pattern 2: Explicit Execution (mise exec / mise x)
echo "[4/4. Pattern 2 - Explicit Execution (mise exec / mise x)]"
if [ "$P2_READY" = true ]; then
    echo "  ✅ Pattern 2 is READY: 'mise exec -- <cmd>' / 'mise x -- <cmd>' can be used immediately."
fi

# 5. Agent Action Directive
echo ""
echo "[Agent Action Directive]"
if [ "$P1_ACTIVE" = true ]; then
    echo "  👉 Recommended: Use Pattern 1. Execute clean native commands directly (e.g. 'go build', 'uv run ...')."
elif [ "$P2_READY" = true ]; then
    echo "  👉 Recommended: Fallback to Pattern 2. Prefix commands with 'mise exec -- <cmd>' or 'mise x -- <cmd>'."
else
    echo "  👉 Error: Neither pattern available. Notify user that mise is not configured."
fi

echo ""
echo "Environment check complete."
