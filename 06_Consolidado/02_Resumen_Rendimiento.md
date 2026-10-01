# Resumen de Rendimiento — Open BreweryDB (TC-REN-001 a TC-REN-005)

> Consolidado a partir de los informes individuales y de las evidencias crudas (Newman JSON, `metricas.json`, JTL y `statistics.json` de JMeter). Las rutas son relativas a `06_Consolidado/`. No se reejecutó ninguna prueba.

---

## 1. Criterios vigentes y compatibilidad de los informes

| ID | Criterio vigente (versión definitiva) | Informe utilizado | ¿Aplica el criterio vigente? |
|---|---|---|---|
| TC-REN-001 | Response Time < 2000 ms | `../05_Rendimiento/TC-REN-001/TC-REN-001_Informe.md` | Sí |
| TC-REN-002 | Response Time < 1500 ms | `../05_Rendimiento/TC-REN-002/TC-REN-002_Informe.md` | Sí |
| TC-REN-003 | 50 secuenciales; 100 % HTTP 200; P95 < 2000 ms | `../05_Rendimiento/TC-REN-003/TC-REN-003_Informe.md` (commit `dae6dcb`) | Sí |
| TC-REN-004 | 10 hilos; ≥ 95 % < 3000 ms; 0 % errores | `../05_Rendimiento/TC-REN-004/TC-REN-004_Informe.md` | Sí |
| TC-REN-005 | 10 hilos × 60 s; ≥ 99.18 req/s; 100 % HTTP 200; 0 % HTTP 429 | `../05_Rendimiento/TC-REN-005/TC-REN-005_Informe.md` (commit `dae6dcb`) | Sí |

TC-REN-003 y TC-REN-005 tuvieron una ejecución anterior con los criterios del plan v1.0 (TC-REN-003: desviación estándar "baja" sin umbral; TC-REN-005: línea base sin mínimo). Esas versiones están en el historial de git (commit `0b9d9b2`) y **no se usan como definitivas**. La línea base de 110.198 req/s del criterio vigente de TC-REN-005 procede de esa ejecución anterior, según su propio informe.

---

## 2. Tabla consolidada

| ID | Escenario | Endpoint | Configuración | Métrica principal | Criterio | Resultado real | Estado | Evidencia principal |
|---|---|---|---|---|---|---|---|---|
| TC-REN-001 | Latencia de listado simple | `GET /v1/breweries` | Newman, 1 request, sin concurrencia | Response Time | < 2000 ms | **316 ms**, HTTP 200 (margen 1684 ms) | APROBADO | `../05_Rendimiento/TC-REN-001/evidencias/TC-REN-001-newman.json` |
| TC-REN-002 | Latencia de búsqueda | `GET /v1/breweries/search?query=san` | Newman, 1 request, sin concurrencia | Response Time | < 1500 ms | **331 ms**, HTTP 200 (margen 1169 ms) | APROBADO | `../05_Rendimiento/TC-REN-002/evidencias/TC-REN-002-newman.json` |
| TC-REN-003 | Estabilidad bajo repetición | `GET /v1/breweries/random` | Newman, 50 iteraciones secuenciales | Tasa de éxito y P95 | 100 % HTTP 200 y P95 < 2000 ms | **50/50 HTTP 200; P95 259 ms** | APROBADO | `../05_Rendimiento/TC-REN-003/evidencias/TC-REN-003-newman.json` |
| TC-REN-004 | Carga moderada | `GET /v1/breweries` | JMeter no-GUI, 10 hilos, ramp-up 0 s, 1 loop, Synchronizing Timer de 10 | % < 3000 ms y error rate | ≥ 95 % y 0 % | **100 % (10/10); 0 % errores; P95 624 ms** | APROBADO | `../05_Rendimiento/TC-REN-004/evidencias/TC-REN-004-results.jtl` |
| TC-REN-005 | Throughput | `GET /v1/breweries` | JMeter no-GUI, 10 hilos, ramp-up 0 s, loop continuo, 60 s | Throughput, HTTP 200 y HTTP 429 | ≥ 99.18 req/s; 100 %; 0 % | **103.31 req/s; 6200/6200 HTTP 200; 0 HTTP 429** | APROBADO | `../05_Rendimiento/TC-REN-005/evidencias/TC-REN-005-results.jtl` |

