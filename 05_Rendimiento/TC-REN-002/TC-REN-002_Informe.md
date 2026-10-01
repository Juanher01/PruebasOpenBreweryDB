# Informe de Ejecución — TC-REN-002

## 1. Identificación

```text
Caso: TC-REN-002
Nombre: Latencia de búsqueda
Tipo: Rendimiento — Latencia base
API: Open BreweryDB
Endpoint: GET /v1/breweries/search?query=san
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T07:13:43.954Z (UTC) — 2026-10-01 02:13:43 hora local (UTC-5)
```

---

## 2. Objetivo

Medir la **latencia base de una única solicitud de búsqueda**, sin carga concurrente, a `GET /v1/breweries/search?query=san` y verificar que responde `200 OK` con un Response Time estrictamente menor a 1500 ms. No es una prueba de carga ni de concurrencia.

---

## 3. Métrica y umbral

```text
Métrica: Response Time de la petición HTTP individual
Fuente: pm.response.responseTime (assertion), corroborado con run.executions[0].response.responseTime del reporte Newman
Umbral: < 1500 ms (estricto: 1500 ms = FAIL)
HTTP esperado: 200 OK
Query: san
Concurrencia: ninguna (1 iteración, 1 request)
```

---

## 4. Ambiente de medición

```text
Herramienta: Newman 6.2.2 (CLI) sobre Node.js v22.15.1
Versión Newman: 6.2.2
Sistema operativo: Windows (Windows_NT 10.0.26200, x64)
Fecha/hora: 2026-10-01T07:13:43.954Z (UTC)
Tipo de conexión: no verificado
Ubicación del runner: no verificada (equipo local del analista; zona horaria UTC-5)
```

La medición es **end-to-end desde este equipo**. Incluye conectividad del cliente, DNS, TLS, latencia de red e infraestructura del proveedor. No representa solo el tiempo de procesamiento del servidor.

---

## 5. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Conectividad / acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en el preflight y en el run oficial. |
| Disponibilidad de la API | Comprobada | `200 OK` en ambas ejecuciones. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección y environment válidos | Comprobada | Validados con `JSON.parse` antes del preflight. |
| `query=san` exacto | Comprobada | Newman registra `"query": [{"key": "query", "value": "san"}]` como único parámetro. |
| Registro del Response Time | Comprobada | `pm.response.responseTime` numérico en el preflight (615 ms) y en el run oficial (331 ms). |

---

## 6. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries/search?query=san
URL final: https://api.openbrewerydb.org/v1/breweries/search?query=san
Query Params: query=san   (único; sin filtros ni paginación)
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de requests del run oficial: 1 (iteraciones: 1; sin hilos, usuarios virtuales ni ejecución en paralelo)
```

---

## 7. Procedimiento

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Rendimiento* → carpeta `TC-REN-002` → request *TC-REN-002 - Latencia de búsqueda* (`GET {{base_url}}/breweries/search?query=san`). La request tiene 3 assertions obligatorias, 3 auxiliares y diagnóstico por consola. Se validaron ambos JSON.
2. **Preflight** (inicio de comando 07:13:31Z UTC) — **Una sola ejecución** para comprobar conectividad, endpoint, `query=san`, HTTP real, Newman, las assertions y el registro del Response Time. Resultado: `200 OK`, **615 ms**, 6/6 PASS, exit code 0. No se usa para determinar el estado. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Run oficial** (07:13:43.954Z → 07:13:44.376Z UTC), una iteración con una request, exit code `0`:
   ```bash
   newman run postman/TC-REN-002.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-REN-002" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-REN-002-newman.json \
     --reporter-htmlextra-export evidencias/TC-REN-002-newman.html \
     > evidencias/TC-REN-002-newman.txt 2>&1
   ```
4. **Extracción de métricas** — Del reporte JSON oficial: `run.executions` contiene 1 ejecución; `response.responseTime` = 331 ms, que coincide con `pm.response.responseTime` registrado por consola y con la CLI de Newman (`[200 OK, 23.11kB, 331ms]`); `response.responseSize` = 21738 bytes; 50 resultados, como dato diagnóstico. El cuerpo se guardó en `evidencias/response-body.json`, solo con indentación.
5. **Comparación con 1500 ms** — `331 < 1500` → cumple. Margen = 1500 − 331 = **1169 ms**.
6. **Repetición** — **No requerida**: el run oficial no alcanzó ni superó 1500 ms.
7. **Determinación del estado** — HTTP 200, Response Time < 1500 ms y 0 assertions fallidas, por lo que el caso queda **APROBADO**.

La duración total del run (422 ms, de `run.timings`) incluye trabajo de Newman y **no** se usa como métrica.

---

## 8. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-REN-002-newman.json`).

