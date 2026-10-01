# Informe de Ejecución — TC-REN-004

## 1. Identificación

```text
Caso: TC-REN-004
Nombre: Carga moderada
Tipo: Rendimiento — Carga concurrente
API: Open BreweryDB
Endpoint: GET /v1/breweries
Herramienta: Apache JMeter 5.6.3 (modo no-GUI)
Fecha/hora: 2026-10-01T07:26:14.849Z → 07:26:15.473Z (UTC) — 2026-10-01 02:26:14 hora local (COT, UTC-5)
```

---

## 2. Objetivo

Evaluar el comportamiento de `GET /v1/breweries` cuando **10 hilos (usuarios virtuales) ejecutan la petición de forma concurrente**, liberados juntos por un Synchronizing Timer. Se verifica que al menos el 95 % de las muestras tengan `elapsed < 3000 ms`, que la tasa de error sea 0 % y que todas las respuestas sean HTTP 200.

---

## 3. Criterios

```text
Threads: 10
Loops: 1
Total esperado: 10
HTTP esperado: 200
Latencia: >=95% de requests <3000 ms (estricto: 3000 ms queda fuera)
Error rate: 0%
```

Con 10 muestras, el ≥95 % solo se cumple con **10/10** muestras < 3000 ms, porque 9/10 equivale a 90 %.

---

## 4. Justificación de configuración

El caso define 10 hilos concurrentes pero no especifica duración ni repeticiones por hilo. Para no introducir una carga adicional no definida, se utilizó un ciclo por hilo, para un total de 10 muestras concurrentes. La carga sostenida corresponde a TC-REN-005.

---

## 5. Ambiente

```text
JMeter version: 5.6.3 (log: "Version 5.6.3"; banner de jmeter -v)
Java version: 22 (Java HotSpot(TM) 64-Bit Server VM, build 22+36-2370)
Sistema operativo: Windows 11 (os.version 10.0, build 10.0.26200, amd64)
Fecha/hora: 2026-10-01T07:26:14Z (UTC)
Endpoint: https://api.openbrewerydb.org/v1/breweries
Runner/localidad: equipo local del analista; ubicación no verificada (zona horaria COT, UTC-5)
Tipo de conexión: no verificado
```

**Instalación de JMeter (con autorización del usuario):** JMeter no estaba instalado: no figuraba en el PATH, no había `JMETER_HOME` y no se encontró ningún `ApacheJMeter.jar` en disco. Con autorización explícita del usuario, se descargó el binario oficial `apache-jmeter-5.6.3.zip` desde `archive.apache.org`. Se verificó su SHA-512 contra el `.sha512` publicado (`387fadca…40b0163076`, coincide) y se descomprimió en `C:\tools\apache-jmeter-5.6.3`, fuera del proyecto y sin modificar el PATH. Los avisos `WARN StatusConsoleListener …package scanning…` de la consola son de log4j y no afectan a la ejecución.

Las métricas son **end-to-end desde este equipo**. Incluyen red, DNS, TLS e infraestructura del proveedor.

---

## 6. Plan JMeter

Archivo: `jmeter/TC-REN-004.jmx`

```text
Test Plan: TC-REN-004 - Carga moderada
└── Thread Group: TC-REN-004 - Thread Group
    ├── Synchronizing Timer
    ├── HTTP Request Defaults
    ├── HTTP Request: TC-REN-004 - GET breweries
    │   └── Response Assertion - HTTP 200
(sin listeners en el plan; el Dashboard se genera desde el .jtl)
```

```text
Threads: ${__P(threads,10)}  → oficial 10
Ramp-Up: ${__P(rampup,0)}    → oficial 0 s
Loops: ${__P(loops,1)}       → oficial 1
Synchronizing Timer: groupSize = ${__P(threads,10)} → oficial 10; timeoutInMs = 60000 (salvaguarda técnica para que un hilo bloqueado no deje el test esperando indefinidamente)
Protocol: https
Host: api.openbrewerydb.org
Port: vacío (estándar HTTPS)
Path: /v1/breweries
Method: GET (sin query params, body ni autenticación)
Assertion: Response Assertion — campo Response Code, tipo "Equals", valor "200" (cualquier otro código marca la muestra como fallida)
Timeouts técnicos: connect 30000 ms / response 60000 ms (salvaguardas muy superiores al umbral; no se usó 3000 ms como timeout)
On sample error: continue
```

---

## 7. Preflight

Con la misma plantilla y `-Jthreads=1 -Jrampup=0 -Jloops=1` (inicio de comando 07:25:59Z UTC):

