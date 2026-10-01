# Informe de Ejecución — TC-REN-001

## 1. Identificación

```text
Caso: TC-REN-001
Nombre: Latencia de listado simple
Tipo: Rendimiento — Latencia base
API: Open BreweryDB
Endpoint: GET /v1/breweries
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T07:10:05.158Z (UTC) — 2026-10-01 02:10:05 hora local (UTC-5)
```

---

## 2. Objetivo

Medir la **latencia base de una única solicitud**, sin carga concurrente, a `GET /v1/breweries` y verificar que responde `200 OK` con un Response Time estrictamente menor a 2000 ms. No es una prueba de carga ni de concurrencia.

---

## 3. Métrica y umbral

```text
Métrica: Response Time de la petición HTTP individual
Fuente: pm.response.responseTime (assertion), corroborado con run.executions[0].response.responseTime del reporte Newman
Umbral: < 2000 ms (estricto: 2000 ms = FAIL)
HTTP esperado: 200 OK
Concurrencia: ninguna (1 iteración, 1 request)
```

---

## 4. Ambiente de medición

```text
Herramienta: Newman 6.2.2 (CLI) sobre Node.js v22.15.1
Versión Newman: 6.2.2
Sistema operativo: Windows (Windows_NT 10.0.26200, x64)
Fecha/hora: 2026-10-01T07:10:05.158Z (UTC)
Tipo de conexión: no verificado
Ubicación del runner: no verificada (equipo local del analista; zona horaria UTC-5)
```

La medición es **end-to-end desde este equipo**. Incluye conectividad del cliente, latencia de red, DNS, TLS y la infraestructura del proveedor. No representa solo el tiempo de procesamiento del servidor.

---

## 5. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Conectividad / acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en el preflight y en el run oficial. |
| Disponibilidad de la API | Comprobada | `200 OK` en ambas ejecuciones. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección y environment válidos | Comprobada | Validados con `JSON.parse` antes del preflight. |
| Registro del Response Time | Comprobada | `pm.response.responseTime` numérico en el preflight (571 ms) y en el run oficial (316 ms). |

---

## 6. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Endpoint: {{base_url}}/breweries
URL final: https://api.openbrewerydb.org/v1/breweries
Método: GET
Query Params: Ninguno (Newman: "query": [])
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de requests del run oficial: 1 (iteraciones: 1; sin hilos, usuarios virtuales ni ejecución en paralelo)
```

---

## 7. Procedimiento

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Rendimiento* → carpeta `TC-REN-001` → request *TC-REN-001 - Latencia de listado simple* (`GET {{base_url}}/breweries`). La request tiene 3 assertions obligatorias, 2 auxiliares y diagnóstico por consola. Se validaron ambos JSON y se registró el ambiente (Newman, Node.js y SO).
2. **Preflight** (inicio de comando 07:09:52Z UTC) — **Una sola ejecución** para comprobar conectividad, endpoint, HTTP real, Newman, las assertions y el registro del Response Time. Resultado: `200 OK`, **571 ms**, 5/5 PASS, exit code 0. No se usa para determinar el estado. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Run oficial** (07:10:05.158Z → 07:10:05.573Z UTC), una iteración con una request, exit code `0`:
   ```bash
   newman run postman/TC-REN-001.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-REN-001" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-REN-001-newman.json \
     --reporter-htmlextra-export evidencias/TC-REN-001-newman.html \
     > evidencias/TC-REN-001-newman.txt 2>&1
   ```
4. **Extracción de métricas** — Del reporte JSON oficial: `run.executions` contiene 1 ejecución; `response.responseTime` = 316 ms, que coincide con el valor de `pm.response.responseTime` registrado por consola y en la CLI de Newman (`[200 OK, 22.1kB, 316ms]`); `response.responseSize` = 20731 bytes. El cuerpo se guardó en `evidencias/response-body.json` (arreglo JSON de 50 registros, solo con indentación).
5. **Evaluación del umbral** — `316 < 2000` → cumple. Margen = 2000 − 316 = **1684 ms**.
6. **Repetición** — **No requerida**: el run oficial no alcanzó ni superó 2000 ms.
7. **Determinación del estado** — HTTP 200, Response Time < 2000 ms y 0 assertions fallidas, por lo que el caso queda **APROBADO**.

La duración total del run (415 ms, de `run.timings`) incluye trabajo de Newman y **no** se usa como métrica.

---

## 8. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-REN-001-newman.json`).

