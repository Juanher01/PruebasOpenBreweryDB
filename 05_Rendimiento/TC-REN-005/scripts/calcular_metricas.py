"""TC-REN-005 - Métricas de throughput y evaluación de aceptación a partir del JTL oficial.

No realiza peticiones HTTP: solo lee el JTL (CSV) generado por JMeter y, si existe,
dashboard/TC-REN-005/statistics.json para el throughput reportado por JMeter.

Criterios (paquete actualizado):
    throughput >= 99.18 req/s  (baseline 110.198 req/s, tolerancia máxima 10%)
    HTTP 200 = 100%
    HTTP 429 = 0%

Uso (desde TC-REN-005/):
    python scripts/calcular_metricas.py [resultados.jtl] [salida-metricas.json] [statistics.json|-]
"""

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

LABEL = "TC-REN-005 - GET breweries"
THREADS = 10
RAMPUP = 0
DURATION = 60
BASELINE_RPS = 110.198
MAX_DEGRADATION_PERCENT = 10
MIN_THROUGHPUT_RPS = 99.18  # 110.198 × 0.90 = 99.1782 → 99.18 según el Plan

root = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
jtl_path = (root / (args[0] if len(args) > 0 else "evidencias/TC-REN-005-results.jtl")).resolve()
out_path = (root / (args[1] if len(args) > 1 else "evidencias/TC-REN-005-metricas.json")).resolve()
stats_arg = args[2] if len(args) > 2 else "dashboard/TC-REN-005/statistics.json"
stats_path = None if stats_arg == "-" else (root / stats_arg).resolve()

with jtl_path.open(newline="", encoding="utf-8") as handle:
    rows = [row for row in csv.DictReader(handle) if row["label"] == LABEL]

samples = [{
    "timeStamp": int(r["timeStamp"]),
    "elapsed": int(r["elapsed"]),
    "responseCode": r["responseCode"],
    "responseMessage": r["responseMessage"],
    "threadName": r["threadName"],
    "success": r["success"].strip().lower() == "true",
    "URL": r.get("URL", ""),
} for r in rows]


def classify(code):
    if code == "200":
        return "http_200"
    if code == "429":
        return "http_429"
    if code.isdigit() and code.startswith("5"):
        return "http_5xx"
    if code.isdigit():
        return "other_http_4xx_or_other"
    return "network_or_transport"  # "Non HTTP response code: ..."


def nearest_rank(ordered, pct):
    return ordered[max(math.ceil(pct / 100 * len(ordered)), 1) - 1]


total = len(samples)
classes = Counter(classify(s["responseCode"]) for s in samples)
http_200 = classes["http_200"]
http_429 = classes["http_429"]
other_http = classes["http_5xx"] + classes["other_http_4xx_or_other"]
network = classes["network_or_transport"]

window_start = min(s["timeStamp"] for s in samples)
window_end = max(s["timeStamp"] + s["elapsed"] for s in samples)
window_seconds = (window_end - window_start) / 1000

ordered = sorted(s["elapsed"] for s in samples)
median = (ordered[total // 2 - 1] + ordered[total // 2]) / 2 if total % 2 == 0 else ordered[(total - 1) // 2]

jmeter_throughput = None
dashboard_stats = None
if stats_path and stats_path.exists():
    dashboard_stats = json.loads(stats_path.read_text(encoding="utf-8")).get(LABEL)
    if dashboard_stats:
        jmeter_throughput = dashboard_stats.get("throughput")

derived = total / window_seconds
official_throughput = jmeter_throughput if jmeter_throughput is not None else derived

per_second = defaultdict(Counter)
for s in samples:
    per_second[(s["timeStamp"] - window_start) // 1000][s["responseCode"]] += 1

samples_429 = sorted((s for s in samples if s["responseCode"] == "429"), key=lambda s: s["timeStamp"])
first_429 = None
if samples_429:
    first_429 = {
        "timeStamp": samples_429[0]["timeStamp"],
        "offset_seconds_from_start": (samples_429[0]["timeStamp"] - window_start) / 1000,
        "threadName": samples_429[0]["threadName"],
    }

throughput_pass = official_throughput >= MIN_THROUGHPUT_RPS
http_200_pass = total > 0 and http_200 == total
http_429_pass = http_429 == 0

metrics = {
    "case_id": "TC-REN-005",
    "source_jtl": jtl_path.relative_to(root).as_posix(),
    "configuration": {
        "threads": THREADS,
        "ramp_up_seconds": RAMPUP,
        "duration_seconds": DURATION,
        "loop": "continuo (LoopController.loops = -1, scheduler)",
        "endpoint": "GET /v1/breweries",
    },
    "baseline": {
        "throughput_req_per_sec": BASELINE_RPS,
        "maximum_degradation_percent": MAX_DEGRADATION_PERCENT,
        "minimum_acceptable_throughput_req_per_sec": MIN_THROUGHPUT_RPS,
        "minimum_exact": BASELINE_RPS * (1 - MAX_DEGRADATION_PERCENT / 100),
    },
    "samples": {
        "total": total,
        "http_200": http_200,
        "http_429": http_429,
        "other_http": other_http,
        "other_http_breakdown": {
            "http_5xx": classes["http_5xx"],
            "other_4xx_or_other": classes["other_http_4xx_or_other"],
        },
        "network_or_transport_errors": network,
        "distinct_threads": len({s["threadName"] for s in samples}),
        "urls": sorted({s["URL"] for s in samples}),
    },
    "rates_percent": {
        "http_200": http_200 / total * 100,
        "http_429": http_429 / total * 100,
        "other_errors": (other_http + network) / total * 100,
    },
    "test_window": {
        "method": "inicio = min(timeStamp); fin = max(timeStamp + elapsed); ventana = fin - inicio",
        "start_epoch_ms": window_start,
        "end_epoch_ms": window_end,
    },
    "test_window_seconds": window_seconds,
    "throughput_req_per_sec": {
        "jmeter_reported": jmeter_throughput,
        "derived_total": derived,
        "successful_http_200": http_200 / window_seconds,
        "official_value_used_for_acceptance": official_throughput,
        "margin_over_minimum": official_throughput - MIN_THROUGHPUT_RPS,
        "degradation_vs_baseline_percent": (BASELINE_RPS - official_throughput) / BASELINE_RPS * 100,
    },
    "latency_ms": {
        "min": ordered[0],
        "max": ordered[-1],
        "mean": sum(ordered) / total,
        "median": median,
        "p90": nearest_rank(ordered, 90),
        "p95": nearest_rank(ordered, 95),
        "p99": nearest_rank(ordered, 99),
        "percentile_method": "nearest-rank (posición = ceil(p/100 × N))",
        "note": "descriptivas; no son criterio de TC-REN-005",
    },
    "rate_limiting": {
        "http_429_present": http_429 > 0,
        "count": http_429,
        "percent": http_429 / total * 100,
        "first_occurrence": first_429,
    },
    "acceptance": {
        "throughput_pass": throughput_pass,
        "http_200_pass": http_200_pass,
        "http_429_pass": http_429_pass,
        "overall_pass": throughput_pass and http_200_pass and http_429_pass,
    },
    "response_codes": dict(Counter(s["responseCode"] for s in samples)),
    "per_second_distribution": [
        {"second": sec, "total": sum(c.values()), "codes": dict(c)} for sec, c in sorted(per_second.items())
    ],
    "jmeter_dashboard_statistics": dashboard_stats,
}

out_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
summary = {k: v for k, v in metrics.items() if k not in ("per_second_distribution", "jmeter_dashboard_statistics")}
print(json.dumps(summary, indent=2, ensure_ascii=False))
