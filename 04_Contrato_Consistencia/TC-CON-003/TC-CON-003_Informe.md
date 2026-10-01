# Informe de Ejecución — TC-CON-003

## 1. Identificación

```text
Caso: TC-CON-003
Nombre: Consistencia en listado vs detalle
Tipo: Contrato y Consistencia
API: Open BreweryDB
Endpoints:
- GET /v1/breweries
- GET /v1/breweries/{id}
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2 + Chai (pm.expect)
Fecha/hora: 2026-10-01T06:49:32.281Z (UTC) — 2026-10-01 01:49:32 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que Open BreweryDB devuelve la **misma representación** de un recurso en el listado (`GET /v1/breweries`) y en el detalle (`GET /v1/breweries/{id}`). Para ello se toma dinámicamente un registro del listado, se guarda su objeto completo como snapshot y se compara con el objeto devuelto por el detalle consultado con el mismo `id`, dentro del mismo run.

---

## 3. Criterio de consistencia

```text
El objeto del detalle debe coincidir completamente con el objeto
del mismo ID obtenido en el listado.
```

- La assertion principal usa **igualdad profunda** (`pm.expect(detailResponse).to.deep.equal(listSnapshot)`) sobre los objetos completos tal como los devuelve la API, sin normalizar valores ni eliminar o agregar propiedades.
- El **orden de las propiedades no se considera** (la igualdad profunda de Chai compara por clave).
- Como apoyo, se comprueba que ambos objetos tengan exactamente el mismo conjunto de propiedades. Un diagnóstico campo a campo identifica valor y tipo de cada diferencia; solo ordena las claves para visualizarlas y no altera ningún valor.
- AJV no se utilizó: este caso compara dos representaciones y no valida un schema (el paquete lo indica como no obligatorio).

---

## 4. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en las 4 requests (preflight y oficial). |
| Disponibilidad de la API | Comprobada | `200 OK` en las 4 requests. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección y environment válidos | Comprobada | Validados con `JSON.parse` antes del preflight; `brewery_id` y `list_brewery_snapshot` inicialmente vacíos. |
| Sin IDs fijos | Comprobada | Búsqueda de patrones UUID en la colección: 0 coincidencias. El pre-request del Paso 1 vacía `brewery_id` y `list_brewery_snapshot` antes de cada run. |
| Independencia de otros casos | Comprobada | No se leyó ni reutilizó ningún archivo de otros casos (incluidos TC-FUN-009, TC-CON-001 y TC-CON-002). |

---

## 5. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Endpoint listado: GET {{base_url}}/breweries   (sin parámetros)
Endpoint detalle: GET {{base_url}}/breweries/{{brewery_id}}
ID obtenido: ae7b3174-8be8-4d53-a3a5-9b8240970eea
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Variables dinámicas: brewery_id, list_brewery_snapshot (vacías al inicio; asignadas en el Paso 1)
Número de ejecuciones: 2 runs (1 preflight + 1 oficial), cada uno con 2 requests; el estado se determina con el run oficial
```

> Nota: el ID coincide con el de TC-CON-001 y TC-CON-002 porque, en los tres casos, se obtuvo dinámicamente como primer elemento del listado por defecto, cuyo orden se mantuvo estable. No se copió de otros casos.

---

## 6. Flujo ejecutado

```text
GET /v1/breweries                                         → 200 OK, 50 registros (350 ms)
        ↓
seleccionar registro → listResponse[0]
        ↓
guardar snapshot completo → list_brewery_snapshot (16 propiedades)
        ↓
ID = ae7b3174-8be8-4d53-a3a5-9b8240970eea
        ↓
GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea    → 200 OK, 16 propiedades (84 ms)
        ↓
comparación profunda → igual (0 diferencias)
```

Trazabilidad del ID (verificada sobre `evidencias/TC-CON-003-newman.json` y `evidencias/comparacion.json`):