**Obligatorias**

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | HTTP | 200 | 200 OK | PASS |
| 2 | Response Time | < 2000 ms | 316 ms | PASS |
| 3 | Response Time válido | número >= 0 | 316 (number) | PASS |

**Auxiliares** (no sustituyen la métrica de rendimiento)

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| A1 | Content-Type | JSON | `application/json` | PASS |
| A2 | JSON válido | Sí | Sí (arreglo de 50 registros) | PASS |

---

## 9. Resultados

```text
HTTP: 200 OK
Response Time oficial: 316 ms
Umbral: < 2000 ms
¿Cumple umbral?: Sí
Margen frente a 2000 ms: 1684 ms
Response Size: 20731 bytes
Assertions: 5 ejecutadas (3 obligatorias + 2 auxiliares) — 5 PASS, 0 FAIL
Exit code Newman: 0
```

Se trata de **una única medición**: no se calculan promedio, mediana, percentiles ni desviación estándar. El valor de preflight (571 ms) se registra solo como trazabilidad y no participa en la evaluación.

---

## 10. Comparación contra el umbral

| Métrica | Obtenido | Límite | Diferencia | Estado |
|---|---:|---:|---:|---|
| Response Time | 316 ms | 2000 ms | 1684 ms por debajo del límite | PASS |

---

## 11. Repetición de confirmación

No fue necesaria. El run oficial (316 ms) no alcanzó el umbral de 2000 ms, así que no se ejecutó ninguna repetición.

---

## 12. Evidencias

```text
postman/TC-REN-001.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-REN-001-newman.json     (reporte JSON — run oficial)
evidencias/TC-REN-001-newman.txt      (salida de consola — run oficial)
evidencias/TC-REN-001-newman.html     (reporte HTML htmlextra — run oficial)
evidencias/response-body.json         (cuerpo real — run oficial)
evidencias/preflight-1-newman.json    (preflight — 571 ms, 5/5 PASS)
evidencias/preflight-1-newman.txt
TC-REN-001_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios.

---

## 13. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman (1 iteración, 1 request, sin concurrencia),
GET https://api.openbrewerydb.org/v1/breweries respondió HTTP 200 OK con un
Response Time de 316 ms, estrictamente menor al umbral de 2000 ms (margen de
1684 ms). Las 5 assertions (3 obligatorias y 2 auxiliares) se aprobaron (0
fallidas) y Newman terminó con código de salida 0.
```

---

## 14. Hallazgos

No se identificaron incumplimientos del umbral de latencia durante TC-REN-001.

---

## 15. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-001
Resultado obtenido: GET /v1/breweries respondió HTTP 200 con un Response Time oficial de 316 ms. El umbral definido para TC-REN-001 es < 2000 ms, por lo que CUMPLE. Margen frente al límite: 1684 ms. Se ejecutaron 5 assertions: 5 aprobadas y 0 fallidas. Exit code Newman: 0.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-001-newman.json (complementos: TC-REN-001-newman.txt, TC-REN-001-newman.html, response-body.json)
Observaciones: Medición individual end-to-end desde equipo local Windows (Newman 6.2.2, Node.js v22.15.1), 1 request sin concurrencia, el 2026-10-01 07:10 UTC. Response Size 20731 bytes. Preflight previo: 571 ms (no usado para el resultado). No se requirió repetición.
```
