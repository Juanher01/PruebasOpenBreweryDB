# Informe de Ejecución — TC-FUN-002

## 1. Identificación

```text
Caso de prueba: TC-FUN-002
Nombre: Consulta de cervecería mediante ID dinámico
Tipo: Funcional
API: Open BreweryDB
Endpoint principal: GET /v1/breweries/{id}
Consulta previa: GET /v1/breweries
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T05:29:08.470Z (UTC) — 2026-10-01 00:29:08 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que Open BreweryDB permite consultar una cervecería concreta mediante `GET /v1/breweries/{id}` usando un identificador válido obtenido **dinámicamente** en la misma ejecución desde `GET /v1/breweries`. Se comprobó que el detalle responde `200 OK` con un único objeto JSON (no un arreglo), que su campo `id` coincide exactamente con el solicitado y que contiene la estructura funcional básica de una cervecería (`id`, `name`, `brewery_type`).

---

## 3. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales de `api.openbrewerydb.org` en el preflight y en la ejecución oficial. |
| Disponibilidad de la API | Comprobada | Ambos endpoints respondieron `200 OK` en las dos ejecuciones. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados por Postman Runtime a través de Newman. La GUI de Postman no fue operada por el agente. |
| Colección válida | Comprobada | Validada con `JSON.parse` antes del preflight. |
| Environment válido | Comprobada | Validado con `JSON.parse`; `brewery_id` y `brewery_list_snapshot` inicialmente vacíos. |
| Sin ID fijo | Comprobada | Búsqueda de patrones UUID en la colección: 0 coincidencias. El pre-request del Paso 1 además vacía `brewery_id` antes de cada ejecución. |
| Independencia de TC-FUN-001 | Comprobada | No se leyó ni utilizó ningún archivo de `TC-FUN-001/`. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Consulta previa: GET {{base_url}}/breweries
Consulta principal: GET {{base_url}}/breweries/{{brewery_id}}
Query Params: Ninguno en ambas requests (reporte Newman: "query": [])
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Variables dinámicas: brewery_id, brewery_list_snapshot (vacías al inicio; asignadas en el Paso 1)
Número de ejecuciones: 2 (1 preflight + 1 oficial); solo la oficial determina el estado
```

---

## 5. Flujo dinámico ejecutado

```text
GET /v1/breweries                                        → 200 OK, 50 registros
        ↓
se obtiene ID = ae7b3174-8be8-4d53-a3a5-9b8240970eea      (responseData[0].id)
        ↓
GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea    → 200 OK
        ↓
respuesta.id = ae7b3174-8be8-4d53-a3a5-9b8240970eea
```

Trazabilidad verificada sobre `evidencias/TC-FUN-002-newman.json`:

| Fuente | Valor |
|---|---|
| ID del Paso 1 (`listado-previo-response.json[0].id`) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| ID en la URL del Paso 2 (request registrada por Newman) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| ID retornado (`detalle-response.json.id`) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| ¿Los tres coinciden? | **Sí** |

---

## 6. Procedimiento ejecutado

1. **Creación/preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`, `brewery_id` vacío, `brewery_list_snapshot` vacío) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-002` con dos requests en orden: Paso 1 y Paso 2. Ambos JSON se validaron y se confirmó que Newman estaba instalado.
2. **Preflight** (05:28:49Z UTC) — Se ejecutó el flujo completo con Newman: 14 assertions, 0 fallidas, exit code 0. Se comprobó que el ID se generaba en el Paso 1 y que el Paso 2 lo consumía. No hubo defectos de script, por lo que no fue necesario corregir la colección. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Consulta previa** (ejecución oficial) — `GET https://api.openbrewerydb.org/v1/breweries` → `200 OK`, 50 registros, 390 ms.
4. **Extracción del ID** — El script de tests del Paso 1 tomó `responseData[0]` y comprobó que tuviera un `id` de tipo string no vacío.
5. **Almacenamiento de variable** — `pm.environment.set("brewery_id", selectedBrewery.id)` y `pm.environment.set("brewery_list_snapshot", JSON.stringify(selectedBrewery))`.
6. **Consulta de detalle** — `GET https://api.openbrewerydb.org/v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea` → `200 OK`, 90 ms.
7. **Ejecución de assertions** — 5 en el Paso 1 y 9 en el Paso 2; 14 aprobadas, 0 fallidas; `run.failures` vacío; exit code de Newman `0`.
8. **Conservación de evidencia** — Los cuerpos de ambas respuestas se extrajeron con Node.js de `run.executions[0|1].response.stream` del reporte JSON oficial y se guardaron con indentación, sin modificar los datos.
9. **Determinación del resultado** — Se aplicaron los criterios de aprobación (sección 11).

Comando oficial:

```bash
newman run postman/TC-FUN-002.postman_collection.json \
  -e postman/OpenBreweryDB.postman_environment.json \
  --folder "TC-FUN-002" \
  -r cli,json,htmlextra \
  --reporter-json-export evidencias/TC-FUN-002-newman.json \
  --reporter-htmlextra-export evidencias/TC-FUN-002-newman.html \
  > evidencias/TC-FUN-002-newman.txt 2>&1
```

---

## 7. Aserciones ejecutadas