Resultado global de rendimiento: **5/5 APROBADO** con los criterios vigentes.

---

## 3. Métricas detalladas

### 3.1 Latencia individual (TC-REN-001 y TC-REN-002)

| ID | Fecha/hora (UTC) | HTTP | Response Time | Response Size | Assertions |
|---|---|---:|---:|---:|---|
| TC-REN-001 | 2026-10-01T07:10:05Z | 200 | 316 ms | 20 731 bytes | 5/5 |
| TC-REN-002 | 2026-10-01T07:13:43Z | 200 | 331 ms | 21 738 bytes (50 resultados) | 6/6 |

Son mediciones únicas: no se calcula promedio ni percentiles.

### 3.2 Estabilidad (TC-REN-003) — fuente `../05_Rendimiento/TC-REN-003/evidencias/metricas.json`

| Métrica | Valor |
|---|---:|
| N / HTTP 200 / tasa de éxito | 50 / 50 / 100 % |
| Mínimo / máximo | 220 / 521 ms |
| Media / mediana | 239.08 / 230.50 ms |
| P95 (nearest-rank, posición 48) | 259 ms |
| Desviación estándar poblacional | 41.82 ms |
| Coeficiente de variación | 17.49 % |

El máximo (521 ms) corresponde a la iteración 1; las 49 restantes estuvieron entre 220 y 265 ms (según el informe y `tiempos-response.json`).

### 3.3 Concurrencia (TC-REN-004) — fuente `../05_Rendimiento/TC-REN-004/evidencias/TC-REN-004-metricas.json`

| Métrica | Valor |
|---|---:|
| Muestras / HTTP 200 / errores | 10 / 10 / 0 |
| Inicio de las 10 muestras | mismo `timeStamp` (dispersión 0 ms) |
| Mínimo / máximo / media / mediana | 613 / 624 / 618.7 / 619.5 ms |
| P95 (nearest-rank = máximo con N = 10) | 624 ms (Dashboard: 624.0) |
| Throughput observado (diagnóstico) | 16.03 req/s |

### 3.4 Throughput (TC-REN-005) — fuente `../05_Rendimiento/TC-REN-005/evidencias/TC-REN-005-metricas.json`

| Métrica | Valor |
|---|---:|
| Ventana observada | 60.012 s |
| Muestras / HTTP 200 / HTTP 429 / otros / errores de red | 6200 / 6200 / 0 / 0 / 0 |
| Throughput JMeter = derivado = HTTP 200 | 103.3127 req/s |
| Margen sobre el mínimo (99.18) | +4.13 req/s |
| Degradación frente a la línea base (110.198) | 6.25 % (tolerancia 10 %) |
| Mínimo / máximo / media / mediana | 85 / 592 / 96.58 / 95 ms |
| P90 / P95 / P99 | 101 / 104 / 115 ms (iguales a los del Dashboard) |

---

## 4. Análisis

### 4.1 Latencia individual
Ambas solicitudes individuales quedaron muy por debajo de sus umbrales: el listado con 316 frente a 2000 ms y la búsqueda con 331 frente a 1500 ms. Son mediciones únicas end-to-end desde el equipo local. Incluyen el establecimiento de conexión, porque cada ejecución de Newman abre una conexión nueva.

### 4.2 Estabilidad
Las 50 repeticiones secuenciales de `/random` tuvieron un 100 % de éxito y un P95 de 259 ms. La dispersión es baja en valores absolutos (σ = 41.82 ms; CV 17.49 %) y se concentra en la primera iteración. El plan vigente solo exige P95 < 2000 ms; σ y CV se reportan como descriptivos.

### 4.3 Concurrencia
Con 10 hilos liberados a la vez no hubo errores y todas las respuestas estuvieron por debajo de 3000 ms, entre 613 y 624 ms. El JTL muestra que **en las 10 muestras el tiempo de conexión (`Connect`) fue de unos 493–497 ms**: cada hilo abrió su propia conexión TLS en el mismo instante. La mayor parte del tiempo observado corresponde, por tanto, al establecimiento de conexión y no al procesamiento de la petición.

