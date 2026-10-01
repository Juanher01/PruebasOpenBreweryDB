# Informe de Ejecución — TC-REN-005

## 1. Identificación

```text
Caso: TC-REN-005
Nombre: Throughput
Tipo: Rendimiento — carga sostenida
API: Open BreweryDB
Endpoint: GET /v1/breweries
Herramienta: Apache JMeter 5.6.3 (modo no-GUI)
Fecha/hora: 2026-10-01T16:01:57.123Z → 16:02:57.135Z (UTC) — 2026-10-01 11:01–11:02 hora local (COT, UTC-5)
```

> **Nota de versión del caso.** Este informe corresponde al **paquete de instrucciones actualizado** de TC-REN-005, que define un umbral de aceptación: línea base 110.198 req/s, tolerancia máxima de degradación del 10 % y mínimo de 99.18 req/s. Esa línea base es el throughput medido en la ejecución anterior de este caso (2026-10-01 07:33 UTC, versión sin umbral). Sus artefactos ya no estaban en la carpeta al iniciar esta ejecución, pero se conservan en el historial de git (commit `0b9d9b2 Pruebas de rendimiento`). Esta ejecución es una campaña nueva y completa: **no reutiliza ningún dato de la anterior**.

---

## 2. Objetivo

Verificar la capacidad de procesamiento sostenido de `GET /v1/breweries` con **10 hilos concurrentes durante 60 segundos** (loop continuo, sin think time ni limitación artificial). Se comprueba que el throughput alcanzado sea ≥ 99.18 req/s, que el 100 % de las respuestas sean HTTP 200 y que no aparezca ninguna respuesta HTTP 429.

---

## 3. Criterios

```text
Threads: 10
Duración: 60 s
Baseline: 110.198 req/s
Tolerancia máxima: 10%
Throughput mínimo: 99.18 req/s   (110.198 × 0.90 = 99.1782 → 99.18; operador >=)
HTTP 200: 100%
HTTP 429: 0%
```

La latencia no es criterio de este caso: no se usa el 95 % < 3000 ms de TC-REN-004.

---

## 4. Ambiente

```text
JMeter version: 5.6.3 (jmeter -v; log "Version 5.6.3"). Instalación en C:\tools\apache-jmeter-5.6.3 (binario oficial verificado por SHA-512, instalado con autorización en TC-REN-004)
Java version: 22 (Java HotSpot(TM) 64-Bit Server VM, build 22+36-2370)
Sistema operativo: Windows 11 (build 10.0.26200, amd64)
Fecha/hora: 2026-10-01T16:01:57Z (UTC)
Threads: 10
Duration: 60 s
Endpoint: https://api.openbrewerydb.org/v1/breweries
Ubicación del runner: equipo local del analista; no verificada (zona horaria COT, UTC-5)
Tipo de conexión: no verificado
```

La medición es **end-to-end desde el runner**: incluye red, DNS, TLS e infraestructura del proveedor.

---

## 5. Configuración JMeter

Archivo: `jmeter/TC-REN-005.jmx`

```text
Test Plan: TC-REN-005 - Throughput
└── Thread Group: TC-REN-005 - Thread Group
    ├── HTTP Request Defaults
    └── HTTP Request: TC-REN-005 - GET breweries
(sin assertions, timers ni listeners; el Dashboard se genera desde el .jtl)
```

```text
Threads: ${__P(threads,10)} → 10
Ramp-Up: ${__P(rampup,0)} → 0 s
Loop: continuo (LoopController.loops = -1)
Scheduler: habilitado
Duration: ${__P(duration,60)} → 60 s
Think Time: ninguno (sin Constant / Uniform Random Timer)
Throughput Timer: ninguno (sin Constant Throughput Timer ni Throughput Shaping Timer)
Synchronizing Timer: no (carga continua)
Protocol: https
Host: api.openbrewerydb.org
Port: estándar HTTPS
Method: GET
Path: /v1/breweries (sin query params, body ni autenticación)
Timeouts técnicos: connect 30000 ms / response 60000 ms (salvaguardas; no son criterio)
On sample error: continue (un 429 u otro error no detiene la campaña)
```

---

## 6. Preflight

Con la misma plantilla y `-Jthreads=1 -Jrampup=0 -Jduration=5` (inicio de comando 16:01:39Z UTC):

```text
Muestras: 41 (1 hilo, 5 s)
Códigos: 200 × 41
URL: https://api.openbrewerydb.org/v1/breweries
Errores: 0
```

