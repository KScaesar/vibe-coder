#!/usr/bin/env bash
# check_tool.sh - Pre-execution tool and version inspector for Mise
# Usage: ./check_tool.sh <tool> [target_version]

set -euo pipefail

TOOL="${1:-}"
REQUESTED_VER="${2:-}"

if [ -z "$TOOL" ]; then
    echo "Error: Missing tool argument."
    echo "Usage: $0 <tool> [target_version]"
    exit 1
fi

echo "Checking Mise tool configuration for: $TOOL..."

# 1. Query installed versions via mise ls --json
INSTALLED_JSON=$(mise ls --json "$TOOL" 2>/dev/null || echo "[]")

INSTALLED_VERSIONS=()
ACTIVE_VERSION=""
SOURCE_CONFIG=""

if command -v jq &>/dev/null; then
    while read -r ver is_active src; do
        [ -z "$ver" ] && continue
        INSTALLED_VERSIONS+=("$ver")
        if [ "$is_active" = "true" ]; then
            ACTIVE_VERSION="$ver"
            SOURCE_CONFIG="$src"
        fi
    done < <(echo "$INSTALLED_JSON" | jq -r '.[] | "\(.version) \(.active) \(.source.path // "none")"')
else
    while read -r t_name t_ver t_src t_req; do
        [ "$t_name" != "$TOOL" ] && continue
        [ -z "$t_ver" ] && continue
        INSTALLED_VERSIONS+=("$t_ver")
        if [ -n "$t_src" ] && [ "$t_src" != "none" ]; then
            ACTIVE_VERSION="$t_ver"
            SOURCE_CONFIG="$t_src"
        fi
    done < <(mise ls "$TOOL" 2>/dev/null | tail -n +2)
fi

# 2. Determine target version (User requested or remote latest)
TARGET_VERSION="$REQUESTED_VER"
if [ -z "$TARGET_VERSION" ]; then
    LATEST_RESOLVED=$(mise latest "$TOOL" 2>/dev/null || true)
    if [ -n "$LATEST_RESOLVED" ]; then
        TARGET_VERSION="$LATEST_RESOLVED"
    fi
fi

# 3. Print Diagnostic Status
echo "[1/2. Status]"
if [ ${#INSTALLED_VERSIONS[@]} -eq 0 ]; then
    echo "  Installed: ❌ Not installed"
else
    echo "  Installed: 📦 ${INSTALLED_VERSIONS[*]} (Active: ${ACTIVE_VERSION:-None})"
    [ -n "$SOURCE_CONFIG" ] && echo "  Config   : $SOURCE_CONFIG"
fi
echo "  Target   : ${TARGET_VERSION:-(Unspecified)}"

echo ""
echo "[2/2. Agent Action Directive]"

if [ ${#INSTALLED_VERSIONS[@]} -eq 0 ]; then
    echo "  👉 Case: NEW_INSTALL"
    echo "  • Clarify scope with user (Project vs Global '-g') if unspecified, or execute: 'mise use [-g] $TOOL@${TARGET_VERSION:-latest}'"
    exit 0

elif [ -n "$TARGET_VERSION" ] && [ "$ACTIVE_VERSION" = "$TARGET_VERSION" ]; then
    echo "  👉 Case: ALREADY_ACTIVE"
    echo "  • $TOOL@$ACTIVE_VERSION is already active in config. No command needed."
    exit 0

else
    echo "  👉 Case: VERSION_CHANGE (Active: '${ACTIVE_VERSION:-None}' -> Target: '${TARGET_VERSION:-(Unspecified)}')"
    echo "================================================================================"
    echo "🛑 BLOCKED: Human-In-The-Loop Decision Required (Exit Code 2)"
    echo "DO NOT execute 'mise use' or 'mise upgrade' directly."
    echo "The Agent MUST immediately invoke the 'ask_question' tool to prompt the user."
    echo "================================================================================"
    cat <<EOF
{
  "status": "REQUIRES_USER_DECISION",
  "tool": "$TOOL",
  "active_version": "${ACTIVE_VERSION:-None}",
  "target_version": "${TARGET_VERSION:-(Unspecified)}",
  "ask_question_payload": {
    "questions": [
      {
        "question": "Detected version change for $TOOL (Active: ${ACTIVE_VERSION:-None} -> Target: ${TARGET_VERSION:-(Unspecified)}). How would you like to proceed?",
        "options": [
          "Scenario 1 - In-place upgrade ('mise upgrade $TOOL --bump'): Upgrade version in the existing configuration file",
          "Scenario 2 - Multi-version coexistence & global switch ('mise use -g $TOOL@$TARGET_VERSION'): Install new version and set as global default, preserving old version",
          "Scenario 3 - Project-local switch ('mise use $TOOL@$TARGET_VERSION'): Set version in current project's mise.toml"
        ],
        "is_multi_select": false
      }
    ]
  }
}
EOF
    exit 2
fi