### 4.4 Throughput
Con 10 hilos durante 60 s se sostuvieron 103.31 req/s, sin errores ni 429. Solo las 10 primeras muestras (una por hilo) incluyeron conexión (`Connect` > 0, mediana de 448 ms). Las demás reutilizaron la conexión keep-alive, con una mediana de 95 ms.

### 4.5 Errores y HTTP 429
En las campañas de rendimiento no se registró ningún código distinto de 200, ningún error de red y **ningún HTTP 429**: 0 de 6200 en TC-REN-005 y 0 de 10 en TC-REN-004. No hay evidencia de rate limiting bajo los perfiles probados.

### 4.6 Comportamiento al incrementar la carga — límites de comparación
**No se presenta una curva de degradación latencia/carga**, porque las campañas no son equivalentes:
- se ejecutaron en momentos distintos (07:10, 07:13, 07:26, 15:52 y 16:01 UTC del 01/10/2026);
- usan herramientas distintas (Newman frente a JMeter) y endpoints distintos (TC-REN-003 usa `/random`);
- tienen patrones de conexión distintos: conexión nueva por request en TC-REN-001, 002 y 004, y conexiones reutilizadas en TC-REN-003 y en la mayoría de TC-REN-005.

Lo que sí puede afirmarse con la evidencia:
- pasar de 1 a 10 hilos concurrentes **no produjo errores ni respuestas 429**;
- con carga sostenida de 10 hilos, la latencia de las peticiones con conexión reutilizada se mantuvo estable (P99 = 115 ms en 6200 muestras);
- las diferencias de latencia observadas entre TC-REN-004 (≈ 619 ms) y TC-REN-005 (≈ 95 ms) se explican, según el JTL, principalmente por el establecimiento de conexión y no por la carga.

TC-REN-005 quedó un 6.25 % por debajo de la línea base (110.198 → 103.31 req/s), dentro de la tolerancia. Ambas mediciones se tomaron desde el mismo runner con unas 8.5 horas de diferencia, por lo que parte de la variación puede deberse a la red del cliente.

---

## 5. Evidencias por caso

| ID | Informe | Evidencia principal | Complementarias |
|---|---|---|---|
| TC-REN-001 | `../05_Rendimiento/TC-REN-001/TC-REN-001_Informe.md` | `../05_Rendimiento/TC-REN-001/evidencias/TC-REN-001-newman.json` | `TC-REN-001-newman.txt`, `TC-REN-001-newman.html`, `response-body.json`, `preflight-1-newman.*`, `postman/` |
| TC-REN-002 | `../05_Rendimiento/TC-REN-002/TC-REN-002_Informe.md` | `../05_Rendimiento/TC-REN-002/evidencias/TC-REN-002-newman.json` | `TC-REN-002-newman.txt`, `TC-REN-002-newman.html`, `response-body.json`, `preflight-1-newman.*`, `postman/` |
| TC-REN-003 | `../05_Rendimiento/TC-REN-003/TC-REN-003_Informe.md` | `../05_Rendimiento/TC-REN-003/evidencias/TC-REN-003-newman.json` | `metricas.json`, `tiempos-response.json`, `muestra-response.json`, `TC-REN-003-newman.txt/.html`, `preflight-1-newman.*`, `scripts/calcular_metricas.js` |
| TC-REN-004 | `../05_Rendimiento/TC-REN-004/TC-REN-004_Informe.md` | `../05_Rendimiento/TC-REN-004/evidencias/TC-REN-004-results.jtl` | `TC-REN-004-metricas.json`, `TC-REN-004-jmeter.log`, `TC-REN-004-console.txt`, `../05_Rendimiento/TC-REN-004/dashboard/TC-REN-004/index.html`, `jmeter/TC-REN-004.jmx`, `preflight-*` |
| TC-REN-005 | `../05_Rendimiento/TC-REN-005/TC-REN-005_Informe.md` | `../05_Rendimiento/TC-REN-005/evidencias/TC-REN-005-results.jtl` | `TC-REN-005-metricas.json`, `TC-REN-005-jmeter.log`, `TC-REN-005-console.txt`, `../05_Rendimiento/TC-REN-005/dashboard/TC-REN-005/index.html`, `jmeter/TC-REN-005.jmx`, `preflight-*` |

Las rutas completas de todos los archivos están en [`03_Indice_Evidencias.md`](03_Indice_Evidencias.md).
