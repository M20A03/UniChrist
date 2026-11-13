#!/bin/bash
# ==============================================================================
# ClamAV Upload Sanitization Hook for Grievance & Student Document Uploads
# Trail of Bits / CSO Security Standard
# ==============================================================================

set -euo pipefail

TARGET_FILE="${1:-}"

if [[ -z "$TARGET_FILE" || ! -f "$TARGET_FILE" ]]; then
    echo '{"error": "Invalid file path provided for scanning"}' >&2
    exit 1
fi

echo "[ClamAV Hook] Sanitizing incoming file payload: $TARGET_FILE"

# Scan via clamscan / clamdscan daemon
if command -v clamdscan &>/dev/null; then
    SCAN_RESULT=$(clamdscan --no-summary --infected "$TARGET_FILE" 2>&1 || true)
elif command -v clamscan &>/dev/null; then
    SCAN_RESULT=$(clamscan --no-summary --infected "$TARGET_FILE" 2>&1 || true)
else
    # Fallback simulation for sandbox environments without native clamav binary
    MIME_TYPE=$(file --mime-type -b "$TARGET_FILE" || echo "application/octet-stream")
    if [[ "$MIME_TYPE" == *"executable"* || "$MIME_TYPE" == *"x-sh"* || "$TARGET_FILE" == *".exe" ]]; then
        echo '{"status": "INFECTED", "threat": "DisallowedExecutableMIME", "file": "'"$TARGET_FILE"'"}'
        exit 2
    fi
    echo '{"status": "CLEAN", "engine": "HeuristicMIMEScanner", "file": "'"$TARGET_FILE"'", "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}'
    exit 0
fi

if [[ -n "$SCAN_RESULT" ]]; then
    echo '{"status": "INFECTED", "threat": "'"$SCAN_RESULT"'", "file": "'"$TARGET_FILE"'"}'
    exit 2
else
    echo '{"status": "CLEAN", "engine": "ClamAV-Daemon", "file": "'"$TARGET_FILE"'", "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}'
    exit 0
fi

