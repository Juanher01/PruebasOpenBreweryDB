# Informe de Ejecución — TC-CON-002

## 1. Identificación

```text
Caso: TC-CON-002
Nombre: Validación de tipos de datos
Tipo: Contrato y Consistencia
API: Open BreweryDB
Endpoint: GET /v1/breweries/{id}
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2 + AJV/JSON Schema (draft-07) + Chai (pm.expect)
Fecha/hora: 2026-10-01T06:46:54.229Z (UTC) — 2026-10-01 01:46:54 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que la representación JSON de una cervecería individual (`GET /v1/breweries/{id}`, con un ID obtenido dinámicamente) respeta el contrato de **tipos de datos** de TC-CON-002. `id` y `name` deben ser String; `latitude` y `longitude` deben ser Number o Null. No se aceptan cadenas numéricas como números ni la cadena vacía como `null`, y no se imponen rangos geográficos ni otras restricciones no definidas.

---

## 3. Contrato evaluado

```text
id        → String
name      → String
latitude  → Number/Null
longitude → Number/Null
```

Reglas aplicadas:

- `0` y los valores negativos son números válidos. Las assertions no usan truthiness: comparan con `=== null` y `typeof === "number"` más `Number.isFinite`.
- `null` es válido para `latitude` y `longitude`.
- `"0"`, `"41.40338"` y `""` son String, así que **no** cumplen Number/Null.
- Sin `additionalProperties: false` y sin `minimum`, `maximum`, `pattern`, `minLength` ni `format`.

---

## 4. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en las 4 requests (preflight y oficial). |
| Disponibilidad de la API | Comprobada | `200 OK` en las 4 requests. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2` (postman-sandbox 4.7.1); reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección, environment y schema válidos | Comprobada | Los tres archivos se validaron con `JSON.parse` antes del preflight. |
| AJV disponible en el runtime | Comprobada | `require("ajv")` se resolvió en el sandbox; el log registra `AJV ejecutado: Sí` en el preflight y en el run oficial. |
| Sin ID fijo | Comprobada | Búsqueda de patrones UUID en la colección: 0 coincidencias. El pre-request del Paso 1 vacía `brewery_id` antes de cada run. |
| Independencia de otros casos | Comprobada | No se leyó ni reutilizó ningún archivo de otros casos (incluido TC-CON-001). |

---

## 5. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Consulta previa: GET {{base_url}}/breweries   (sin parámetros; solo preparación de datos)
Endpoint detalle: GET {{base_url}}/breweries/{{brewery_id}}
ID obtenido: ae7b3174-8be8-4d53-a3a5-9b8240970eea
URL final: /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 2 runs (1 preflight + 1 oficial), cada uno con 2 requests; el estado se determina con el run oficial
```

**Origen dinámico del ID:** `brewery_id` inicia vacío en el environment y el pre-request del Paso 1 lo vacía de nuevo. El script de tests del Paso 1 lo asigna desde `listResponse[0].id`. En el run oficial, el `id` del primer elemento de `evidencias/listado-previo-response.json`, el ID de la URL del Paso 2 y el `id` de `evidencias/detalle-response.json` son el mismo valor: `ae7b3174-8be8-4d53-a3a5-9b8240970eea`.

> Nota: el ID coincide con el usado en TC-CON-001 porque, en ambos casos, se obtuvo dinámicamente como primer elemento del listado por defecto, cuyo orden se mantuvo estable. No se copió ni leyó de TC-CON-001.

---

## 6. Procedimiento

1. **Preparación** — Se crearon `postman/`, `schemas/` y `evidencias/`. Se escribió el JSON Schema y se generó la colección con un script Node auxiliar que **lee el schema del archivo y lo incrusta tal cual** en el script de tests del Paso 2. Colección *Open BreweryDB - Contrato y Consistencia* → carpeta `TC-CON-002` → Paso 1 *Obtener ID válido* y Paso 2 *Validar tipos de datos*.
2. **Preflight** (06:46:38Z UTC) — Flujo completo: ID obtenido dinámicamente, detalle consultado con ese ID y tipos detectados `string`, `string`, `number`, `number`. AJV se ejecutó realmente (`PASS`, errores `[]`). 14 assertions, 0 fallidas, exit code 0. No hubo defectos de script. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Obtención dinámica del ID** (run oficial) — `GET /v1/breweries` → `200 OK`, 50 registros, 327 ms; `listResponse[0].id` = `ae7b3174-8be8-4d53-a3a5-9b8240970eea`.
4. **Consulta de detalle** — `GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea` → `200 OK`, `application/json`, 86 ms.
5. **AJV** — `new Ajv({ allErrors: true }).compile(contractSchema)` aplicado a `detailResponse`: válido, sin errores.
6. **Assertions** — 5 en el Paso 1 y 9 en el Paso 2 (4 generales, 4 de tipos y 1 de schema): 14 aprobadas, 0 fallidas; `run.failures` vacío; exit code `0`.
7. **Evidencias** — Los cuerpos del listado y del detalle se extrajeron de `run.executions[0|1].response.stream` del reporte JSON oficial y se guardaron solo con indentación.
8. **Verificación auxiliar de la lógica** (fuera del run, sin llamar a la API) — Se aplicaron el mismo schema y el mismo predicado Chai a valores sintéticos (`0`, negativo, decimal, `null`, `"0"`, `""`, `"41.40338"`, `true`, `{}`, `[]`). Todos se clasificaron según el contrato. Resultado en `evidencias/verificacion-logica-validacion.txt`.

Comando oficial:

```bash
newman run postman/TC-CON-002.postman_collection.json \
  -e postman/OpenBreweryDB.postman_environment.json \
  --folder "TC-CON-002" \
  -r cli,json,htmlextra \
  --reporter-json-export evidencias/TC-CON-002-newman.json \
  --reporter-htmlextra-export evidencias/TC-CON-002-newman.html \
  > evidencias/TC-CON-002-newman.txt 2>&1