**Obligatorias**

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | HTTP | 200 | 200 OK | PASS |
| 2 | Response Time | < 1500 ms | 331 ms | PASS |
| 3 | Response Time válido | número >= 0 | 331 (number) | PASS |

**Auxiliares** (no sustituyen la métrica de rendimiento)

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| A1 | Content-Type | JSON | `application/json` | PASS |
| A2 | JSON válido | Sí | Sí | PASS |
| A3 | Respuesta tipo arreglo | Array | Array (50 elementos) | PASS |

---

## 9. Resultados

```text
HTTP: 200 OK
Query: san
Response Time oficial: 331 ms
Umbral: < 1500 ms
¿Cumple umbral?: Sí
Margen frente a 1500 ms: 1169 ms
Response Size: 21738 bytes
Cantidad de resultados: 50 (solo diagnóstico)
Assertions: 6 ejecutadas (3 obligatorias + 3 auxiliares) — 6 PASS, 0 FAIL
Exit code Newman: 0
```

Se trata de **una única medición**: no se calculan promedio, mediana, percentiles ni desviación estándar. El valor de preflight (615 ms) se registra solo como trazabilidad y no participa en la evaluación.

> Nota de alcance: este caso mide latencia, no la corrección funcional de la búsqueda. La coincidencia de los resultados con el término `san` se evalúa en TC-FUN-003.

---

## 10. Comparación contra el umbral

| Métrica | Obtenido | Límite | Diferencia | Estado |
|---|---:|---:|---:|---|
| Response Time | 331 ms | 1500 ms | 1169 ms por debajo del límite | PASS |

---

## 11. Repetición de confirmación

No fue necesaria. El run oficial (331 ms) no alcanzó el umbral de 1500 ms, así que no se ejecutó ninguna repetición.

---

## 12. Evidencias

```text
postman/TC-REN-002.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-REN-002-newman.json     (reporte JSON — run oficial)
evidencias/TC-REN-002-newman.txt      (salida de consola — run oficial)
evidencias/TC-REN-002-newman.html     (reporte HTML htmlextra — run oficial)
evidencias/response-body.json         (cuerpo real — run oficial)
evidencias/preflight-1-newman.json    (preflight — 615 ms, 6/6 PASS)
evidencias/preflight-1-newman.txt
TC-REN-002_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios.

---

## 13. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman (1 iteración, 1 request, sin concurrencia),
GET https://api.openbrewerydb.org/v1/breweries/search?query=san respondió HTTP
200 OK con un Response Time de 331 ms, estrictamente menor al umbral de 1500 ms
(margen de 1169 ms). Las 6 assertions (3 obligatorias y 3 auxiliares) se
aprobaron (0 fallidas) y Newman terminó con código de salida 0.
```

---

## 14. Hallazgos

No se identificaron incumplimientos del umbral de latencia durante TC-REN-002.

---

## 15. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-002
Resultado obtenido: GET /v1/breweries/search?query=san respondió HTTP 200 con un Response Time oficial de 331 ms. El umbral definido para TC-REN-002 es < 1500 ms, por lo que CUMPLE. Margen frente al límite: 1169 ms. Se ejecutaron 6 assertions: 6 aprobadas y 0 fallidas. Exit code Newman: 0.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-002-newman.json (complementos: TC-REN-002-newman.txt, TC-REN-002-newman.html, response-body.json)
Observaciones: Medición individual end-to-end desde equipo local Windows (Newman 6.2.2, Node.js v22.15.1), 1 request sin concurrencia, query=san, el 2026-10-01 07:13 UTC. Response Size 21738 bytes; 50 resultados. Preflight previo: 615 ms (no usado para el resultado). No se requirió repetición.
```
