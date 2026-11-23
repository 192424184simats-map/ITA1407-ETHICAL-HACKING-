#!/usr/bin/env bash
# Safe HTTP response-header inspection for a local/authorized web application.
set -euo pipefail
TARGET="${1:-http://127.0.0.1/}"
case "$TARGET" in
  http://127.0.0.1/*|https://127.0.0.1/*|http://localhost/*|https://localhost/*) ;;
  *) echo "Refusing remote target. Use localhost only with this helper." >&2; exit 2 ;;
esac
command -v curl >/dev/null || { echo "curl is required" >&2; exit 3; }
headers="$(mktemp)"
trap 'rm -f "$headers"' EXIT
curl --silent --show-error --max-time 10 --head "$TARGET" > "$headers"
echo "Target: $TARGET"
echo
cat "$headers"
echo
for h in content-security-policy x-frame-options x-content-type-options strict-transport-security; do
  if grep -qi "^$h:" "$headers"; then
    printf '[PRESENT] %s\n' "$h"
  else
    printf '[MISSING] %s\n' "$h"
  fi
done