### Consulta previa

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | JSON válido | Sí | Sí | PASS |
| 3 | Tipo de respuesta | Array | Array | PASS |
| 4 | Registros | > 0 | 50 | PASS |
| 5 | Registro seleccionado contiene `id` (string no vacío) | Sí | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` | PASS |

### Consulta principal

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Objeto JSON único | Objeto, no arreglo | Objeto (`Array.isArray` = false) | PASS |
| 5 | Campo `id` presente | Sí | Sí | PASS |
| 6 | ID retornado = ID solicitado | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` | PASS |
| 7 | Estructura básica (`id`, `name`, `brewery_type`) | Presentes | Presentes | PASS |
| 8 | Nombre consistente listado/detalle (control complementario) | `'s` | `'s` | PASS |
| 9 | Tipo consistente listado/detalle (control complementario) | `brewpub` | `brewpub` | PASS |

---

## 8. Resultados obtenidos

```text
Registros obtenidos en consulta previa: 50
ID seleccionado: ae7b3174-8be8-4d53-a3a5-9b8240970eea
HTTP consulta previa: 200 OK
Response Time consulta previa: 390 ms

URL final solicitada: https://api.openbrewerydb.org/v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea
HTTP detalle: 200 OK
Content-Type detalle: application/json
Response Time detalle: 90 ms
Tipo de respuesta: Objeto JSON único
ID solicitado: ae7b3174-8be8-4d53-a3a5-9b8240970eea
ID retornado: ae7b3174-8be8-4d53-a3a5-9b8240970eea
Coincidencia: Sí (exacta)
Nombre retornado: 's
brewery_type retornado: brewpub
Assertions totales: 14 (5 consulta previa + 9 consulta principal)
Assertions exitosas: 14
Assertions fallidas: 0
Código de salida Newman: 0
Duración total del run: 699 ms
```

---

## 9. Muestra de la respuesta

Campos seleccionados del objeto real retornado por `GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea` (ejecución oficial):

```json
{
  "id": "ae7b3174-8be8-4d53-a3a5-9b8240970eea",
  "name": "'s",
  "brewery_type": "brewpub",
  "city": "Kronach",
  "state_province": "Bayern",
  "country": "Germany"
}
```

El cuerpo completo se conserva en `evidencias/detalle-response.json`.

---

## 10. Evidencias

```text
postman/TC-FUN-002.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-002-newman.json        (reporte JSON — ejecución oficial)
evidencias/TC-FUN-002-newman.txt         (salida de consola — ejecución oficial)
evidencias/TC-FUN-002-newman.html        (reporte HTML htmlextra — ejecución oficial)
evidencias/listado-previo-response.json  (cuerpo real de GET /v1/breweries — ejecución oficial)
evidencias/detalle-response.json         (cuerpo real de GET /v1/breweries/{id} — ejecución oficial)
evidencias/preflight-1-newman.json       (preflight — 14/14 PASS)
evidencias/preflight-1-newman.txt
TC-FUN-002_Informe.md
```

---

## 11. Resultado final

```text
Estado: APROBADO

Justificación:
En la ejecución oficial con Newman, GET /v1/breweries respondió 200 OK con un
arreglo de 50 registros, del cual se obtuvo dinámicamente el ID
ae7b3174-8be8-4d53-a3a5-9b8240970eea. Con ese mismo valor se ejecutó
GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea, que respondió 200 OK
(application/json) con un único objeto JSON cuyo id coincide exactamente con el
solicitado y que contiene id, name y brewery_type. Las 14 assertions se
aprobaron (0 fallidas) y Newman terminó con código de salida 0.
```

---

## 12. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-002.

> Observaciones (no constituyen hallazgos de TC-FUN-002):
> - El preflight y la ejecución oficial obtuvieron el mismo ID. En ambas ejecuciones el ID se obtuvo dinámicamente (el pre-request vacía `brewery_id` y el Paso 1 lo vuelve a asignar), así que la coincidencia indica que el orden por defecto del listado se mantuvo estable entre ambas ejecuciones, no que se reutilizara un valor.
> - El registro obtenido tiene como `name` el valor `'s`, que parece un nombre incompleto. TC-FUN-002 no valida la calidad del contenido de los campos, por lo que no afecta al resultado. Se deja constancia por si se quiere revisar en pruebas de contrato o calidad de datos (TC-CON).

---

## 13. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-002
Resultado obtenido: HTTP 200 OK en consulta de detalle. Se obtuvo dinámicamente el ID ae7b3174-8be8-4d53-a3a5-9b8240970eea desde GET /v1/breweries y se consultó mediante GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea. El objeto retornado presentó el mismo identificador solicitado. Se ejecutaron 14 assertions: 14 aprobadas y 0 fallidas. Tiempo de respuesta del detalle: 90 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-002-newman.json (complementos: TC-FUN-002-newman.txt, TC-FUN-002-newman.html, listado-previo-response.json, detalle-response.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 05:29 UTC. Consulta previa: 200 OK, 50 registros, 390 ms. Preflight previo 14/14 PASS. Sin hallazgos. El registro consultado tiene name = "'s" (dato real de la API, fuera del alcance de TC-FUN-002).
```
