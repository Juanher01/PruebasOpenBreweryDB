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
Fecha/hora: 2026-10-01T07:17:10.030Z → 2026-10-01T07:17:27.251Z (UTC) — 2026-10-01 02:17 hora local (UTC-5)
```

---

## 2. Objetivo

Evaluar la estabilidad temporal de `GET /v1/breweries/random` mediante **50 solicitudes secuenciales**, sin concurrencia. Se comprueba que las 50 respondan HTTP 200 (100 % de éxito) y se calcula, a partir de los 50 tiempos reales, la desviación estándar junto con métricas descriptivas que ayudan a interpretar la dispersión.

---

## 3. Criterios del caso

```text
HTTP esperado: 200 OK
Tasa de éxito esperada: 100%
Desviación estándar esperada: baja
Umbral numérico para desviación estándar: no definido en el plan
Concurrencia: ninguna
```

No se aplicó ningún umbral individual de latencia: las assertions no contienen `below(X)`.

---

## 4. Ambiente de medición

```text
Versión Newman: 6.2.2 (CLI) sobre Node.js v22.15.1
Sistema operativo: Windows (Windows_NT 10.0.26200, x64)
Fecha/hora: 2026-10-01T07:17:10.030Z → 07:17:27.251Z (UTC)
Ubicación del runner: no verificada (equipo local del analista; zona horaria UTC-5)
Tipo de conexión: no verificado
```

Las mediciones son **end-to-end desde este equipo**. Incluyen conectividad del cliente, DNS, TLS, latencia de red e infraestructura del proveedor.

---

## 5. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Endpoint: {{base_url}}/breweries/random
URL final: https://api.openbrewerydb.org/v1/breweries/random
Método: GET
Iteration Count: 50
Requests por iteración: 1
Total esperado de requests: 50
Modo de ejecución: secuencial (comportamiento estándar de Newman: una iteración tras otra; sin --delay-request, sin paralelismo ni hilos)
Query Params: ninguno
Autenticación: ninguna
Headers personalizados / Body: ninguno
```

---

## 6. Procedimiento

1. **Preparación** — Se crearon `postman/`, `scripts/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Rendimiento* → carpeta `TC-REN-003` → una única request *TC-REN-003 - Estabilidad bajo repetición* (`GET {{base_url}}/breweries/random`). Tiene 2 assertions obligatorias, 2 auxiliares (Content-Type JSON y JSON válido; no se valida objeto/arreglo) y diagnóstico por iteración. Se creó `scripts/calcular_metricas.js`, que solo lee el reporte de Newman. Los JSON y el script se validaron.
2. **Preflight** (inicio de comando 07:16:58Z UTC) — **Una sola request** (1 iteración): `200 OK`, 784 ms, 4/4 PASS, exit code 0. Confirmó conectividad, endpoint, Newman, assertions y registro del Response Time. **No forma parte de la muestra oficial** y se conserva aparte. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Run oficial con 50 iteraciones** (07:17:10.030Z → 07:17:27.251Z UTC; duración total 17.2 s), exit code `0`:
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
4. **Extracción de 50 tiempos** — `node scripts/calcular_metricas.js` leyó `evidencias/TC-REN-003-newman.json`, filtró las ejecuciones de la request oficial (50) y extrajo iteración, HTTP y `response.responseTime` sin redondear. Escribió `evidencias/tiempos-response.json`, `evidencias/metricas.json` y `evidencias/muestra-response.json` (cuerpo real de la iteración 1).
5. **Cálculo de métricas** — N, mínimo, máximo, media, mediana, desviación estándar **poblacional**, P95 (**nearest-rank**) y CV. Se verificaron con un recálculo independiente y contra los agregados del propio Newman (`run.timings`: media 260.7, mín 217, máx 1032, s.d. 118.8468…). Todos coinciden.
6. **Comprobación del 100 % de éxito** — 50/50 respuestas con HTTP 200.
7. **Interpretación de la desviación estándar** — Se reporta el valor observado sin aplicar umbral, porque el plan no define uno (sección 11).
8. **Repetición** — **No requerida**: la tasa de éxito fue 100 %.

---

## 7. Validación de las 50 ejecuciones

```text
Iteraciones configuradas: 50
Iteraciones reportadas por Newman: 50
Ejecuciones observadas de la request: 50 (cursor.iteration 0…49, una por iteración)
Responses recibidas: 50
HTTP 200: 50
Otros HTTP: 0
Errores de red: 0
Tasa de éxito: 100%
Assertions: 200 ejecutadas (4 por iteración × 50) — 200 PASS, 0 FAIL
Endpoint en las 50 ejecuciones: /v1/breweries/random, sin query params
```

---

## 8. Métricas de tiempo

Calculadas sobre las 50 mediciones oficiales (fuente: `evidencias/metricas.json`). Los valores se muestran redondeados a 2 decimales; `metricas.json` conserva los valores completos.

| Métrica | Resultado |
|---|---:|
| N | 50 |
| Mínimo | 217 ms |
| Máximo | 1032 ms |
| Media | 260.70 ms |
| Mediana | 228.50 ms |
| Desviación estándar poblacional | 118.85 ms |
| P95 (nearest-rank, posición 48) | 353 ms |
| Coeficiente de variación | 45.59 % |

Métodos:

- **Media** = 13035 / 50.
- **Mediana** = (valor 25 + valor 26) / 2 = (228 + 229) / 2.
- **σ poblacional** = √(Σ(tᵢ − μ)² / N).
- **P95 nearest-rank**: posición ⌈0.95 × 50⌉ = 48 en el conjunto ordenado.
- **CV** = σ / μ × 100.

---

## 9. Serie completa de tiempos

Las 50 mediciones, en orden de iteración (todas con HTTP 200), también en `evidencias/tiempos-response.json`:

| Iteraciones | Response Time (ms) |
|---|---|
| 1–10 | 456, 224, 220, 238, 237, 222, 221, 220, 219, 227 |
| 11–20 | 224, 226, 220, 231, 231, 226, 222, 294, 227, 229 |
| 21–30 | 225, 226, 246, 225, 220, 226, 245, 218, 219, 221 |
| 31–40 | 228, 229, 231, 240, 223, 229, 230, 231, 353, 323 |
| 41–50 | 311, 296, 331, 318, 1032, 240, 230, 225, 233, 217 |

---

## 10. Resultado de éxito

```text
Éxitos HTTP 200: 50/50
Tasa de éxito: 100%
Esperado: 100%
Estado del criterio: CUMPLE
```

---

## 11. Análisis de estabilidad

La desviación estándar poblacional observada fue de **118.85 ms** para las 50 mediciones oficiales. La media fue **260.70 ms**, la mediana **228.50 ms** y el P95 **353 ms**. El coeficiente de variación observado fue **45.59 %**.

El plan de pruebas describe la desviación esperada como "baja", pero no establece un umbral numérico. Por ello, estas métricas se reportan como **línea base de estabilidad** y no se aplica un límite arbitrario para clasificarlas.

Observaciones descriptivas, sin juicio de umbral:

- 40 de las 50 mediciones (80 %) están entre 217 y 246 ms.
- La dispersión se concentra en pocas iteraciones: la **iteración 45 (1032 ms)** es la única por encima de media + 2σ (≈ 498 ms); la iteración 1 registró 456 ms; las iteraciones 39–44 estuvieron entre 296 y 353 ms.
- La diferencia entre media (260.70 ms) y mediana (228.50 ms) refleja ese sesgo hacia valores altos. Ninguna iteración se excluyó del cálculo.
- Como la medición es end-to-end, no se puede atribuir la variabilidad exclusivamente al servidor ni a la red del cliente.

---

## 12. Iteraciones no exitosas

No se registraron iteraciones no exitosas.

---

## 13. Evidencias

```text
postman/TC-REN-003.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
scripts/calcular_metricas.js               (script auxiliar; solo lee el reporte Newman, no hace requests)
evidencias/TC-REN-003-newman.json          (reporte JSON — run oficial, 50 iteraciones)
evidencias/TC-REN-003-newman.txt           (salida de consola — run oficial)
evidencias/TC-REN-003-newman.html          (reporte HTML htmlextra — run oficial)
evidencias/tiempos-response.json           (50 mediciones: iteración, HTTP, response_time_ms, tamaño)
evidencias/metricas.json                   (métricas calculadas)
evidencias/muestra-response.json           (cuerpo real de la iteración 1 del run oficial)
evidencias/preflight-1-newman.json         (preflight — 1 request, 784 ms; excluido de la muestra)
evidencias/preflight-1-newman.txt
TC-REN-003_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios.

