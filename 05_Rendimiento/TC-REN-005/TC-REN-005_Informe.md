# Informe de Ejecución — TC-REN-005

## 1. Identificación

```text
Caso: TC-REN-005
Nombre: Throughput
Tipo: Rendimiento — Carga sostenida
API: Open BreweryDB
Endpoint: GET /v1/breweries
Herramienta: Apache JMeter 5.6.3 (modo no-GUI)
Fecha/hora: 2026-10-01T07:33:13.213Z → 07:34:13.196Z (UTC) — 2026-10-01 02:33–02:34 hora local (COT, UTC-5)
```

---

## 2. Objetivo

Establecer la **línea base de throughput** de `GET /v1/breweries` bajo una carga sostenida de **10 hilos concurrentes durante 60 segundos**, con loop continuo y sin think time. Se registran las peticiones por segundo alcanzadas, la distribución de códigos HTTP y la presencia o ausencia de respuestas **HTTP 429** (rate limiting), distinguiéndolas de otros errores HTTP o de red.

---

## 3. Criterios del caso

```text
Threads: 10
Duración: 60 segundos
Endpoint: GET /v1/breweries
HTTP esperado: 200
Throughput mínimo: no definido
HTTP 429: registrar presencia o ausencia
```

No se aplicó ningún umbral de throughput ni de latencia: el criterio de 3000 ms pertenece a TC-REN-004 y no se usó aquí.

---

## 4. Ambiente

```text
JMeter version: 5.6.3 (jmeter -v; log "Version 5.6.3"). Instalación en C:\tools\apache-jmeter-5.6.3 (binario oficial verificado por SHA-512, instalado con autorización para TC-REN-004)
Java version: 22 (Java HotSpot(TM) 64-Bit Server VM, build 22+36-2370)
Sistema operativo: Windows 11 (build 10.0.26200, amd64)
Fecha/hora: 2026-10-01T07:33:13Z (UTC)
Threads: 10
Duration: 60 s
Endpoint: https://api.openbrewerydb.org/v1/breweries
Ubicación del runner: equipo local del analista; no verificada (zona horaria COT, UTC-5)
Tipo de conexión: no verificado
```

Las mediciones son **end-to-end desde este equipo** e incluyen red, DNS, TLS e infraestructura del proveedor.

---

## 5. Configuración JMeter

Archivo: `jmeter/TC-REN-005.jmx`

```text
Test Plan: TC-REN-005 - Throughput
└── Thread Group: TC-REN-005 - Thread Group
    ├── HTTP Request Defaults
    └── HTTP Request: TC-REN-005 - GET breweries
(sin assertions, timers ni listeners en el plan; el Dashboard se genera desde el .jtl)
```

```text
Threads: ${__P(threads,10)} → oficial 10
Ramp-Up: ${__P(rampup,0)} → oficial 0 s
Loop: continuo (LoopController.loops = -1)
Scheduler: habilitado
Duration: ${__P(duration,60)} → oficial 60 s
Think Time: ninguno (sin Constant/Uniform Random Timer)
Throughput Timer: ninguno (sin Constant Throughput Timer ni limitadores)
Synchronizing Timer: no (carga continua, no por ráfagas)
Protocol: https
Host: api.openbrewerydb.org
Method: GET
Path: /v1/breweries (sin query params, body ni autenticación)
Timeouts técnicos: connect 30000 ms / response 60000 ms (salvaguardas; no son criterio)
On sample error: continue (un 429 u otro error no detiene la campaña)
```

Sin Response Assertion, el código HTTP real de cada muestra se conserva tal cual en el JTL. JMeter marca los 4xx/5xx como `success=false` sin transformarlos.

---

## 6. Preflight

Con la misma plantilla y `-Jthreads=1 -Jrampup=0 -Jduration=5` (inicio de comando 07:32:53Z UTC):

```text
Muestras: 45 (1 hilo, 5 s)
Códigos: 200 × 45
URL: https://api.openbrewerydb.org/v1/breweries
Elapsed: 856 ms la primera muestra (con conexión TLS), 91–96 ms el resto
Errores: 0
```

Confirmó que JMeter funciona, DNS/TLS, el endpoint, la generación del JTL, la captura de códigos HTTP y la estructura del plan. **No forma parte de la campaña oficial** ni de sus métricas. Evidencia: `evidencias/preflight-results.jtl`, `preflight-jmeter.log` y `preflight-console.txt`.

