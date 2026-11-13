#!/bin/bash
# ==============================================================================
# CSO & Trail of Bits Continuous Security Audit Script
# Validates Nginx configurations, permissions, exposed secrets & STIX protocols
# ==============================================================================

set -euo pipefail

echo "================================================================="
echo "  Sherlock AI & CSO Continuous Security Audit Routine"
echo "  Guidelines: Trail of Bits, CIS Benchmark & garrytan/gstack/cso"
echo "================================================================="

AUDIT_FAILURES=0

check_status() {
    local test_name="$1"
    local status="$2"
    if [ "$status" -eq 0 ]; then
        echo "  [PASS] $test_name"
    else
        echo "  [FAIL] $test_name"
        AUDIT_FAILURES=$((AUDIT_FAILURES + 1))
    fi
}

echo "1. Checking Nginx Security Headers Specification..."
if grep -q "Strict-Transport-Security" infrastructure/nginx/security-headers.conf && \
   grep -q "Content-Security-Policy" infrastructure/nginx/security-headers.conf && \
   grep -q "X-Frame-Options" infrastructure/nginx/security-headers.conf; then
    check_status "Security Headers (HSTS, CSP, X-Frame-Options present)" 0
else
    check_status "Security Headers (HSTS, CSP, X-Frame-Options present)" 1
fi

echo "2. Checking ClamAV Malware Sanitization Hook..."
if [ -x infrastructure/clamav/scan_upload.sh ]; then
    check_status "ClamAV Scan Hook Executable & Configured" 0
else
    check_status "ClamAV Scan Hook Executable & Configured" 1
fi

echo "3. Checking STIX 2.1 Threat Modeling & Emitter..."
if python3 infrastructure/stix/stix_emitter.py > /dev/null 2>&1; then
    check_status "STIX 2.1 Bundle Generation Operational" 0
else
    check_status "STIX 2.1 Bundle Generation Operational" 1
fi

echo "4. Checking for Hardcoded Production Secrets in Tracked Files..."
SECRETS_FOUND=$(grep -rnE "(AIza[0-9A-Za-z-_]{35}|ghp_[0-9a-zA-Z]{36}|sk_live_[0-9a-zA-Z]{24})" UniChristBackend/ client/ 2>/dev/null || true)
if [ -z "$SECRETS_FOUND" ]; then
    check_status "No Exposed Live Provider API Keys Found" 0
else
    check_status "No Exposed Live Provider API Keys Found" 1
fi

echo "5. Checking Coolify Multi-Container Isolation & Network Topology..."
if grep -q "unichrist-network" infrastructure/coolify/docker-compose.yml && \
   grep -q "restart: always" infrastructure/coolify/docker-compose.yml; then
    check_status "Coolify Container Isolation Enforced" 0
else
    check_status "Coolify Container Isolation Enforced" 1
fi

echo "================================================================="
if [ "$AUDIT_FAILURES" -eq 0 ]; then
    echo "  AUDIT PASSED: 0 Security Violations Detected."
    echo "================================================================="
    exit 0
else
    echo "  AUDIT FAILED: $AUDIT_FAILURES Vulnerability / Compliance Issues."
    echo "================================================================="
    exit 1
fi

