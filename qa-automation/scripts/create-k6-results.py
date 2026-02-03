#!/usr/bin/env python3
"""
Create k6 results.json for dashboard display
Use this if k6 tests ran but results.json wasn't captured properly
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Default values - update with actual k6 test results
TOTAL_REQUESTS = 0
FAILED_RATE = 0.0  # As percentage (0.0 = 0%)
AVG_RESPONSE_TIME = 0.0  # milliseconds
P95_RESPONSE_TIME = 0.0  # milliseconds
P99_RESPONSE_TIME = 0.0  # milliseconds

# Allow override from command line
if len(sys.argv) > 1:
    try:
        TOTAL_REQUESTS = int(sys.argv[1])
        if len(sys.argv) > 2:
            FAILED_RATE = float(sys.argv[2])
        if len(sys.argv) > 3:
            AVG_RESPONSE_TIME = float(sys.argv[3])
        if len(sys.argv) > 4:
            P95_RESPONSE_TIME = float(sys.argv[4])
        if len(sys.argv) > 5:
            P99_RESPONSE_TIME = float(sys.argv[5])
    except ValueError:
        print("Usage: python create-k6-results.py [total_requests] [failed_rate%] [avg_ms] [p95_ms] [p99_ms]")
        sys.exit(1)

# Create k6 results.json in k6 format
results = {
    "metrics": {
        "http_reqs": {
            "values": {
                "count": TOTAL_REQUESTS
            }
        },
        "http_req_duration": {
            "values": {
                "avg": AVG_RESPONSE_TIME,
                "p(95)": P95_RESPONSE_TIME,
                "p(99)": P99_RESPONSE_TIME
            }
        },
        "http_req_failed": {
            "values": {
                "rate": FAILED_RATE / 100.0  # Convert percentage to rate
            }
        }
    },
    "root_group": {},
    "state": {
        "testRunDurationMs": 0
    }
}

# Ensure reports directory exists
reports_dir = Path(__file__).parent.parent / "reports"
reports_dir.mkdir(exist_ok=True)

output_file = reports_dir / "k6-results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"✅ Created {output_file}")
print(f"   Total Requests: {TOTAL_REQUESTS}")
print(f"   Failed Rate: {FAILED_RATE}%")
print(f"   Avg Response Time: {AVG_RESPONSE_TIME}ms")
print(f"   P95 Response Time: {P95_RESPONSE_TIME}ms")
print(f"   P99 Response Time: {P99_RESPONSE_TIME}ms")