```text
Muestras: 1
HTTP: 200 OK, success=true
Elapsed: 792 ms (Latency 785 ms, Connect 682 ms)
URL: https://api.openbrewerydb.org/v1/breweries
Synchronizing Timer: no bloqueó (groupSize = 1)
Errores: 0
```

Confirmó que JMeter funciona, que el endpoint es correcto, que responde HTTP 200, que se genera el JTL y que la assertion se evalúa. **No forma parte de las 10 muestras oficiales.** Evidencia: `evidencias/preflight-results.jtl`, `preflight-jmeter.log` y `preflight-console.txt`.

---

## 8. Procedimiento

1. **Validación del JMX** — El `.jmx` se parseó como XML válido (`jmeterTestPlan`, jmeter 5.6.3) y se comprobó que contiene TestPlan, ThreadGroup, SyncTimer, HTTP Request Defaults, HTTPSamplerProxy y ResponseAssertion. El script `scripts/calcular_metricas.py` se compiló sin errores.
2. **Preflight** — 1 hilo, ver sección 7.
3. **Ejecución no-GUI** — Antes del run se comprobó que no existían `dashboard/` ni el JTL oficial. Comando (inicio 07:26:13Z UTC), exit code `0`:
   ```bash
   jmeter -n \
     -t jmeter/TC-REN-004.jmx \
     -Jthreads=10 \
     -Jrampup=0 \
     -Jloops=1 \
     -l evidencias/TC-REN-004-results.jtl \
     -j evidencias/TC-REN-004-jmeter.log \
     -e \
     -o dashboard/TC-REN-004 \
     > evidencias/TC-REN-004-console.txt 2>&1
   ```
   (ejecutado como `C:\tools\apache-jmeter-5.6.3\bin\jmeter.bat` con rutas Windows)
4. **Generación del JTL** — CSV con cabecera `timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Latency,IdleTime,Connect`, 10 filas. No se editó.
5. **Generación del Dashboard** — `dashboard/TC-REN-004/` (`index.html`, `statistics.json`, `content/`, `sbadmin2-1.0.7/`).
6. **Cálculo independiente** — `python scripts/calcular_metricas.py` (solo lee el JTL) escribió `evidencias/TC-REN-004-metricas.json`. Los resultados se contrastaron con un segundo recálculo directo sobre el JTL y con `dashboard/TC-REN-004/statistics.json`, y coinciden.
7. **Evaluación de criterios** — Ver sección 10.
8. **Repetición** — **No requerida**: el run oficial cumplió todos los criterios.

---

## 9. Resultados de muestras

| Métrica | Resultado |
|---|---:|
| Total samples | 10 |
| HTTP 200 | 10 |
| No 200 | 0 |
| Success | 10 |
| Failed | 0 |
| Error % | 0 % |
| Requests <3000 ms | 10 |
| Requests >=3000 ms | 0 |
| % <3000 ms | 100 % |
| Min | 613 ms |
| Max | 624 ms |
| Average | 618.7 ms |
| Median | 619.5 ms |
| P95 | 624 ms |
| Throughput observado | 16.03 req/s |

El throughput es **diagnóstico**: 10 muestras / ventana de 624 ms, desde el primer inicio hasta el último fin. Coincide con el `throughput` del Dashboard (16.0256 req/s). No es un criterio de TC-REN-004.

---

## 10. Evaluación de criterios

| Criterio | Esperado | Obtenido | Estado |
|---|---:|---:|---|
| Hilos | 10 | 10 (10 hilos distintos en el JTL: 1-1 … 1-10) | PASS |
| HTTP 200 | 100 % | 100 % (10/10) | PASS |
| Peticiones <3000 ms | >=95 % | 100 % (10/10) | PASS |
| Error rate | 0 % | 0 % (0/10) | PASS |

**Evidencia de concurrencia (JTL):** los 10 hilos aparecen con el mismo `timeStamp` de inicio, 1790839574849 (2026-10-01T07:26:14.849Z); la dispersión de inicios es 0 ms. Cuando arrancó la última muestra, las 10 estaban en curso, y la ventana total fue de 624 ms, frente a 6 186 ms que sumarían ejecutadas en serie. `grpThreads/allThreads` = 10 en las primeras muestras que terminaron, lo que confirma que los 10 hilos estaban activos a la vez. La precisión del timestamp es de milisegundos: esto demuestra ejecución concurrente, no simultaneidad exacta.

---

## 11. Distribución de tiempos

Las 10 muestras oficiales, en el orden en que aparecen en el JTL (orden de finalización):

