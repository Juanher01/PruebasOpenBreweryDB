# Informe de Ejecución — TC-REN-003

## 1. Identificación

```text
Caso: TC-REN-003
Nombre: Estabilidad bajo repetición
Tipo: Rendimiento
API: Open BreweryDB
Endpoint: GET /v1/breweries/random
Ejecuciones oficiales: 50
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T15:52:02.602Z → 15:52:18.791Z (UTC) — 2026-10-01 10:52 hora local (UTC-5)
```

> **Nota de versión del caso.** Este informe corresponde al **paquete de instrucciones actualizado** de TC-REN-003, que añade el criterio cuantitativo `P95 < 2000 ms`. La versión anterior del caso solo pedía una "desviación estándar baja", sin umbral numérico. Se ejecutó antes en esta misma sesión (2026-10-01 07:17 UTC) y resultó APROBADA por 100 % de éxito, con σ reportada como línea base. Sus artefactos ya no estaban en la carpeta al iniciar esta ejecución, pero se conservan en el historial de git (commit `0b9d9b2 Pruebas de rendimiento`). Esta ejecución es nueva y completa: **no reutiliza ningún dato de la anterior**.

---

## 2. Objetivo

Evaluar la estabilidad temporal de `GET /v1/breweries/random` mediante **50 solicitudes secuenciales**, sin concurrencia. Se verifica que las 50 respondan HTTP 200 (100 % de éxito) y que el **P95** de los 50 tiempos de respuesta, calculado por nearest-rank, sea estrictamente menor a 2000 ms. También se registran métricas descriptivas de dispersión.

---

## 3. Criterios

```text
HTTP esperado: 200
Tasa de éxito esperada: 100%
P95 esperado: < 2000 ms (estricto: 2000 ms = FAIL)
Método P95: nearest-rank — posición = ceil(0.95 × 50) = 48
Concurrencia: ninguna
```

El umbral de 2000 ms se aplica **al P95 de la muestra**, no a cada request: la colección no contiene ninguna assertion `responseTime < 2000`. La desviación estándar y el CV son **descriptivos**.

---

## 4. Ambiente

```text
Versión Newman: 6.2.2
Node.js: v22.15.1
Sistema operativo: Windows (Windows_NT 10.0.26200, x64)
Fecha/hora: 2026-10-01T15:52:02.602Z → 15:52:18.791Z (UTC)
Ubicación del runner: no verificada (equipo local del analista; zona horaria UTC-5)
Tipo de conexión: no verificado
```

Las mediciones son **end-to-end desde este equipo**. Incluyen red, DNS, TLS e infraestructura del proveedor.

---

## 5. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Endpoint: {{base_url}}/breweries/random
URL final: https://api.openbrewerydb.org/v1/breweries/random
Método: GET
Iteration Count: 50
Requests por iteración: 1
Total esperado: 50
Modo: secuencial (comportamiento estándar de Newman; sin paralelismo ni hilos)
Query Params: ninguno
Autenticación: ninguna
```

---

## 6. Procedimiento

1. **Preparación** — La carpeta solo contenía `.gitkeep` (ver nota de versión). Se crearon `postman/`, `scripts/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Rendimiento* → carpeta `TC-REN-003` → una única request *TC-REN-003 - Estabilidad bajo repetición* (`GET {{base_url}}/breweries/random`). Tiene 2 assertions obligatorias (HTTP 200 y Response Time válido), 2 auxiliares (Content-Type JSON y JSON válido) y diagnóstico por iteración. Se creó `scripts/calcular_metricas.js`, que solo lee el reporte de Newman y no hace requests. Se validaron los JSON y la sintaxis del script.
2. **Preflight** (inicio de comando 15:51:44Z UTC) — **Una sola request**: `200 OK`, 891 ms, 4/4 PASS, exit code 0. **Excluido** de las 50 mediciones, del P95 y de la tasa de éxito. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Ejecución oficial** (inicio de comando 15:51:58Z UTC; run 15:52:02.602Z → 15:52:18.791Z UTC; 16.1 s), exit code `0`:
   ```bash
   newman run postman/TC-REN-003.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-REN-003" \
     --iteration-count 50 \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-REN-003-newman.json \
     --reporter-htmlextra-export evidencias/TC-REN-003-newman.html \
     > evidencias/TC-REN-003-newman.txt 2>&1
   ```
4. **Extracción de tiempos** — `node scripts/calcular_metricas.js` filtró las 50 ejecuciones de la request oficial y extrajo iteración, HTTP y `response.responseTime` sin redondear. Escribió `evidencias/tiempos-response.json`, `evidencias/metricas.json` y `evidencias/muestra-response.json`.
5. **Cálculo de métricas** — Se contrastaron con un recálculo independiente y con los agregados de Newman (`run.timings`: media 239.08, mín 220, máx 521, s.d. 41.8152…). Todos coinciden.
6. **Evaluación de la tasa de éxito** — 50/50 HTTP 200 = 100 % → cumple.
7. **Evaluación del P95** — Valor en la posición 48 de los 50 tiempos ordenados = 259 ms; 259 < 2000 → cumple.
8. **Repetición** — **No requerida**: el run oficial no quedó RECHAZADO.

---

## 7. Validación de ejecuciones

```text
Iteraciones configuradas: 50
Iteraciones reportadas por Newman: 50
Ejecuciones observadas: 50 (cursor.iteration 0…49, una request por iteración)
Responses recibidas: 50
HTTP 200: 50
Otros HTTP: 0
Errores de red: 0
Tasa de éxito: 100%
Assertions: 200 (4 × 50) — 200 PASS, 0 FAIL
Endpoint en las 50: /v1/breweries/random, sin query params
```