---

## 7. Procedimiento

1. **Validación del JMX** — Parseado como XML válido (`jmeterTestPlan`, jmeter 5.6.3). Elementos: TestPlan, ThreadGroup (LoopController −1, scheduler), ConfigTestElement (HTTP Request Defaults) y HTTPSamplerProxy. Se confirmó la ausencia de timers, throughput timer y listeners. `scripts/calcular_metricas.py` compiló sin errores.
2. **Preflight** — 1 hilo, 5 s (sección 6).
3. **Run oficial** — Antes se comprobó que no existían `dashboard/` ni el JTL oficial. Comando (inicio 07:33:11Z UTC; fin del proceso, con generación del Dashboard, 07:34:15Z), exit code `0`:
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
4. **Generación del JTL** — CSV con `timeStamp, elapsed, label, responseCode, responseMessage, threadName, dataType, success, failureMessage, bytes, sentBytes, grpThreads, allThreads, URL, Latency, IdleTime, Connect`; 6610 filas. No se editó.
5. **Dashboard** — `dashboard/TC-REN-005/` (`index.html`, `statistics.json` y las páginas `OverTime.html`, `Throughput.html`, `ResponseTimes.html` y `CustomsGraphs.html`, con las gráficas Response Time Over Time, Active Threads Over Time, Transactions per Second y Response Codes per Second).
6. **Cálculo independiente de métricas** — `python scripts/calcular_metricas.py` (solo lee el JTL; toma el throughput de JMeter desde `statistics.json`) escribió `evidencias/TC-REN-005-metricas.json`. Se contrastó con un segundo recálculo directo sobre el JTL y con el Dashboard, y todo coincide.
7. **Análisis de throughput** — Sección 9.
8. **Análisis de 429** — Sección 11.
9. **Determinación del estado** — Sección 16. No se requirió repetición: el run fue técnicamente válido y completo.

---

## 8. Volumen de ejecución

| Métrica | Resultado |
|---|---:|
| Duración configurada | 60 s |
| Ventana observada | 59.983 s |
| Threads | 10 (10 hilos distintos en el JTL) |
| Total samples | 6610 |
| HTTP 200 | 6610 |
| HTTP 429 | 0 |
| Otros HTTP | 0 |
| Errores de red | 0 |

**Ventana observada:** primer inicio de muestra (`timeStamp` 1790839993213 = 07:33:13.213Z) hasta el máximo de `timeStamp + elapsed` (1790840053196 = 07:34:13.196Z). La duración total del proceso de consola (~64 s) incluye el arranque de JMeter y la generación del Dashboard, y no se usa para el throughput. Cada hilo ejecutó entre 638 y 711 muestras.

---

## 9. Throughput

| Métrica | Resultado |
|---|---:|
| Throughput JMeter | 110.198 req/s (110.19788940199723) |
| Throughput derivado total | 110.198 req/s (6610 / 59.983 s) |
| Throughput HTTP 200 | 110.198 req/s (6610 / 59.983 s) |

- **JMeter** reporta el throughput en req/s (`statistics.json` → `throughput` de la etiqueta *TC-REN-005 - GET breweries*); no hizo falta convertir unidades.
- El **throughput derivado** coincide con el de JMeter (diferencia < 1e-13 req/s), porque ambos usan la misma ventana (primer inicio → último fin).
- El **throughput HTTP 200** es igual al total porque el 100 % de las respuestas fueron 200.
- Por segundo, contado por el `timeStamp` de inicio: 60 segundos con muestras, entre 52 req (primer segundo, apertura de conexiones) y 115 req. Los resúmenes intermedios de la consola fueron 106.2, 111.4 y 111.6 req/s, con un total de 110.0/s.

---

## 10. Distribución HTTP

| Código/Tipo | Cantidad | Porcentaje |
|---|---:|---:|
| 200 | 6610 | 100 % |

Solo se observó el código 200.

---

## 11. Rate limiting

```text
¿Se observaron HTTP 429?: No
Cantidad: 0
Porcentaje: 0 %
Primera aparición: no aplica
Comportamiento: no aplica
Impacto sobre throughput HTTP 200: ninguno (throughput HTTP 200 = throughput total = 110.198 req/s)
```

---

## 12. Latencia durante carga

| Métrica | Resultado |
|---|---:|
| Min | 80 ms |
| Max | 630 ms |
| Average | 90.57 ms |
| Median | 90 ms |
| P90 | 94 ms |
| P95 | 95 ms |
| P99 | 98 ms |

