# Informe de Ejecución — TC-FUN-001

## 1. Identificación

```text
Caso de prueba: TC-FUN-001
Nombre: Listado general de cervecerías
Tipo: Funcional
API: Open BreweryDB
Endpoint: GET /v1/breweries
Herramientas: Postman (formato de colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora de ejecución: 2026-10-01T03:19:28.334Z (UTC) — 2026-09-30 22:19:28 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que el endpoint público `GET /v1/breweries` de Open BreweryDB, invocado sin parámetros (paginación por defecto), responde con HTTP `200 OK` y un cuerpo JSON válido de tipo arreglo, no vacío, cuyos elementos son objetos de cervecerías, sin errores HTTP ni fallos de ejecución.

---

## 3. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman alcanzó `api.openbrewerydb.org` en las tres ejecuciones (respuestas HTTP reales recibidas). |
| Disponibilidad de la API | Comprobada | La API respondió `200 OK` en las tres ejecuciones. |
| Postman operativo | Parcial | Postman Desktop está instalado en el equipo (`%LOCALAPPDATA%\Postman`). La colección y el environment se crearon en formato Postman v2.1 y son importables. La ejecución en la interfaz gráfica de Postman **no** fue realizada por el agente (no puede operar la GUI); el preflight se ejecutó con el mismo motor (Postman Runtime) vía Newman. Ver sección 5. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2` (Node.js v22.15.1). Reporter `newman-reporter-htmlextra@1.23.1` disponible. |
| Environment cargado | Comprobada | `OpenBreweryDB.postman_environment.json` cargado con `-e`; la URL resuelta fue `https://api.openbrewerydb.org/v1/breweries`. |
| Colección disponible | Comprobada | `TC-FUN-001.postman_collection.json` validada como JSON y ejecutada con `--folder "TC-FUN-001"`. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable de environment {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries  →  https://api.openbrewerydb.org/v1/breweries
Query Params: Ninguno (lista de query vacía en el reporte Newman: "query": [])
Autenticación: Ninguna
Headers personalizados: Ninguno
Body: Ninguno
Número de ejecuciones: 3 (2 preflight + 1 oficial); la ejecución oficial es la única que determina el estado
```

**No se enviaron parámetros explícitos de paginación** (`page`, `per_page` ni ningún otro). La respuesta corresponde a la paginación por defecto del servicio.

---

## 5. Procedimiento ejecutado

1. **Preparación** — Se creó la estructura `postman/` y `evidencias/`; se generaron el environment (`base_url`) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-001` → request *TC-FUN-001 - Listado general de cervecerías* (`GET {{base_url}}/breweries`) con las 6 assertions obligatorias y registro por consola de métricas de ejecución.
2. **Preflight** — Al no ser posible operar la GUI de Postman desde el agente, el preflight se realizó con Newman (Postman Runtime):
   - **Preflight 1** (03:19:04Z UTC): la API respondió `200 OK, 22.11kB, 536ms`, pero el script de test falló con `SyntaxError: Identifier 'data' has already been declared`. Causa: `data` es un identificador global reservado en el sandbox de Postman. Es un **defecto del script de prueba**, no del endpoint. Se ejecutaron 0 assertions. Evidencia conservada en `evidencias/preflight-1-script-error-newman.*`.
   - **Corrección**: se renombró la variable local `data` → `responseData`. No se modificó ninguna condición, valor esperado, endpoint ni método.
   - **Preflight 2** (03:19:14Z UTC): `200 OK, 22.1kB, 329ms`, 6 assertions ejecutadas, 0 fallidas, 50 registros. Evidencia en `evidencias/preflight-2-newman.*`.
3. **Ejecución Newman oficial** (inicio de comando 03:19:24Z UTC; run 03:19:28.334Z → 03:19:28.774Z UTC):
   ```bash
   newman run postman/TC-FUN-001.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-001" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-001-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-001-newman.html \
     > evidencias/TC-FUN-001-newman.txt 2>&1
   ```
   Código de salida de Newman: `0`.
4. **Captura de respuesta** — El cuerpo de respuesta se extrajo con Node.js del campo `run.executions[0].response.stream` del reporte `TC-FUN-001-newman.json` (es decir, la respuesta real de la ejecución oficial) y se guardó en `evidencias/response-body.json`. Solo se aplicó indentación para legibilidad; el contenido no fue alterado.
5. **Análisis de assertions** — Se revisaron los resultados en consola y en el reporte JSON: 6 ejecutadas, 6 PASS, 0 FAIL; `run.failures` vacío.
6. **Determinación del estado** — Se aplicaron los criterios de aprobación del caso (sección 9).

---

## 6. Aserciones ejecutadas

Valores de la ejecución oficial (`evidencias/TC-FUN-001-newman.json`).

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí (`pm.response.json()` no lanzó excepción) | PASS |
| 4 | Tipo de respuesta | Array | Array | PASS |
| 5 | Registros | > 0 | 50 | PASS |
| 6 | Elementos | Objetos | 50 de 50 elementos son objetos | PASS |

---

## 7. Resultados obtenidos

```text
Fecha/hora: 2026-10-01T03:19:28.334Z (UTC)
URL utilizada: https://api.openbrewerydb.org/v1/breweries
Método HTTP: GET
HTTP obtenido: 200 OK
Response Time: 323 ms
Tamaño de respuesta: 20731 bytes (~20.73 kB de datos recibidos; 22.1 kB según Newman incluyendo cabeceras)
Cantidad de registros: 50
Assertions ejecutadas: 6
Assertions exitosas: 6
Assertions fallidas: 0
Duración total del run: 440 ms
Resultado global: Sin fallos (exit code 0)
```

---

## 8. Evidencias

```text
postman/TC-FUN-001.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-001-newman.json            (reporte JSON — ejecución oficial)
evidencias/TC-FUN-001-newman.txt             (salida de consola — ejecución oficial)
evidencias/TC-FUN-001-newman.html            (reporte HTML htmlextra — ejecución oficial)
evidencias/response-body.json                (cuerpo real de la ejecución oficial)
evidencias/preflight-1-script-error-newman.json  (preflight 1 — error de script)
evidencias/preflight-1-script-error-newman.txt
evidencias/preflight-2-newman.json               (preflight 2 — correcto)
evidencias/preflight-2-newman.txt
```

---

## 9. Resultado final

```text
Estado: APROBADO

Justificación:
En la ejecución oficial con Newman, GET https://api.openbrewerydb.org/v1/breweries
(sin parámetros de paginación) respondió HTTP 200 OK con Content-Type
application/json. El cuerpo se interpretó como JSON válido de tipo Array con
50 elementos, todos objetos. Las 6 assertions obligatorias de TC-FUN-001 se
ejecutaron y aprobaron (0 fallidas). El resultado coincide con el preflight 2.
```

---

## 10. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-001.

> Nota (no es hallazgo del servicio): el preflight 1 falló por un error del script de prueba (`data` es un identificador reservado en el sandbox de Postman). Se corrigió renombrando la variable sin cambiar la lógica de ninguna assertion; la evidencia de ese fallo se conserva. Queda pendiente, si se requiere, la ejecución manual de la request desde la GUI de Postman por parte del analista.

---

## 11. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-001
Resultado obtenido: HTTP 200 OK. Respuesta JSON (application/json) tipo Array con 50 registros, todos objetos, usando paginación por defecto (sin query params). Se ejecutaron 6 assertions: 6 aprobadas y 0 fallidas. Tiempo de respuesta: 323 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-001-newman.json (complementos: TC-FUN-001-newman.txt, TC-FUN-001-newman.html, response-body.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 03:19 UTC. Preflight realizado con Newman; el primero falló por error del script (variable reservada 'data'), corregido sin alterar la lógica. Sin hallazgos en el servicio.
```
