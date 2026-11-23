#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
source scripts/scanlib.sh
mkdir -p out

clean_ports data/ports_raw.csv out/ports_clean.csv out/ports_rejected.csv
awk -F, 'NR>1 && $4=="open"{n[$1]++} END{print "host,open_ports"; for(h in n)print h,n[h]}' out/ports_clean.csv | sort -t, -k1,1 > out/open_ports_by_host.csv
melt data/wide_scan.csv > out/scan_long.csv
cast_open_counts out/scan_long.csv > out/wide_open_summary.csv
export_result out/ports_clean.csv ports_clean >/dev/null
echo "Pipeline completed. Results are in $ROOT/out/"
echo "Input rows: $(( $(wc -l < data/ports_raw.csv) - 1 ))"
echo "Clean rows: $(( $(wc -l < out/ports_clean.csv) - 1 ))"
echo "Rejected rows: $(( $(wc -l < out/ports_rejected.csv) - 1 ))"