Confirmó que JMeter funciona, DNS/TLS, el endpoint, la generación del JTL y la captura de códigos HTTP. **Excluido** de la ventana oficial, del throughput y de los porcentajes. Evidencia: `evidencias/preflight-results.jtl`, `preflight-jmeter.log` y `preflight-console.txt`.

---

## 7. Procedimiento

1. **Validación del JMX** — Parseado como XML válido (`jmeterTestPlan`). Elementos: TestPlan, ThreadGroup (LoopController −1, scheduler), HTTP Request Defaults y HTTPSamplerProxy. Se confirmó la ausencia de timers, throughput timers y listeners. `scripts/calcular_metricas.py` compiló sin errores.
2. **Preflight** — 1 hilo, 5 s (sección 6).
3. **Run oficial** — Se comprobó antes que no existían ni `dashboard/` ni el JTL oficial. Comando (inicio 16:01:55Z UTC; fin del proceso, incluida la generación del Dashboard, 16:03:00Z), exit code `0`:
   ```bash
   jmeter -n \
     -t jmeter/TC-REN-005.jmx \
     -Jthreads=10 \
     -Jrampup=0 \
     -Jduration=60 \
     -l evidencias/TC-REN-005-results.jtl \
     -j evidencias/TC-REN-005-jmeter.log \
     -e \
     -o dashboard/TC-REN-005 \
     > evidencias/TC-REN-005-console.txt 2>&1
   ```
   (ejecutado como `C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat` con rutas Windows)
4. **Generación del JTL** — CSV con `timeStamp, elapsed, label, responseCode, responseMessage, threadName, dataType, success, failureMessage, bytes, sentBytes, grpThreads, allThreads, URL, Latency, IdleTime, Connect`; 6200 filas. No se editó.
5. **Dashboard** — `dashboard/TC-REN-005/` (`index.html`, `statistics.json` y las páginas `OverTime.html`, `Throughput.html`, `ResponseTimes.html` y `CustomsGraphs.html`, con Response Time Over Time, Active Threads Over Time, Transactions per Second y Response Codes per Second).
6. **Cálculo de throughput** — `python scripts/calcular_metricas.py` (sin HTTP) leyó el JTL y `statistics.json` y escribió `evidencias/TC-REN-005-metricas.json`. Se verificó con un recálculo independiente sobre el JTL.
7. **Cálculo de porcentajes HTTP** — 6200/6200 HTTP 200; 0 HTTP 429; 0 otros; 0 errores de transporte.
8. **Comparación contra el umbral** — 103.3127 ≥ 99.18 → cumple. Margen +4.1327 req/s; degradación 6.2481 % (< 10 %).
9. **Determinación del estado** — APROBADO (sección 14). No se requirió repetición.

---

## 8. Volumen

| Métrica | Resultado |
|---|---:|
| Threads | 10 (10 hilos distintos en el JTL) |
| Duración configurada | 60 s |
| Ventana observada | 60.012 s |
| Total samples | 6200 |
| HTTP 200 | 6200 |
| HTTP 429 | 0 |
| Otros HTTP | 0 |
| Errores de red | 0 |

**Ventana observada:** desde el primer inicio de muestra (`timeStamp` 1790870517123 = 16:01:57.123Z) hasta el máximo de `timeStamp + elapsed` (1790870577135 = 16:02:57.135Z). La duración total del proceso (~65 s) incluye el arranque de JMeter y la generación del Dashboard, y no se usa para el throughput. Cada hilo ejecutó entre 593 y 652 muestras.

---

## 9. Throughput

| Métrica | Resultado |
|---|---:|
| Baseline | 110.198 req/s |
| Mínimo aceptable | 99.18 req/s |
| Throughput JMeter | 103.3127 req/s (103.3126707991735) |
| Throughput derivado | 103.3127 req/s (6200 / 60.012 s) |
| Throughput HTTP 200 | 103.3127 req/s (6200 / 60.012 s) |
| Margen sobre mínimo | +4.1327 req/s |
| Degradación vs baseline | 6.25 % (6.2481 %) |

- **JMeter** reporta el throughput en req/s (`statistics.json` → `throughput` de *TC-REN-005 - GET breweries*); no hubo conversión de unidades. Es el valor usado para el criterio.
- El **throughput derivado** coincide exactamente con el de JMeter, porque ambos usan la misma ventana (primer inicio → último fin).
- El **throughput HTTP 200** es igual al total, porque el 100 % fueron 200.
- Por segundos (contados por el `timeStamp` de inicio): 60 segundos con muestras, entre 60 req (primer segundo, apertura de conexiones) y 108 req. Resúmenes de la consola: 81.3/s en los primeros 3 s, después 104.2/s y 104.3/s; total 103.1/s.
- **Margen** = 103.3127 − 99.18 = +4.1327 req/s. **Degradación** = (110.198 − 103.3127) / 110.198 × 100 = 6.2481 %, dentro de la tolerancia del 10 %.

