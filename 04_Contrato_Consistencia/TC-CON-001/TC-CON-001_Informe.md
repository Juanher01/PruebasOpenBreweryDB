# Informe de Ejecución — TC-CON-001

## 1. Identificación

```text
Caso: TC-CON-001
Nombre: Presencia de campos obligatorios
Tipo: Contrato y Consistencia
API: Open BreweryDB
Endpoint: GET /v1/breweries/{id}
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2 + AJV/JSON Schema (draft-07) + Chai (pm.expect)
Fecha/hora: 2026-10-01T06:36:52.930Z (UTC) — 2026-10-01 01:36:52 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que la representación JSON de una cervecería individual (`GET /v1/breweries/{id}`, con un ID obtenido dinámicamente) cumple el contrato mínimo de TC-CON-001: respuesta `200 OK`, JSON válido con raíz de tipo objeto y **presencia** de las seis propiedades obligatorias. La validación se hizo mediante JSON Schema/AJV y, de forma complementaria, con una assertion Chai por campo.

---

## 3. Contrato evaluado

```text
Campos obligatorios:
- id
- name
- brewery_type
- city
- state
- country
```

TC-CON-001 valida **presencia de propiedades**, no tipos ni nulabilidad. El schema no declara `properties`, `type` por campo ni `additionalProperties: false`. Un campo con valor `null` se considera presente. La validación de tipos corresponde a TC-CON-002.

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
| Independencia de otros casos | Comprobada | No se leyó ni reutilizó ningún archivo de otros casos. |

---

## 5. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Consulta previa: GET {{base_url}}/breweries   (sin parámetros; solo preparación de datos)
Endpoint de detalle: GET {{base_url}}/breweries/{{brewery_id}}
ID obtenido: ae7b3174-8be8-4d53-a3a5-9b8240970eea
URL consultada: /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 2 runs (1 preflight + 1 oficial), cada uno con 2 requests; el estado se determina con el run oficial
```

**Origen dinámico del ID:** `brewery_id` inicia vacío en el environment y el pre-request del Paso 1 lo vacía de nuevo. El script de tests del Paso 1 lo asigna desde `listResponse[0].id`. En el run oficial, el ID usado en la URL del Paso 2 (`ae7b3174-8be8-4d53-a3a5-9b8240970eea`) coincide con el `id` del primer elemento de `evidencias/listado-previo-response.json`. La colección no contiene ningún UUID escrito a mano.

---

## 6. Procedimiento

1. **Preparación** — Se crearon `postman/`, `schemas/` y `evidencias/`. Primero se escribió el JSON Schema y después se generó la colección con un script Node auxiliar que **lee el schema del archivo y lo incrusta tal cual** en el script de tests del Paso 2, para que el schema ejecutado y el conservado sean el mismo. Colección *Open BreweryDB - Contrato y Consistencia* → carpeta `TC-CON-001` → Paso 1 *Obtener ID válido* y Paso 2 *Validar contrato de detalle*.
2. **Preflight** (06:36:34Z UTC) — Flujo completo: el ID se obtuvo dinámicamente, el detalle se consultó con ese ID, las assertions funcionaron y AJV se ejecutó realmente (`AJV ejecutado: Sí`, `PASS`, errores `[]`). 16 assertions, 0 fallidas, exit code 0. No hubo defectos de script. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Obtención dinámica del ID** (run oficial) — `GET /v1/breweries` → `200 OK`, 50 registros, 574 ms; se tomó `listResponse[0].id` = `ae7b3174-8be8-4d53-a3a5-9b8240970eea`.
4. **Consulta de detalle** — `GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea` → `200 OK`, `application/json`, 85 ms.
5. **Validación del schema** — `new Ajv({ allErrors: true }).compile(contractSchema)` aplicado a `detailResponse`: válido, sin errores.
6. **Assertions** — 5 en el Paso 1 y 11 en el Paso 2 (4 de respuesta, 6 de presencia por campo y 1 de schema): 16 aprobadas, 0 fallidas; `run.failures` vacío; exit code `0`.
7. **Evidencias** — Los cuerpos del listado y del detalle se extrajeron de `run.executions[0|1].response.stream` del reporte JSON oficial y se guardaron solo con indentación.

Comando oficial:

```bash
newman run postman/TC-CON-001.postman_collection.json \
  -e postman/OpenBreweryDB.postman_environment.json \
  --folder "TC-CON-001" \
  -r cli,json,htmlextra \
  --reporter-json-export evidencias/TC-CON-001-newman.json \
  --reporter-htmlextra-export evidencias/TC-CON-001-newman.html \
  > evidencias/TC-CON-001-newman.txt 2>&1
```

---

## 7. JSON Schema utilizado

Ruta: `schemas/TC-CON-001-brewery-required-fields.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TC-CON-001 - Campos obligatorios de Brewery",
  "type": "object",
  "required": [
    "id",
    "name",
    "brewery_type",
    "city",
    "state",
    "country"
  ]
}
```

Se verificó que el schema incrustado en el script del Paso 2 de la colección registrada por Newman (`run` oficial) es idéntico al contenido de este archivo.

---

## 8. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-CON-001-newman.json`), Paso 2:

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Raíz | Object | Object (`Array.isArray` = false) | PASS |
| 5 | `id` | Presente | Presente (`"ae7b3174-8be8-4d53-a3a5-9b8240970eea"`) | PASS |
| 6 | `name` | Presente | Presente (`"'s"`) | PASS |
| 7 | `brewery_type` | Presente | Presente (`"brewpub"`) | PASS |
| 8 | `city` | Presente | Presente (`"Kronach"`) | PASS |
| 9 | `state` | Presente | Presente (`"Bayern"`) | PASS |
| 10 | `country` | Presente | Presente (`"Germany"`) | PASS |
| 11 | JSON Schema | Cumple | Cumple (AJV válido, 0 errores) | PASS |

