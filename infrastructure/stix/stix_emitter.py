#!/usr/bin/env python3
"""
STIX 2.1 Security Incident and Threat Intelligence Serializer
Transforms UniChrist application security alerts (rate limit abuses, malicious uploads,
SQL injection probe attempts) into standardized STIX 2.1 Threat Observable Bundles.
"""

import json
import uuid
from datetime import datetime, timezone

def generate_stix_bundle(incident_type: str, indicator_pattern: str, description: str, severity: str = "medium"):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    identity_id = f"identity--{uuid.uuid4()}"
    indicator_id = f"indicator--{uuid.uuid4()}"
    observed_data_id = f"observed-data--{uuid.uuid4()}"
    bundle_id = f"bundle--{uuid.uuid4()}"

    stix_identity = {
        "type": "identity",
        "spec_version": "2.1",
        "id": identity_id,
        "created": now_iso,
        "modified": now_iso,
        "name": "UniChrist Automated SOC Sensor",
        "identity_class": "system",
        "sectors": ["education", "technology"]
    }

    stix_indicator = {
        "type": "indicator",
        "spec_version": "2.1",
        "id": indicator_id,
        "created": now_iso,
        "modified": now_iso,
        "name": f"UniChrist Alert: {incident_type}",
        "description": description,
        "indicator_types": ["malicious-activity", "anomalous-activity"],
        "pattern": indicator_pattern,
        "pattern_type": "stix",
        "valid_from": now_iso,
        "confidence": 95 if severity == "high" else 75
    }

    stix_observed_data = {
        "type": "observed-data",
        "spec_version": "2.1",
        "id": observed_data_id,
        "created": now_iso,
        "modified": now_iso,
        "first_observed": now_iso,
        "last_observed": now_iso,
        "number_observed": 1,
        "objects": {
            "0": {
                "type": "network-traffic",
                "protocols": ["ipv4", "tcp", "http"]
            }
        }
    }

    stix_bundle = {
        "type": "bundle",
        "id": bundle_id,
        "spec_version": "2.1",
        "objects": [stix_identity, stix_indicator, stix_observed_data]
    }

    return stix_bundle

if __name__ == "__main__":
    sample_bundle = generate_stix_bundle(
        incident_type="Grievance Attachment SQLi Payload Pattern",
        indicator_pattern="[file:name MATCHES '.*(select|union|concat).*\\\\.sql']",
        description="Detected anomalous malicious SQL query embedded in student attachment.",
        severity="high"
    )
    print(json.dumps(sample_bundle, indent=2))