```

---

## 7. JSON Schema utilizado

Ruta: `schemas/TC-CON-002-brewery-types.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TC-CON-002 - Tipos de datos Brewery",
  "type": "object",
  "required": [
    "id",
    "name",
    "latitude",
    "longitude"
  ],
  "properties": {
    "id": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "latitude": {
      "type": ["number", "null"]
    },
    "longitude": {
      "type": ["number", "null"]
    }
  }
}
```

Se verificó que el schema incrustado en el script del Paso 2 de la colección registrada por Newman (run oficial) es idéntico al contenido de este archivo. `latitude` y `longitude` esperan `["number", "null"]`, no String.

---

## 8. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-CON-002-newman.json`), Paso 2:

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Raíz | Object | Object (`Array.isArray` = false) | PASS |
| 5 | `id` | String | string | PASS |
| 6 | `name` | String | string | PASS |
| 7 | `latitude` | Number/Null | number (`50.241246`) | PASS |
| 8 | `longitude` | Number/Null | number (`11.327765`) | PASS |
| 9 | JSON Schema | Cumple | Cumple (AJV válido, 0 errores) | PASS |

Preparación (Paso 1), también en el run oficial: HTTP 200 en listado previo, JSON válido, arreglo, con registros e `id` string no vacío en el registro seleccionado: **5/5 PASS**.

---

## 9. Resultado de AJV

```text
AJV ejecutado: Sí
Mecanismo: require("ajv") dentro del sandbox de scripts de Postman (postman-sandbox 4.7.1,
  incluido en Newman 6.2.2); new Ajv({ allErrors: true }) y ajv.compile(schema) sobre el schema
  draft-07 de TC-CON-002. El sandbox no expone la versión exacta de AJV y no se registró.
Resultado: PASS (validateContract(detailResponse) = true)
Errores: [] (ninguno)
```

Los logs de consola del preflight y del run oficial registran `TC-CON-002 | AJV ejecutado: Sí`, `AJV resultado: PASS` y `AJV errores: []`. La assertion *"TC-CON-002 | JSON cumple el schema de tipos"* solo se registra cuando AJV se carga, y en el run oficial se ejecutó y aprobó.

---

## 10. Resultados

