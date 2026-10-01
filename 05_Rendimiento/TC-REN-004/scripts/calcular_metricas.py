"""TC-REN-004 - Cálculo de métricas a partir del JTL oficial de JMeter.

No realiza peticiones HTTP: solo lee el archivo de resultados (.jtl CSV) generado por JMeter.

Uso (desde TC-REN-004/):
    python scripts/calcular_metricas.py [resultados.jtl] [salida-metricas.json] [threads] [rampup] [loops]
Valores por defecto: el JTL oficial, evidencias/TC-REN-004-metricas.json y la configuración 10 / 0 / 1.
"""

import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

THRESHOLD_MS = 3000
LABEL = "TC-REN-004 - GET breweries"

root = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
jtl_path = (root / (args[0] if len(args) > 0 else "evidencias/TC-REN-004-results.jtl")).resolve()
out_path = (root / (args[1] if len(args) > 1 else "evidencias/TC-REN-004-metricas.json")).resolve()
threads = int(args[2]) if len(args) > 2 else 10
rampup = int(args[3]) if len(args) > 3 else 0
loops = int(args[4]) if len(args) > 4 else 1

with jtl_path.open(newline="", encoding="utf-8") as handle:
    rows = [row for row in csv.DictReader(handle) if row["label"] == LABEL]

samples = []
for row in rows:
    samples.append({
        "timeStamp": int(row["timeStamp"]),
        "elapsed": int(row["elapsed"]),
        "threadName": row["threadName"],
        "responseCode": row["responseCode"],
        "responseMessage": row["responseMessage"],
        "success": row["success"].strip().lower() == "true",
        "failureMessage": row.get("failureMessage", ""),
        "bytes": int(row["bytes"]),
        "sentBytes": int(row["sentBytes"]),
        "Latency": int(row["Latency"]),
        "Connect": int(row["Connect"]),
        "URL": row.get("URL", ""),
    })

total = len(samples)
elapsed = [s["elapsed"] for s in samples]
ordered = sorted(elapsed)

success_samples = sum(1 for s in samples if s["success"])
failed_samples = total - success_samples
http_200 = sum(1 for s in samples if s["responseCode"] == "200")
under = sum(1 for e in elapsed if e < THRESHOLD_MS)  # estrictamente menor

mean = sum(elapsed) / total if total else None
if total == 0:
    median = None
elif total % 2 == 0:
    median = (ordered[total // 2 - 1] + ordered[total // 2]) / 2
else:
    median = ordered[(total - 1) // 2]

# P95 nearest-rank: posición = ceil(0.95 × N), base 1
p95_rank = math.ceil(0.95 * total) if total else None
p95 = ordered[p95_rank - 1] if total else None

# Throughput observado (diagnóstico): muestras / ventana [primer inicio, último fin]
if total:
    window_start = min(s["timeStamp"] for s in samples)
    window_end = max(s["timeStamp"] + s["elapsed"] for s in samples)
    window_ms = window_end - window_start
    throughput = total / (window_ms / 1000) if window_ms > 0 else None
    start_offsets = sorted(s["timeStamp"] - window_start for s in samples)
    # Solapamiento: cuántas muestras seguían en curso cuando empezó la última
    last_start = max(s["timeStamp"] for s in samples)
    in_flight_at_last_start = sum(1 for s in samples if s["timeStamp"] <= last_start < s["timeStamp"] + s["elapsed"])
else:
    window_start = window_end = window_ms = throughput = None
    start_offsets = []
    in_flight_at_last_start = 0

metrics = {
    "case_id": "TC-REN-004",
    "source_jtl": jtl_path.relative_to(root).as_posix(),
    "configuration": {
        "threads": threads,
        "ramp_up_seconds": rampup,
        "loops": loops,
        "expected_samples": threads * loops,
    },
    "observed": {
        "total_samples": total,
        "success_samples": success_samples,
        "failed_samples": failed_samples,
        "http_200_count": http_200,
        "non_200_count": total - http_200,
        "distinct_threads": len({s["threadName"] for s in samples}),
        "urls": sorted({s["URL"] for s in samples}),
    },
    "latency_ms": {
        "threshold_ms": THRESHOLD_MS,
        "comparison": "elapsed < 3000 (estricto)",
        "under_3000_count": under,
        "at_or_over_3000_count": total - under,
        "under_3000_percent": (under / total) * 100 if total else None,
        "min": ordered[0] if total else None,
        "max": ordered[-1] if total else None,
        "mean": mean,
        "median": median,
        "p95": p95,
        "p95_method": "nearest-rank",
        "p95_rank": p95_rank,
    },
    "errors": {
        "error_rate_percent": (failed_samples / total) * 100 if total else None,
        "response_codes": dict(Counter(s["responseCode"] for s in samples)),
        "failed": [s for s in samples if not s["success"] or s["responseCode"] != "200"],
    },
    "throughput_observed_req_per_sec": throughput,
    "throughput_method": "total_samples / (max(timeStamp+elapsed) - min(timeStamp)) en segundos; diagnóstico",
    "concurrency": {
        "window_start_epoch_ms": window_start,
        "window_end_epoch_ms": window_end,
        "window_ms": window_ms,
        "start_offsets_ms": start_offsets,
        "start_spread_ms": (start_offsets[-1] - start_offsets[0]) if start_offsets else None,
        "samples_in_flight_when_last_started": in_flight_at_last_start,
    },
    "samples": sorted(samples, key=lambda s: (s["timeStamp"], s["threadName"])),
}

out_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(metrics, indent=2, ensure_ascii=False))