---

## 14. Resultado final

```text
Estado: APROBADO

Justificación:
Se completaron exactamente 50 ejecuciones secuenciales de
GET /v1/breweries/random en un único run oficial de Newman (exit code 0). Las
50 obtuvieron HTTP 200, con una tasa de éxito del 100 %, que es el criterio
cuantificable del caso. Se obtuvieron 50 tiempos válidos, las 200 assertions se
aprobaron y no hubo fallos técnicos de la automatización. La desviación estándar
observada fue de 118.85 ms. El plan no define un umbral numérico para
clasificarla como "baja", por lo que se reporta como métrica observada y no se
aplica un límite inventado.
```

---

## 15. Hallazgos

No se identificaron fallos de disponibilidad durante las 50 ejecuciones de TC-REN-003.

> Observación (no es hallazgo): la variabilidad de latencia se concentró en pocas iteraciones, con un máximo de 1032 ms en la iteración 45 (ver sección 11). Se deja como línea base por si el plan llega a definir un umbral cuantitativo de estabilidad. El body de `/random` no se evaluó aquí; su forma de respuesta corresponde a TC-FUN-004.

---

## 16. Registro para Excel

### Registro para Excel

```text
ID: TC-REN-003
Resultado obtenido: Se ejecutaron 50 solicitudes secuenciales a GET /v1/breweries/random. Se obtuvieron 50/50 respuestas HTTP 200, para una tasa de éxito de 100%. Los tiempos observados fueron: mínimo 217 ms, máximo 1032 ms, media 260.70 ms, mediana 228.50 ms, desviación estándar poblacional 118.85 ms y P95 353 ms. El plan no define un umbral numérico para clasificar la desviación estándar como "baja", por lo que el valor se registra como línea base sin aplicar un límite arbitrario. Newman terminó con exit code 0.
Estado: APROBADO
Evidencia principal: evidencias/TC-REN-003-newman.json (complementos: metricas.json, tiempos-response.json, TC-REN-003-newman.txt, TC-REN-003-newman.html)
Observaciones: 1 run oficial de 50 iteraciones (1 request por iteración, sin concurrencia), el 2026-10-01 07:17 UTC desde equipo local Windows con Newman 6.2.2. CV 45.59 %; P95 por nearest-rank (posición 48). Máximo puntual de 1032 ms en la iteración 45. Preflight (1 request, 784 ms) excluido de la muestra. No se requirió repetición.
```