| Sample | Thread | HTTP | Elapsed ms | <3000 | Success |
|---:|---|---:|---:|---|---|
| 1 | TC-REN-004 - Thread Group 1-8 | 200 | 613 | Sí | true |
| 2 | TC-REN-004 - Thread Group 1-9 | 200 | 616 | Sí | true |
| 3 | TC-REN-004 - Thread Group 1-5 | 200 | 616 | Sí | true |
| 4 | TC-REN-004 - Thread Group 1-10 | 200 | 616 | Sí | true |
| 5 | TC-REN-004 - Thread Group 1-7 | 200 | 619 | Sí | true |
| 6 | TC-REN-004 - Thread Group 1-6 | 200 | 620 | Sí | true |
| 7 | TC-REN-004 - Thread Group 1-3 | 200 | 620 | Sí | true |
| 8 | TC-REN-004 - Thread Group 1-2 | 200 | 620 | Sí | true |
| 9 | TC-REN-004 - Thread Group 1-1 | 200 | 623 | Sí | true |
| 10 | TC-REN-004 - Thread Group 1-4 | 200 | 624 | Sí | true |

Todas: `timeStamp` de inicio 1790839574849, URL `https://api.openbrewerydb.org/v1/breweries`, `responseMessage` OK.

---

## 12. Percentil 95

```text
P95 calculado: 624 ms
Método: nearest-rank — posición ceil(0.95 × 10) = 10 → mayor valor de la muestra
P95 Dashboard JMeter: 624.0 ms (pct2ResTime; percentiles por defecto 90/95/99)
```

Ambos coinciden. Como referencia, el Dashboard reporta P90 = 623.9 ms (interpolado) y P99 = 624.0 ms. El criterio principal de latencia es el porcentaje directo de muestras `< 3000 ms` (100 %).

---

## 13. Errores

No se registraron errores ni respuestas HTTP distintas de 200. Tampoco hubo ningún HTTP 429, y el log de JMeter no contiene entradas `ERROR`.

---

## 14. Evidencias

```text
jmeter/TC-REN-004.jmx
scripts/calcular_metricas.py
evidencias/TC-REN-004-results.jtl       (JTL CSV oficial — 10 muestras)
evidencias/TC-REN-004-jmeter.log        (log de JMeter — run oficial)
evidencias/TC-REN-004-console.txt       (salida de consola — run oficial)
evidencias/TC-REN-004-metricas.json     (métricas calculadas desde el JTL oficial)
dashboard/TC-REN-004/                   (Dashboard HTML de JMeter: index.html, statistics.json, content/, sbadmin2-1.0.7/)
evidencias/preflight-results.jtl        (preflight — 1 muestra; excluido de la campaña)
evidencias/preflight-jmeter.log
evidencias/preflight-console.txt
TC-REN-004_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios.

---

## 15. Resultado final

```text
Estado: APROBADO

Justificación:
El run oficial de JMeter en modo no-GUI (10 hilos, ramp-up 0 s, 1 loop,
Synchronizing Timer de 10) generó exactamente 10 muestras concurrentes contra
GET https://api.openbrewerydb.org/v1/breweries, todas iniciadas en el mismo
milisegundo. Las 10 respondieron HTTP 200 con success=true: error rate 0 %. Las
10 tuvieron elapsed < 3000 ms (100 % ≥ 95 %), con mínimo 613 ms, máximo 624 ms,
media 618.7 ms y P95 624 ms. Se cumplen simultáneamente todos los criterios.
```

---

## 16. Hallazgos

No se identificaron incumplimientos de los criterios de carga moderada durante TC-REN-004.

---

## 17. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-004
Resultado obtenido: Se ejecutó una campaña JMeter con 10 hilos concurrentes y 1 request por hilo contra GET /v1/breweries. Se obtuvieron 10/10 HTTP 200, con una tasa de error de 0%. 10/10 peticiones (100%) tuvieron elapsed <3000 ms. El P95 fue de 624 ms. El criterio exige >=95% de peticiones <3000 ms y 0% errores. Resultado: CUMPLE.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-004-results.jtl (complementos: TC-REN-004-metricas.json, dashboard/TC-REN-004/index.html, TC-REN-004-jmeter.log, TC-REN-004-console.txt, jmeter/TC-REN-004.jmx)
Observaciones: Apache JMeter 5.6.3 en modo no-GUI (Java 22, Windows 11), instalado para esta prueba con autorización (binario oficial verificado por SHA-512). Ramp-up 0 s y Synchronizing Timer de 10: los 10 hilos iniciaron en el mismo milisegundo. Min 613 / máx 624 / media 618.7 ms; throughput observado 16.03 req/s (diagnóstico). Preflight de 1 hilo (792 ms) excluido. Ejecución el 2026-10-01 07:26 UTC. No se requirió repetición.
```