Método de percentiles: **nearest-rank** (posición = ⌈p/100 × N⌉, N = 6610). Los valores coinciden con los del Dashboard de JMeter (pct1/pct2/pct3 = 94.0 / 95.0 / 98.0; media 90.566, mediana 90.0, mín 80, máx 630). **Estas métricas son descriptivas en TC-REN-005** y no se evaluaron contra ningún umbral.

---

## 13. Errores no 429

No se registraron errores distintos de HTTP 429. Tampoco hubo ningún 429, ningún código no HTTP (`Non HTTP response code`) ni ningún error de red o timeout, y el log de JMeter no contiene entradas `ERROR`.

---

## 14. Línea base establecida

Bajo una carga de 10 hilos concurrentes durante 60 segundos, el endpoint alcanzó un throughput de **110.198 req/s** según JMeter (**110.198 req/s** según cálculo independiente: 6610 muestras / 59.983 s). El throughput de respuestas HTTP 200 fue de **110.198 req/s**. No se observaron respuestas HTTP 429.

Latencia descriptiva bajo esta carga: media 90.57 ms, mediana 90 ms y P95 95 ms, medidos end-to-end desde el runner local.

---

## 15. Evidencias

```text
jmeter/TC-REN-005.jmx
scripts/calcular_metricas.py               (solo lee el .jtl y statistics.json; no hace requests)
evidencias/TC-REN-005-results.jtl          (JTL CSV oficial — 6610 muestras)
evidencias/TC-REN-005-jmeter.log           (log de JMeter — run oficial)
evidencias/TC-REN-005-console.txt          (salida de consola — run oficial)
evidencias/TC-REN-005-metricas.json        (métricas, incluida la distribución por segundo)
dashboard/TC-REN-005/                      (Dashboard HTML de JMeter)
evidencias/preflight-results.jtl           (preflight — 1 hilo, 5 s, 45 muestras; excluido)
evidencias/preflight-jmeter.log
evidencias/preflight-console.txt
TC-REN-005_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios.

---

## 16. Resultado final

```text
Estado: APROBADO

Justificación:
JMeter ejecutó correctamente en modo no-GUI la campaña oficial con 10 hilos,
ramp-up 0 s, loop continuo y duración configurada de 60 s (ventana observada de
59.983 s) contra GET https://api.openbrewerydb.org/v1/breweries, sin think time
ni throughput artificial. Se obtuvieron 6610 muestras, todas HTTP 200: 0 HTTP
429, 0 otros códigos y 0 errores de red. El throughput se midió y registró: 110.198
req/s según JMeter, coincidente con el cálculo independiente. Se conservan el JTL,
los logs y el Dashboard, y no hubo fallos técnicos que invalidaran la medición. El
caso no define un throughput mínimo: el valor queda registrado como línea base.
```

---

## 17. Hallazgos

No se identificaron fallos técnicos que invalidaran la línea base de throughput de TC-REN-005.

> No se observó rate limiting (0 respuestas HTTP 429) con 10 hilos durante 60 s, a unos 110 req/s desde un único runner.

---

## 18. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-005
Resultado obtenido: Se ejecutó carga sostenida con 10 hilos concurrentes durante 60 s contra GET /v1/breweries. Se procesaron 6610 muestras. El throughput reportado por JMeter fue 110.198 req/s y el throughput derivado fue 110.198 req/s. HTTP 200: 6610 (100%). HTTP 429: 0 (0%); no se observó rate limiting. Otros errores: 0. La prueba establece esta medición como línea base de throughput; el caso no define un throughput mínimo de aceptación.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-005-results.jtl (complementos: TC-REN-005-metricas.json, dashboard/TC-REN-005/index.html, TC-REN-005-jmeter.log, TC-REN-005-console.txt, jmeter/TC-REN-005.jmx)
Observaciones: Apache JMeter 5.6.3 no-GUI (Java 22, Windows 11), 10 hilos, ramp-up 0 s, loop continuo, 60 s (ventana observada 59.983 s), sin think time ni throughput timer. Latencia descriptiva: media 90.57 ms, mediana 90 ms, P90 94, P95 95, P99 98 ms, máx 630 ms. Preflight de 1 hilo/5 s (45 muestras) excluido. Ejecución el 2026-10-01 07:33 UTC.
```