```text
HTTP: 200 OK
Content-Type: application/json
Tipo raíz: Object
Response Time: 86 ms
ID: ae7b3174-8be8-4d53-a3a5-9b8240970eea
URL final: https://api.openbrewerydb.org/v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea

id:
Valor: ae7b3174-8be8-4d53-a3a5-9b8240970eea
Tipo real: string
Esperado: String

name:
Valor: 's
Tipo real: string
Esperado: String

latitude:
Valor: 50.241246
Tipo real: number
Esperado: Number/Null

longitude:
Valor: 11.327765
Tipo real: number
Esperado: Number/Null

AJV: ejecutado — PASS (0 errores)
Assertions totales: 14 (5 preparación + 9 contrato)
Assertions exitosas: 14
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 11. Muestra de respuesta

Valores reales de `evidencias/detalle-response.json` (run oficial), solo los campos del contrato:

```json
{
  "id": "ae7b3174-8be8-4d53-a3a5-9b8240970eea",
  "name": "'s",
  "latitude": 50.241246,
  "longitude": 11.327765
}
```

El cuerpo completo (16 campos) queda en `evidencias/detalle-response.json`.

---

## 12. Matriz de tipos

| Campo | Valor real | Tipo real | Tipo esperado | Estado |
|---|---|---|---|---|
| id | `"ae7b3174-8be8-4d53-a3a5-9b8240970eea"` | string | String | PASS |
| name | `"'s"` | string | String | PASS |
| latitude | `50.241246` | number | Number/Null | PASS |
| longitude | `11.327765` | number | Number/Null | PASS |

El tipo real se calculó con un helper que devuelve `"null"` para `null` y `"array"` para arreglos antes de usar `typeof`. Así se evita reportar `null` como `object`. En este registro ninguno de los campos fue `null`.

---

## 13. Evidencias

```text
postman/TC-CON-002.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
schemas/TC-CON-002-brewery-types.schema.json
evidencias/TC-CON-002-newman.json             (reporte JSON — run oficial)
evidencias/TC-CON-002-newman.txt              (salida de consola — run oficial)
evidencias/TC-CON-002-newman.html             (reporte HTML htmlextra — run oficial)
evidencias/listado-previo-response.json       (cuerpo real de GET /v1/breweries — run oficial)
evidencias/detalle-response.json              (cuerpo real de GET /v1/breweries/{id} — run oficial)
evidencias/preflight-1-newman.json            (preflight — 14/14 PASS)
evidencias/preflight-1-newman.txt
evidencias/verificacion-logica-validacion.txt (verificación auxiliar con datos sintéticos; no es ejecución contra la API)
TC-CON-002_Informe.md
```

La carpeta también contenía un archivo `.gitkeep` vacío creado antes de esta ejecución. No forma parte de la evidencia y se conservó sin cambios.

---

## 14. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman se obtuvo dinámicamente el ID
ae7b3174-8be8-4d53-a3a5-9b8240970eea desde GET /v1/breweries, y
GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea respondió 200 OK con
application/json y un objeto JSON válido. Los tipos cumplen el contrato: id =
string, name = string, latitude = number (50.241246), longitude = number
(11.327765). Lo confirman las 4 assertions Chai de tipos y la validación AJV del
JSON Schema de TC-CON-002 (PASS, 0 errores). Las 14 assertions se aprobaron (0
fallidas) y Newman terminó con código de salida 0. El preflight dio el mismo
resultado.
```

---

## 15. Hallazgos

No se identificaron incumplimientos de tipos de datos durante TC-CON-002.

> Alcance: el resultado corresponde al registro evaluado en el run oficial, cuyas coordenadas son numéricas. Este registro no ejercitó el caso `latitude`/`longitude` = `null` contra la API. El tratamiento correcto de `null` y de `0` está respaldado por la definición del schema y de las assertions, y por la verificación auxiliar con datos sintéticos (`evidencias/verificacion-logica-validacion.txt`).

---

## 16. Registro para Excel

### Registro para Excel

```text
ID: TC-CON-002
Resultado obtenido: HTTP 200 OK. GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea retornó un objeto JSON. Se validaron los tipos de datos del contrato: id=String, name=String, latitude=Number y longitude=Number. Contrato esperado: String, String, Number/Null y Number/Null. Validación AJV: PASS. Se ejecutaron 14 assertions: 14 aprobadas y 0 fallidas. Tiempo de respuesta: 86 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-CON-002-newman.json (complementos: TC-CON-002-newman.txt, TC-CON-002-newman.html, detalle-response.json, listado-previo-response.json, schemas/TC-CON-002-brewery-types.schema.json)
Observaciones: ID obtenido dinámicamente desde GET /v1/breweries en el mismo run. latitude=50.241246 y longitude=11.327765 (numéricos). AJV ejecutado realmente en el sandbox de Newman 6.2.2, PASS sin errores. Preflight previo 14/14 PASS. Lógica de validación de 0/null/strings numéricos verificada con datos sintéticos. Ejecución el 2026-10-01 06:46 UTC; exit code 0.
```
