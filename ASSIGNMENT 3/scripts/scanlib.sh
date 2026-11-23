#!/usr/bin/env bash
# Reusable CSV functions for the Assignment 3 sample pipeline.
# Processes files only; it does not perform network scans.

set -uo pipefail
SCOPE_PREFIX="192.168.56."
OUTDIR="${OUTDIR:-out}"

valid_ip() {
  local ip="$1" a b c d
  [[ "$ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
  IFS=. read -r a b c d <<< "$ip"
  (( a <= 255 && b <= 255 && c <= 255 && d <= 255 )) || return 1
  [[ "$ip" == "$SCOPE_PREFIX"* ]]
}

import_check() {
  local f="${1:?CSV file required}"
  [[ -r "$f" ]] || { echo "cannot read $f" >&2; return 2; }
  [[ "$(head -n 1 "$f")" == "ip,port,protocol,state,service,version" ]] || {
    echo "header mismatch in $f" >&2; return 3;
  }
  awk -F, 'NR>1 && (NF!=6 || $2 !~ /^[0-9]+$/ || $3 !~ /^(tcp|udp)$/ || $4 !~ /^(open|closed|filtered|open\|filtered)$/) {bad=1} END{exit bad}' "$f" || {
    echo "invalid row in $f" >&2; return 4;
  }
}

norm_service() {
  local map="${1:-data/services.map}"
  awk -F, -v OFS=, 'NR==FNR {m[tolower($1)]=$2; next}
    FNR==1 {print; next}
    {k=tolower($5); gsub(/^[[:space:]]+|[[:space:]]+$/, "", k); if(k in m) $5=m[k]; print}' "$map" -
}

clean_ports() {
  local input="${1:?input CSV required}"
  local clean="${2:-$OUTDIR/ports_clean.csv}"
  local rejected="${3:-$OUTDIR/ports_rejected.csv}"
  [[ -r "$input" ]] || { echo "missing file: $input" >&2; return 2; }
  mkdir -p "$(dirname "$clean")" "$(dirname "$rejected")"
  local tmp
  tmp="$(mktemp)"
  awk -F, -v OFS=, -v scope="$SCOPE_PREFIX" -v rej="$tmp" '
    NR==1 {if($0!="ip,port,protocol,state,service,version"){print "header_mismatch" > rej; exit 3}; print; next}
    {
      reason=""
      if (NF!=6 || $1 !~ /^([0-9]{1,3}\.){3}[0-9]{1,3}$/) reason="malformed_ip"
      else {
        split($1,oct,"."); for(i=1;i<=4;i++) if(oct[i]>255) reason="malformed_ip"
        if(reason=="" && index($1,scope)!=1) reason="out_of_scope"
      }
      if(reason=="" && $2=="") reason="missing_port"
      if(reason=="" && ($2 !~ /^[0-9]+$/ || $2<1 || $2>65535)) reason="port_out_of_range"
      if(reason=="" && $3 !~ /^(tcp|udp)$/) reason="invalid_protocol"
      if(reason=="" && $4 !~ /^(open|closed|filtered|open\|filtered)$/) reason="invalid_state"
      key=$1 SUBSEP $2 SUBSEP $3
      if(reason=="" && seen[key]++) reason="duplicate"
      if(reason=="") print
      else print $0,reason >> rej
    }
    END {close(rej)}
  ' "$input" > "$clean"
  {
    echo "ip,port,protocol,state,service,version,reason"
    cat "$tmp"
  } > "$rejected"
  rm -f "$tmp"
}

melt() {
  local wide="${1:?wide CSV required}"
  awk -F, -v OFS=, 'NR==1 {for(i=2;i<=NF;i++){p=$i; sub(/^p/,"",p); port[i]=p} print "host,port,state"; next}
    {for(i=2;i<=NF;i++) print $1,port[i],$i}' "$wide"
}

cast_open_counts() {
  local longfile="${1:?long CSV required}"
  awk -F, -v OFS=, 'NR>1 && $3=="open" {count[$1]++}
    END {print "host,open_ports"; for(h in count) print h,count[h]}' "$longfile" | sort -t, -k1,1
}

export_result() {
  local source="${1:?source file required}" tag="${2:-scan}"
  local ts dest n=1
  ts="$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$OUTDIR"
  while :; do
    dest="$OUTDIR/${tag}_${ts}_v${n}.csv"
    [[ -e "$dest" ]] || break
    ((n++))
  done
  cp -- "$source" "$dest" || return 1
  (cd "$OUTDIR" && sha256sum "$(basename "$dest")" >> checksums.sha256)
  printf '%s\n' "$dest"
}