| Eslabón | Valor |
|---|---|
| ID en el elemento del listado (`elemento-listado-seleccionado.json`) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| `brewery_id` almacenado (log del Paso 1: *ID seleccionado*) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| ID usado en la URL del detalle (request registrada por Newman) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| ID retornado por el detalle (`detalle-response.json`) | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` |
| ¿Los cuatro coinciden? | **Sí** |

---

## 7. Procedimiento

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`, `brewery_id` vacío, `list_brewery_snapshot` vacío) y la colección *Open BreweryDB - Contrato y Consistencia* → carpeta `TC-CON-003` → Paso 1 *Obtener registro desde listado* y Paso 2 *Consultar y comparar detalle*. La colección se generó con un script Node auxiliar.
2. **Preflight** (06:49:12Z UTC) — Flujo completo: el ID se obtuvo dinámicamente, el snapshot se guardó completo (16 campos), el detalle se consultó con el mismo ID, la igualdad profunda se evaluó y el diagnóstico reportó 0 diferencias. 14 assertions, 0 fallidas, exit code 0. No hubo defectos de script. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Selección** (run oficial) — `GET /v1/breweries` → `200 OK`, 50 registros; se seleccionó `listResponse[0]`.
4. **Snapshot** — `pm.environment.set("list_brewery_snapshot", JSON.stringify(selectedBrewery))` sin agregar ni eliminar propiedades. El log registra las 16 claves del objeto.
5. **Detalle** — `GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea` → `200 OK`, `application/json`, 84 ms.
6. **Assertions** — 6 en el Paso 1 y 8 en el Paso 2 (4 generales, snapshot disponible, ID, igualdad profunda y mismas propiedades): 14 aprobadas, 0 fallidas; `run.failures` vacío; exit code `0`.
7. **Evidencias** — Los cuerpos del listado y del detalle se extrajeron de `run.executions[0|1].response.stream` del reporte JSON oficial. El elemento seleccionado es `listado[0]` de ese mismo cuerpo. Se guardaron solo con indentación. `comparacion.json` se calculó a partir de esos cuerpos con la misma lógica de diagnóstico del Paso 2 e incluye el resultado real de las assertions de Newman.

Comando oficial:

```bash
newman run postman/TC-CON-003.postman_collection.json \
  -e postman/OpenBreweryDB.postman_environment.json \
  --folder "TC-CON-003" \
  -r cli,json,htmlextra \
  --reporter-json-export evidencias/TC-CON-003-newman.json \
  --reporter-htmlextra-export evidencias/TC-CON-003-newman.html \
  > evidencias/TC-CON-003-newman.txt 2>&1
```

---

## 8. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-CON-003-newman.json`).

### Paso 1 — Listado

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| PRE-1 | HTTP | 200 | 200 OK | PASS |
| PRE-2 | Content-Type | JSON | `application/json` | PASS |
| PRE-3 | JSON válido | Sí | Sí | PASS |
| PRE-4 | Tipo de respuesta | Array | Array | PASS |
| PRE-5 | Registros | > 0 | 50 | PASS |
| PRE-6 | Registro seleccionado con `id` válido | Objeto con `id` string no vacío | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` | PASS |

### Paso 2 — Detalle y consistencia

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Raíz | Object | Object (`Array.isArray` = false) | PASS |
| 5 | Snapshot del listado disponible | Objeto con `id` | Objeto con `id`, 16 propiedades | PASS |
| 6 | **ID coincide** | `id` del detalle = `brewery_id` = `id` del snapshot | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` en los tres | PASS |
| 7 | **Igualdad profunda** | `detailResponse` deep equal `listSnapshot` | Iguales | PASS |
| 8 | **Mismas propiedades** | Mismo conjunto de claves | 16 = 16, mismo conjunto | PASS |

---

## 9. Resultados

```text
Listado:
URL: https://api.openbrewerydb.org/v1/breweries
HTTP: 200 OK
Response Time: 350 ms
Cantidad: 50
ID seleccionado: ae7b3174-8be8-4d53-a3a5-9b8240970eea
Campos del snapshot: 16

Detalle:
URL: https://api.openbrewerydb.org/v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea
HTTP: 200 OK
Content-Type: application/json
Response Time: 84 ms
ID retornado: ae7b3174-8be8-4d53-a3a5-9b8240970eea
Campos del detalle: 16

Comparación:
ID coincide: Sí
Mismas propiedades: Sí
Igualdad profunda: Sí
Diferencias: ninguna
Cantidad de diferencias: 0

Assertions: 14 (6 Paso 1 + 8 Paso 2)
PASS: 14
FAIL: 0
Exit code: 0
Resultado global: Exitoso
```

---

## 10. Objeto del listado seleccionado

Contenido real completo de `evidencias/elemento-listado-seleccionado.json` (`listado[0]` del run oficial):

```json
{
  "id": "ae7b3174-8be8-4d53-a3a5-9b8240970eea",
  "name": "'s",
  "brewery_type": "brewpub",
  "address_1": "Friesener Straße 1",
  "address_2": null,
  "address_3": null,
  "city": "Kronach",
  "state_province": "Bayern",
  "postal_code": "96317",
  "country": "Germany",
  "longitude": 11.327765,
  "latitude": 50.241246,
  "phone": "+49 9261 628000",
  "website_url": "http://www.antla.de",
  "state": "Bayern",
  "street": "Friesener Straße 1"
}
```