Preparación (Paso 1), también en el run oficial: HTTP 200 en listado previo, JSON válido, arreglo, al menos un registro e `id` string no vacío en el registro seleccionado: **5/5 PASS**.

---

## 9. Resultado de AJV

```text
AJV ejecutado: Sí
Versión/mecanismo utilizado: require("ajv") dentro del sandbox de scripts de Postman
  (postman-sandbox 4.7.1, incluido en Newman 6.2.2); instancia new Ajv({ allErrors: true })
  y ajv.compile(schema) sobre el schema draft-07 de TC-CON-001. El sandbox no expone la
  versión exacta de AJV y no se registró.
Resultado: PASS (validateContract(detailResponse) = true)
Errores AJV: [] (ninguno)
```

AJV se ejecutó tanto en el preflight como en el run oficial. Ambos logs de consola lo registran (`TC-CON-001 | AJV ejecutado: Sí`, `TC-CON-001 | AJV resultado: PASS`, `TC-CON-001 | AJV errores: []`). La assertion *"TC-CON-001 | JSON cumple el schema de campos obligatorios"* solo se registra cuando AJV se carga, y en el run oficial se ejecutó y aprobó.

---

## 10. Resultados

```text
HTTP: 200 OK
Content-Type: application/json
Tipo raíz: Object
Response Time: 85 ms
ID: ae7b3174-8be8-4d53-a3a5-9b8240970eea
URL final: https://api.openbrewerydb.org/v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea
Campo id: presente
Campo name: presente
Campo brewery_type: presente
Campo city: presente
Campo state: presente
Campo country: presente
Campos obligatorios esperados: 6
Campos presentes: 6
Campos faltantes: ninguno
AJV ejecutado: Sí
Resultado AJV: PASS
Assertions totales: 16 (5 preparación + 11 contrato)
Assertions exitosas: 16
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 11. Muestra de respuesta

Los seis campos obligatorios, con sus valores reales tomados de `evidencias/detalle-response.json` (run oficial):

```json
{
  "id": "ae7b3174-8be8-4d53-a3a5-9b8240970eea",
  "name": "'s",
  "brewery_type": "brewpub",
  "city": "Kronach",
  "state": "Bayern",
  "country": "Germany"
}
```

El cuerpo completo (16 campos) queda en `evidencias/detalle-response.json`.

---

## 12. Evidencias

```text
postman/TC-CON-001.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
schemas/TC-CON-001-brewery-required-fields.schema.json
evidencias/TC-CON-001-newman.json         (reporte JSON — run oficial)
evidencias/TC-CON-001-newman.txt          (salida de consola — run oficial)
evidencias/TC-CON-001-newman.html         (reporte HTML htmlextra — run oficial)
evidencias/listado-previo-response.json   (cuerpo real de GET /v1/breweries — run oficial)
evidencias/detalle-response.json          (cuerpo real de GET /v1/breweries/{id} — run oficial)
evidencias/preflight-1-newman.json        (preflight — 16/16 PASS)
evidencias/preflight-1-newman.txt
TC-CON-001_Informe.md
```

La carpeta también contenía un archivo `.gitkeep` vacío creado antes de esta ejecución. No forma parte de la evidencia y se conservó sin cambios.

---

## 13. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman se obtuvo dinámicamente el ID
ae7b3174-8be8-4d53-a3a5-9b8240970eea desde GET /v1/breweries, y
GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea respondió 200 OK con
application/json y un objeto JSON válido. Están presentes los 6 campos
obligatorios (id, name, brewery_type, city, state, country), lo que confirman
las 6 assertions Chai por campo y la validación AJV del JSON Schema de TC-CON-001
(PASS, 0 errores). Las 16 assertions se aprobaron (0 fallidas) y Newman terminó
con código de salida 0. El preflight dio el mismo resultado.
```

---

## 14. Hallazgos

No se identificaron incumplimientos de contrato durante TC-CON-001.

> Observación (fuera del alcance de TC-CON-001, que solo valida presencia): para este registro alemán, `state` vale `"Bayern"`, igual que `state_province`. El valor de `name` es `"'s"`, que parece un nombre incompleto. Ninguno afecta a la presencia de los campos. Se dejan anotados por si se quieren revisar en TC-CON-002 o en pruebas de calidad de datos.

---

## 15. Registro para Excel

### Registro para Excel

```text
ID: TC-CON-001
Resultado obtenido: HTTP 200 OK. GET /v1/breweries/ae7b3174-8be8-4d53-a3a5-9b8240970eea retornó un objeto JSON. Se verificaron los 6 campos obligatorios definidos por el contrato: id, name, brewery_type, city, state y country. Se encontraron 6 de 6 campos; campos faltantes: NINGUNO. Validación de schema: PASS. Se ejecutaron 16 assertions: 16 aprobadas y 0 fallidas. Tiempo de respuesta: 85 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-CON-001-newman.json (complementos: TC-CON-001-newman.txt, TC-CON-001-newman.html, detalle-response.json, listado-previo-response.json, schemas/TC-CON-001-brewery-required-fields.schema.json)
Observaciones: ID obtenido dinámicamente desde GET /v1/breweries en el mismo run. AJV ejecutado realmente en el sandbox de Newman 6.2.2 (require("ajv")), resultado PASS sin errores. El schema solo valida presencia (required), sin tipos. Preflight previo 16/16 PASS. Ejecución el 2026-10-01 06:36 UTC; exit code 0.
```
