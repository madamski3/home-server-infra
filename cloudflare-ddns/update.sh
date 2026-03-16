#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

# Get current public IPv4
CURRENT_IP=$(curl -s -4 ifconfig.me)

if [[ -z "$CURRENT_IP" ]]; then
  echo "$(date): ERROR - Could not determine public IP" >&2
  exit 1
fi

# Get the current IP in the DNS record
RECORD=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records?type=A&name=${CF_RECORD_NAME}" \
  -H "Authorization: Bearer ${CF_API_TOKEN}")

RECORD_IP=$(echo "$RECORD" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['content'] if r else '')")
RECORD_ID=$(echo "$RECORD" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['id'] if r else '')")

if [[ "$CURRENT_IP" == "$RECORD_IP" ]]; then
  echo "$(date): IP unchanged (${CURRENT_IP}), no update needed"
  exit 0
fi

# Update the record
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records/${RECORD_ID}" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data "{\"content\":\"${CURRENT_IP}\"}" > /dev/null

echo "$(date): Updated ${CF_RECORD_NAME} from ${RECORD_IP} to ${CURRENT_IP}"