---

## 11. Objeto del detalle

Contenido real completo de `evidencias/detalle-response.json` (run oficial):

```json
{
  "id": "ae7b3174-8be8-4d53-a3a5-9b8240970eea",
  "name": "'s",
  "brewery_type": "brewpub",
  "address_1": "Friesener Straße 1",
  "address_2": null,
  "address_3": null,
  "city": "Kronach",
  "state_province": "Bayern",
  "postal_code": "96317",
  "country": "Germany",
  "longitude": 11.327765,
  "latitude": 50.241246,
  "phone": "+49 9261 628000",
  "website_url": "http://www.antla.de",
  "state": "Bayern",
  "street": "Friesener Straße 1"
}
```

---

## 12. Comparación campo a campo

No se identificaron diferencias entre el objeto del listado y el detalle.

Se compararon las 16 propiedades de la unión de claves de ambos objetos: `address_1`, `address_2`, `address_3`, `brewery_type`, `city`, `country`, `id`, `latitude`, `longitude`, `name`, `phone`, `postal_code`, `state`, `state_province`, `street` y `website_url`. Coinciden en valor, tipo y nulabilidad (`address_2` y `address_3` son `null` en ambos; `latitude` y `longitude` son number en ambos). El orden de las claves también es idéntico en los dos objetos, aunque el criterio no lo exige. Detalle en `evidencias/comparacion.json` (`difference_count: 0`, `differences: []`).

---

## 13. Evidencias

```text
postman/TC-CON-003.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-CON-003-newman.json                (reporte JSON — run oficial)
evidencias/TC-CON-003-newman.txt                 (salida de consola — run oficial)
evidencias/TC-CON-003-newman.html                (reporte HTML htmlextra — run oficial)
evidencias/listado-response.json                 (cuerpo real de GET /v1/breweries — run oficial)
evidencias/elemento-listado-seleccionado.json    (listado[0] — run oficial)
evidencias/detalle-response.json                 (cuerpo real de GET /v1/breweries/{id} — run oficial)
evidencias/comparacion.json                      (comparación calculada sobre los cuerpos oficiales)
evidencias/preflight-1-newman.json               (preflight — 14/14 PASS)
evidencias/preflight-1-newman.txt
TC-CON-003_Informe.md
```

La carpeta también contenía un archivo `.gitkeep` vacío creado antes de esta ejecución. No forma parte de la evidencia y se conservó sin cambios.

---

## 14. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman, GET /v1/breweries respondió 200 OK con un arreglo
JSON de 50 registros. Se seleccionó dinámicamente listado[0]
(id ae7b3174-8be8-4d53-a3a5-9b8240970eea) y se guardó como snapshot completo
(16 propiedades). GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea
respondió 200 OK (application/json) con un objeto JSON de 16 propiedades cuyo id
coincide con el solicitado y con el del snapshot. El objeto del detalle es
profundamente igual al del listado: mismo conjunto de propiedades y 0
diferencias de valor, tipo o nulabilidad. Las 14 assertions se aprobaron (0
fallidas) y Newman terminó con código de salida 0. El preflight dio el mismo
resultado.
```

---

## 15. Hallazgos

No se identificaron inconsistencias entre listado y detalle durante TC-CON-003.

---

## 16. Registro para Excel

### Registro para Excel

```text
ID: TC-CON-003
Resultado obtenido: HTTP 200 OK en listado y detalle. Se obtuvo dinámicamente el ID ae7b3174-8be8-4d53-a3a5-9b8240970eea desde GET /v1/breweries y se consultó mediante GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea. El objeto del detalle coincide profundamente con el objeto del mismo ID en el listado. Se compararon 16 propiedades y se identificaron 0 diferencias. Se ejecutaron 14 assertions: 14 aprobadas y 0 fallidas. Tiempo de respuesta del detalle: 84 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-CON-003-newman.json (complementos: TC-CON-003-newman.txt, TC-CON-003-newman.html, elemento-listado-seleccionado.json, detalle-response.json, comparacion.json, listado-response.json)
Observaciones: Igualdad profunda sobre el objeto completo, sin normalizar valores (el orden de propiedades no influye). Listado: 200 OK, 50 registros, 350 ms. Mismo conjunto de 16 propiedades. Preflight previo 14/14 PASS. Ejecución con Newman 6.2.2 el 2026-10-01 06:49 UTC; exit code 0. Sin hallazgos.
```
