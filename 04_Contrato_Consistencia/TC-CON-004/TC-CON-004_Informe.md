# Informe de Ejecución — TC-CON-004

## 1. Identificación

```text
Caso: TC-CON-004
Nombre: Estructura de metadatos
Tipo: Contrato y Consistencia
API: Open BreweryDB
Endpoint: GET /v1/breweries/meta
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2 + AJV/JSON Schema (draft-07) + Chai (pm.expect)
Fecha/hora: 2026-10-01T07:02:24.772Z (UTC) — 2026-10-01 02:02:24 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que `GET /v1/breweries/meta` (sin parámetros) mantiene los campos mínimos de metadatos del contrato de TC-CON-004: `total`, `page` y `per_page` deben estar presentes y ser **números enteros** (`Number.isInteger`, sin convertir strings). Los metadatos adicionales que devuelva la API están permitidos: se documentan, pero no invalidan el contrato. La validación se hizo con un JSON Schema ejecutado con AJV y con assertions Chai equivalentes.

---

## 3. Contrato esperado

```text
Campos obligatorios:
- total: Integer
- page: Integer
- per_page: Integer

Propiedades adicionales: permitidas
```

> **Nota de versión del contrato.** Este informe corresponde a la versión revisada del paquete de instrucciones de TC-CON-004, entregada por el responsable del caso. Antes, en esta misma sesión, se había ejecutado una versión anterior con contrato **estricto** (`additionalProperties: false`, exactamente tres propiedades). Aquella ejecución (run oficial 2026-10-01T06:51:50Z UTC) resultó **RECHAZADA** por las propiedades adicionales `by_state`, `by_country` y `by_type`: 10/12 assertions, 3 errores AJV `additionalProperties`. Al iniciar esta ejecución, los artefactos de esa versión **ya no estaban en la carpeta**, nunca se llegó a hacer commit en git y no se pudieron conservar. El cambio de contrato lo decidió el responsable del caso mediante el nuevo paquete; durante esta ejecución no se modificó el contrato.

---

## 4. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en el preflight y en el run oficial. |
| Disponibilidad de la API | Comprobada | `200 OK` en ambas ejecuciones. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2` (postman-sandbox 4.7.1); reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección, environment y schema válidos | Comprobada | Los tres archivos se validaron con `JSON.parse` antes del preflight. |
| Schema sin `additionalProperties` | Comprobada | `grep` de `additionalProperties` en el schema y en la colección: 0 coincidencias. Tampoco existe ninguna assertion de "exactamente tres propiedades". |
| AJV disponible en el runtime | Comprobada | `require("ajv")` se resolvió en el sandbox; el log registra `AJV ejecutado: Sí` en ambas ejecuciones. |
| Sin query params | Comprobada | Newman registra `"query": []` en la request. |

---

