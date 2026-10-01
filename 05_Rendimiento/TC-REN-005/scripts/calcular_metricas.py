"""TC-REN-005 - Cálculo de métricas de throughput a partir del JTL oficial de JMeter.

No realiza peticiones HTTP: solo lee el archivo de resultados (.jtl CSV) generado por JMeter.

Uso (desde TC-REN-005/):
    python scripts/calcular_metricas.py [resultados.jtl] [salida-metricas.json] [threads] [rampup] [duration]
Valores por defecto: el JTL oficial, evidencias/TC-REN-005-metricas.json y la configuración 10 / 0 / 60.
"""

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

LABEL = "TC-REN-005 - GET breweries"

root = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
jtl_path = (root / (args[0] if len(args) > 0 else "evidencias/TC-REN-005-results.jtl")).resolve()
out_path = (root / (args[1] if len(args) > 1 else "evidencias/TC-REN-005-metricas.json")).resolve()
threads = int(args[2]) if len(args) > 2 else 10
rampup = int(args[3]) if len(args) > 3 else 0
duration = int(args[4]) if len(args) > 4 else 60

with jtl_path.open(newline="", encoding="utf-8") as handle:
    rows = [row for row in csv.DictReader(handle) if row["label"] == LABEL]

samples = [{
    "timeStamp": int(r["timeStamp"]),
    "elapsed": int(r["elapsed"]),
    "responseCode": r["responseCode"],
    "responseMessage": r["responseMessage"],
    "threadName": r["threadName"],
    "success": r["success"].strip().lower() == "true",
    "failureMessage": r.get("failureMessage", ""),
    "URL": r.get("URL", ""),
} for r in rows]


def classify(sample):
    code = sample["responseCode"]
    if code == "200":
        return "http_200"
    if code == "429":
        return "http_429"
    if code.isdigit():
        return "other_http"
    # Códigos no numéricos ("Non HTTP response code: ...") = errores de red/transporte
    return "network_or_transport"


def nearest_rank(ordered, pct):
    rank = math.ceil(pct / 100 * len(ordered))
    return ordered[max(rank, 1) - 1]


total = len(samples)
classes = Counter(classify(s) for s in samples)
http_200 = classes["http_200"]
http_429 = classes["http_429"]
other_http = classes["other_http"]
network = classes["network_or_transport"]

# Ventana de prueba: inicio de la primera muestra → max(timeStamp + elapsed)
window_start = min(s["timeStamp"] for s in samples)
window_end = max(s["timeStamp"] + s["elapsed"] for s in samples)
window_seconds = (window_end - window_start) / 1000

ordered = sorted(s["elapsed"] for s in samples)
mean = sum(ordered) / total
median = (ordered[total // 2 - 1] + ordered[total // 2]) / 2 if total % 2 == 0 else ordered[(total - 1) // 2]

# Distribución por segundo (desde el inicio de la ventana) de códigos, según timeStamp de inicio
per_second = defaultdict(Counter)
for s in samples:
    per_second[(s["timeStamp"] - window_start) // 1000][s["responseCode"]] += 1
per_second_list = [
    {"second": sec, "total": sum(c.values()), "codes": dict(c)}
    for sec, c in sorted(per_second.items())
]

samples_429 = sorted((s for s in samples if s["responseCode"] == "429"), key=lambda s: s["timeStamp"])
first_429 = None
if samples_429:
    s0 = samples_429[0]
    first_429 = {
        "timeStamp": s0["timeStamp"],
        "offset_seconds_from_start": (s0["timeStamp"] - window_start) / 1000,
        "threadName": s0["threadName"],
        "sample_index_by_start_time": sorted(samples, key=lambda s: s["timeStamp"]).index(s0) + 1,
    }

network_types = Counter(s["responseCode"] for s in samples if classify(s) == "network_or_transport")
other_http_types = Counter(s["responseCode"] for s in samples if classify(s) == "other_http")

metrics = {
    "case_id": "TC-REN-005",
    "source_jtl": jtl_path.relative_to(root).as_posix(),
    "configuration": {
        "threads": threads,
        "ramp_up_seconds": rampup,
        "duration_seconds": duration,
        "loop": "continuo (Loop Count = -1, scheduler)",
        "endpoint": "GET /v1/breweries",
    },
    "samples": {
        "total": total,
        "http_200": http_200,
        "http_429": http_429,
        "other_http": other_http,
        "network_or_transport_errors": network,
        "jmeter_success_true": sum(1 for s in samples if s["success"]),
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
        "jmeter_reported": None,  # se completa desde dashboard/TC-REN-005/statistics.json si existe
        "derived_total": total / window_seconds,
        "successful_http_200": http_200 / window_seconds,
    },
    "latency_ms": {
        "min": ordered[0],
        "max": ordered[-1],
        "mean": mean,
        "median": median,
        "p90": nearest_rank(ordered, 90),
        "p95": nearest_rank(ordered, 95),
        "p99": nearest_rank(ordered, 99),
        "percentile_method": "nearest-rank (posición = ceil(p/100 × N))",
    },
    "response_codes": dict(Counter(s["responseCode"] for s in samples)),
    "rate_limiting": {
        "http_429_present": http_429 > 0,
        "count": http_429,
        "percent": http_429 / total * 100,
        "first_occurrence": first_429,
        "seconds_with_429": sorted({e["second"] for e in per_second_list if "429" in e["codes"]}),
    },
    "other_http_by_code": dict(other_http_types),
    "network_or_transport_by_type": dict(network_types),
    "per_second_distribution": per_second_list,
}

# Throughput reportado por JMeter (Dashboard) para la etiqueta, si el Dashboard existe
stats_path = root / "dashboard" / "TC-REN-005" / "statistics.json"
if stats_path.exists() and jtl_path.name == "TC-REN-005-results.jtl":
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    label_stats = stats.get(LABEL, {})
    metrics["throughput_req_per_sec"]["jmeter_reported"] = label_stats.get("throughput")
    metrics["jmeter_dashboard_statistics"] = label_stats

out_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
summary = {k: v for k, v in metrics.items() if k not in ("per_second_distribution", "jmeter_dashboard_statistics")}
print(json.dumps(summary, indent=2, ensure_ascii=False))