---

## 8. Métricas

Fuente: `evidencias/metricas.json`. Valores redondeados a 2 decimales; el archivo conserva los valores completos.

| Métrica | Resultado |
|---|---:|
| N | 50 |
| Mínimo | 220 ms |
| Máximo | 521 ms |
| Media | 239.08 ms |
| Mediana | 230.50 ms |
| P95 (nearest-rank, posición 48) | 259 ms |
| Desviación estándar poblacional | 41.82 ms |
| Coeficiente de variación | 17.49 % |

Métodos:

- **Media** = 11954 / 50.
- **Mediana** = (posición 25 + posición 26) / 2 = (230 + 231) / 2.
- **P95** = valor ordenado en la posición ⌈0.95 × 50⌉ = 48. Las posiciones 46–50 son 255, 255, **259**, 265 y 521.
- **σ poblacional** = √(Σ(tᵢ − μ)² / N).
- **CV** = σ / μ × 100.

Serie completa de tiempos en orden de iteración (todas con HTTP 200), también en `evidencias/tiempos-response.json`:

| Iteraciones | Response Time (ms) |
|---|---|
| 1–10 | 521, 224, 228, 235, 224, 226, 232, 224, 233, 229 |
| 11–20 | 229, 220, 231, 224, 265, 230, 253, 223, 220, 222 |
| 21–30 | 231, 220, 228, 242, 250, 227, 223, 241, 227, 235 |
| 31–40 | 226, 226, 250, 242, 240, 220, 228, 259, 255, 247 |
| 41–50 | 236, 255, 231, 241, 245, 226, 235, 222, 232, 221 |

---

## 9. Evaluación de criterios

| Criterio | Esperado | Obtenido | Estado |
|---|---:|---:|---|
| Total requests | 50 | 50 | PASS |
| HTTP 200 | 50/50 | 50/50 | PASS |
| Tasa de éxito | 100 % | 100 % | PASS |
| P95 | <2000 ms | 259 ms | PASS |

---

## 10. Análisis de estabilidad

El P95 observado fue de **259 ms**, calculado mediante nearest-rank sobre 50 mediciones (posición 48), por lo que **CUMPLE** el SLO definido de <2000 ms, con un margen de 1741 ms.

La media fue **239.08 ms**, la mediana **230.50 ms**, la desviación estándar poblacional **41.82 ms** y el coeficiente de variación **17.49 %**. Estas métricas se registran como información descriptiva complementaria.

Observación descriptiva: el máximo (521 ms) corresponde a la **iteración 1**. Las 49 iteraciones restantes estuvieron entre 220 y 265 ms. Ninguna medición se excluyó del cálculo.

---

## 11. Evidencias

```text
postman/TC-REN-003.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
scripts/calcular_metricas.js               (solo lee el reporte Newman; no hace requests)
evidencias/TC-REN-003-newman.json          (reporte JSON — run oficial, 50 iteraciones)
evidencias/TC-REN-003-newman.txt           (salida de consola — run oficial)
evidencias/TC-REN-003-newman.html          (reporte HTML htmlextra — run oficial)
evidencias/tiempos-response.json           (50 mediciones: iteración, HTTP, response_time_ms, tamaño)
evidencias/metricas.json                   (métricas y evaluación de aceptación)
evidencias/muestra-response.json           (cuerpo real de la iteración 1 del run oficial)
evidencias/preflight-1-newman.json         (preflight — 1 request, 891 ms; excluido)
evidencias/preflight-1-newman.txt
TC-REN-003_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios.

---

## 12. Resultado final

```text
Estado: APROBADO

Justificación:
En un único run oficial de Newman (exit code 0) se ejecutaron exactamente 50
solicitudes secuenciales a GET /v1/breweries/random, una por iteración y sin
concurrencia. Las 50 respondieron HTTP 200: tasa de éxito del 100 %, que cumple. El
P95 de los 50 tiempos, por nearest-rank en la posición 48, fue de 259 ms,
estrictamente menor a 2000 ms, que también cumple. Las 200 assertions se aprobaron
y no hubo fallos técnicos que invalidaran la ejecución.
```

---

## 13. Hallazgos

No se identificaron incumplimientos de los criterios de TC-REN-003 (100 % HTTP 200 y P95 < 2000 ms).

---

## 14. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-003
Resultado obtenido: Se ejecutaron 50 solicitudes secuenciales a GET /v1/breweries/random. Se obtuvieron 50/50 respuestas HTTP 200, para una tasa de éxito de 100%. El P95 fue de 259 ms frente al criterio <2000 ms. La media fue 239.08 ms, la mediana 230.50 ms, la desviación estándar poblacional 41.82 ms y el CV 17.49%. Resultado: CUMPLE.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-003-newman.json (complementos: metricas.json, tiempos-response.json, TC-REN-003-newman.txt, TC-REN-003-newman.html)
Observaciones: Ejecutado con el paquete actualizado (criterio P95 < 2000 ms, nearest-rank posición 48). 1 run oficial de 50 iteraciones sin concurrencia, el 2026-10-01 15:52 UTC desde equipo local Windows con Newman 6.2.2. Mín 220 / máx 521 ms (máximo en la iteración 1). Preflight (1 request, 891 ms) excluido. No se requirió repetición. La ejecución de la versión anterior del caso se conserva en git (commit 0b9d9b2).
```