## 5. Configuración

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries/meta
URL final: https://api.openbrewerydb.org/v1/breweries/meta
Query Params: Ninguno
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 2 (1 preflight + 1 oficial); el estado se determina con el run oficial
```

---

## 6. Procedimiento

1. **Preparación** — Se comprobó el estado de la carpeta: solo contenía `.gitkeep` (ver nota en la sección 3). Se crearon `postman/`, `schemas/` y `evidencias/`. Primero se escribió el JSON Schema revisado y después se generó la colección con un script Node auxiliar que **lee el schema del archivo y lo incrusta tal cual** en el script de tests. Colección *Open BreweryDB - Contrato y Consistencia* → carpeta `TC-CON-004` → request *TC-CON-004 - Estructura de metadatos* (`GET {{base_url}}/breweries/meta`).
2. **Preflight** (07:02:08Z UTC) — `200 OK`, 590 ms. AJV se ejecutó realmente y dio PASS, con errores `[]`. Se revisaron la presencia y los tipos de `total`, `page` y `per_page` (number, enteros). Los campos adicionales (`by_country`, `by_state`, `by_type`) se registraron sin convertirlos en fallo. 11 assertions, 0 fallidas, exit code 0. No hubo defectos de script. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Run oficial** (07:02:24.772Z → 07:02:25.219Z UTC), exit code `0`:
   ```bash
   newman run postman/TC-CON-004.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-CON-004" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-CON-004-newman.json \
     --reporter-htmlextra-export evidencias/TC-CON-004-newman.html \
     > evidencias/TC-CON-004-newman.txt 2>&1
   ```
4. **AJV** — `new Ajv({ allErrors: true }).compile(contractSchema)` aplicado a `metaResponse`: válido, sin errores.
5. **Assertions** — 11 ejecutadas: 4 generales, 3 de presencia, 3 de tipo entero y 1 de schema. 11 aprobadas, 0 fallidas; `run.failures` vacío.
6. **Extracción del response body** — Se extrajo de `run.executions[0].response.stream` del reporte JSON oficial y se guardó completo en `evidencias/response-body.json`, con sus 6 propiedades y solo con indentación.
7. **Verificación auxiliar de la lógica** (fuera del run, sin llamar a la API) — Se aplicaron el mismo schema y el equivalente Chai a objetos sintéticos para confirmar que el schema revisado admite propiedades adicionales y `0`, y que sigue rechazando `"50"`, `50.5`, `null`, `true` y la ausencia de un campo obligatorio. Las 8 comprobaciones coinciden con el contrato. Resultado en `evidencias/verificacion-logica-validacion.txt`.
8. **Estado** — Se cumplen todas las condiciones del criterio de aprobación, por lo que el caso queda **APROBADO**.

---

## 7. JSON Schema utilizado

Ruta: `schemas/TC-CON-004-meta.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TC-CON-004 - Metadatos obligatorios",
  "type": "object",
  "required": [
    "total",
    "page",
    "per_page"
  ],
  "properties": {
    "total": {
      "type": "integer"
    },
    "page": {
      "type": "integer"
    },
    "per_page": {
      "type": "integer"
    }
  }
}
```

Se verificó que el schema incrustado en la colección registrada por Newman (run oficial) es idéntico al contenido de este archivo. **No contiene `additionalProperties: false`** y no impone tipos ni obligatoriedad a otros campos.

---

## 8. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-CON-004-newman.json`):

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Raíz | Object | Object (`Array.isArray` = false) | PASS |
| 5 | `total` presente | Sí | Sí | PASS |
| 6 | `page` presente | Sí | Sí | PASS |
| 7 | `per_page` presente | Sí | Sí | PASS |
| 8 | `total` | Integer | number, entero (`11848`) | PASS |
| 9 | `page` | Integer | number, entero (`1`) | PASS |
| 10 | `per_page` | Integer | number, entero (`50`) | PASS |
| 11 | JSON Schema AJV | Cumple | Cumple (0 errores) | PASS |

---

## 9. Resultado AJV

```text
AJV ejecutado: Sí
Mecanismo: require("ajv") dentro del sandbox de scripts de Postman (postman-sandbox 4.7.1,
  incluido en Newman 6.2.2); new Ajv({ allErrors: true }) y ajv.compile(schema) sobre el
  schema draft-07 de TC-CON-004. El sandbox no expone la versión exacta de AJV y no se registró.
Resultado: PASS (validateContract(metaResponse) = true)
Errores: [] (ninguno)
```

---

## 10. Resultados obtenidos