---

## 10. Evaluación de criterios

| Criterio | Esperado | Obtenido | Estado |
|---|---:|---:|---|
| Threads | 10 | 10 | PASS |
| Duración | 60 s | 60 s configurados (ventana observada 60.012 s) | PASS |
| Throughput | >=99.18 req/s | 103.3127 req/s | PASS |
| HTTP 200 | 100 % | 100 % (6200/6200) | PASS |
| HTTP 429 | 0 % | 0 % (0/6200) | PASS |

---

## 11. Distribución HTTP

| Código / tipo | Cantidad | Porcentaje |
|---|---:|---:|
| 200 | 6200 | 100 % |
| 429 | 0 | 0 % |
| Otros (4xx distintos de 429, 5xx, errores de red/transporte) | 0 | 0 % |

---

## 12. Latencia descriptiva

| Métrica | Resultado |
|---|---:|
| Min | 85 ms |
| Max | 592 ms |
| Average | 96.58 ms |
| Median | 95 ms |
| P90 | 101 ms |
| P95 | 104 ms |
| P99 | 115 ms |

Estas métricas son descriptivas en TC-REN-005. Percentiles por **nearest-rank** (⌈p/100 × N⌉, N = 6200), idénticos a los del Dashboard de JMeter (pct1/pct2/pct3 = 101 / 104 / 115).

---

## 13. Rate limiting

```text
¿Se observaron HTTP 429?: No
Cantidad: 0
Porcentaje: 0%
Primera aparición: no aplica
Comportamiento: no aplica
```

No se observaron respuestas HTTP 429.

---

## 14. Resultado final

```text
Estado: APROBADO

Justificación:
JMeter ejecutó en modo no-GUI la campaña oficial con 10 hilos, ramp-up 0 s, loop
continuo y 60 s configurados (ventana observada de 60.012 s) contra
GET https://api.openbrewerydb.org/v1/breweries, sin think time ni throughput
artificial. Se procesaron 6200 solicitudes con un throughput de 103.3127 req/s
según JMeter, coincidente con el cálculo independiente: mayor o igual al mínimo de
99.18 req/s (margen +4.13 req/s; degradación 6.25 % frente a la línea base de
110.198 req/s, dentro de la tolerancia del 10 %). El 100 % de las respuestas
fueron HTTP 200 y no hubo ningún HTTP 429, otro código ni error de red. No hubo
fallos técnicos que invalidaran la medición.
```

---

## 15. Hallazgos

No se identificaron incumplimientos de los criterios definidos para TC-REN-005.

> Observación (no es hallazgo): el throughput de esta campaña (103.31 req/s) es un 6.25 % inferior a la línea base de 110.198 req/s, medida desde el mismo runner unas 8.5 horas antes. La diferencia está dentro de la tolerancia definida. Como ambas mediciones son end-to-end desde un único equipo, parte de la variación puede deberse a la red del cliente y no solo al servicio. La latencia media pasó de 90.57 ms a 96.58 ms, coherente con un throughput algo menor a concurrencia fija.

---

## 16. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-005
Resultado obtenido: Se ejecutó una carga sostenida con 10 hilos concurrentes durante 60 segundos contra GET /v1/breweries. Se procesaron 6200 solicitudes. El throughput fue de 103.31 req/s frente al mínimo aceptable de 99.18 req/s, con una degradación de 6.25% respecto a la línea base de 110.198 req/s. HTTP 200: 6200 (100%). HTTP 429: 0 (0%). Resultado: CUMPLE.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-005-results.jtl (complementos: TC-REN-005-metricas.json, dashboard/TC-REN-005/index.html, TC-REN-005-jmeter.log, TC-REN-005-console.txt, jmeter/TC-REN-005.jmx)
Observaciones: Paquete actualizado con umbral >= 99.18 req/s. Apache JMeter 5.6.3 no-GUI (Java 22, Windows 11), 10 hilos, ramp-up 0 s, loop continuo, 60 s (ventana observada 60.012 s), sin think time ni throughput timer. Throughput JMeter = derivado = 103.3127 req/s; margen +4.13 req/s. Latencia descriptiva: media 96.58 ms, P95 104 ms, máx 592 ms. Preflight de 1 hilo/5 s (41 muestras) excluido. Ejecución el 2026-10-01 16:01 UTC. La ejecución previa que fijó la línea base se conserva en git (commit 0b9d9b2).
```