```text
URL: https://api.openbrewerydb.org/v1/breweries/meta
HTTP: 200 OK
Content-Type: application/json
Response Time: 311 ms
Tamaño de respuesta: 3950 bytes
Tipo raíz: Object

Propiedades reales: by_country, by_state, by_type, page, per_page, total
  (orden real en la respuesta: total, by_state, by_country, by_type, page, per_page)
Total de propiedades: 6
Campos obligatorios faltantes: ninguno
Campos adicionales: by_country, by_state, by_type

total:
Valor: 11848
Tipo: number
¿Entero?: Sí

page:
Valor: 1
Tipo: number
¿Entero?: Sí

per_page:
Valor: 50
Tipo: number
¿Entero?: Sí

AJV ejecutado: Sí — Resultado: PASS (0 errores)
Assertions totales: 11
Assertions exitosas: 11
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 11. Respuesta real

Respuesta del run oficial con el orden real de claves. `by_type` aparece completo; `by_state` y `by_country` se **abrevian solo en este informe** a sus 3 primeras entradas reales:

```json
{
  "total": 11848,
  "by_state": { "ACT": 7, "Alabama": 52, "Alaska": 60, "…": "(211 claves más)" },
  "by_country": { "Australia": 514, "Austria": 15, "Belgium": 478, "…": "(20 claves más)" },
  "by_type": {
    "bar": 41, "beergarden": 3, "brewpub": 3929, "cidery": 7, "closed": 642,
    "contract": 210, "large": 137, "location": 1, "micro": 5864, "nano": 22,
    "planning": 639, "proprietor": 67, "regional": 239, "taproom": 47
  },
  "page": 1,
  "per_page": 50
}
```

Las entradas `"…"` son solo una marca de abreviación del informe y no forman parte de la respuesta. `evidencias/response-body.json` contiene el cuerpo completo y sin alterar (214 claves en `by_state` y 23 en `by_country`).

---

## 12. Matriz de contrato

| Campo | Presente | Valor real | Tipo real | Esperado | Estado |
|---|---|---|---|---|---|
| total | Sí | `11848` | number (entero) | Integer | PASS |
| page | Sí | `1` | number (entero) | Integer | PASS |
| per_page | Sí | `50` | number (entero) | Integer | PASS |

```text
Campos adicionales observados: by_state (objeto, 214 claves), by_country (objeto, 23 claves), by_type (objeto, 14 claves)
(Informativo: permitidos por el contrato; sin estado FAIL.)
```

---

## 13. Evidencias

```text
postman/TC-CON-004.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
schemas/TC-CON-004-meta.schema.json
evidencias/TC-CON-004-newman.json              (reporte JSON — run oficial)
evidencias/TC-CON-004-newman.txt               (salida de consola — run oficial)
evidencias/TC-CON-004-newman.html              (reporte HTML htmlextra — run oficial)
evidencias/response-body.json                  (cuerpo real completo — run oficial)
evidencias/preflight-1-newman.json             (preflight — 11/11 PASS)
evidencias/preflight-1-newman.txt
evidencias/verificacion-logica-validacion.txt  (verificación auxiliar con datos sintéticos; no es ejecución contra la API)
TC-CON-004_Informe.md
```

La carpeta también contiene un archivo `.gitkeep` vacío creado antes de esta ejecución, que se conservó sin cambios. Las evidencias de la ejecución anterior con contrato estricto no estaban disponibles (ver sección 3).

---

## 14. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman, GET /v1/breweries/meta (sin query params) respondió
200 OK con application/json y un objeto JSON válido. Los tres campos obligatorios
están presentes y son enteros: total = 11848, page = 1 y per_page = 50 (number,
Number.isInteger = true). La validación AJV del JSON Schema revisado fue PASS sin
errores. La respuesta incluye además by_state, by_country y by_type, que el contrato
revisado permite y que se documentan de forma informativa. Las 11 assertions se
aprobaron (0 fallidas) y Newman terminó con código de salida 0. El preflight dio el
mismo resultado.
```

---

## 15. Hallazgos

No se identificaron incumplimientos en los campos obligatorios de metadatos durante TC-CON-004.

---

## 16. Registro para Excel

### Registro para Excel

```text
ID: TC-CON-004
Resultado obtenido: HTTP 200 OK. GET /v1/breweries/meta retornó un objeto JSON. Se verificaron los campos obligatorios del contrato: total=11848 (number entero), page=1 (number entero) y per_page=50 (number entero). Campos obligatorios faltantes: NINGUNO. La respuesta contiene 3 propiedades adicionales de metadatos: by_state, by_country, by_type, permitidas por el contrato. Validación AJV: PASS. Se ejecutaron 11 assertions: 11 aprobadas y 0 fallidas. Tiempo de respuesta: 311 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-CON-004-newman.json (complementos: TC-CON-004-newman.txt, TC-CON-004-newman.html, response-body.json, schemas/TC-CON-004-meta.schema.json)
Observaciones: Ejecutado con la versión revisada del contrato (propiedades adicionales permitidas, sin additionalProperties: false). Una ejecución previa con contrato estricto fue RECHAZADA por by_state, by_country y by_type, pero su evidencia no estaba disponible al iniciar esta ejecución. AJV ejecutado realmente en el sandbox de Newman 6.2.2. Preflight previo 11/11 PASS. Ejecución el 2026-10-01 07:02 UTC; exit code 0.
```
