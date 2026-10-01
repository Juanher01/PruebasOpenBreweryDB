# Informe de Ejecución — TC-FUN-004

## 1. Identificación

```text
Caso de prueba: TC-FUN-004
Nombre: Cervecería aleatoria
Tipo: Funcional
API: Open BreweryDB
Endpoint: GET /v1/breweries/random
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora de ejecución: 2026-10-01T05:54:32.233Z (UTC) — 2026-10-01 00:54:32 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que `GET /v1/breweries/random`, invocado sin parámetros, responde `200 OK` con **un único objeto JSON** de cervecería (no un arreglo), con los campos funcionales básicos `id`, `name` y `brewery_type` como strings no vacíos.

---

## 3. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en las 3 ejecuciones. |
| Disponibilidad de la API | Comprobada | `200 OK` en las 3 ejecuciones. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección válida | Comprobada | Validada con `JSON.parse` antes del preflight. |
| Environment válido | Comprobada | Validado con `JSON.parse` (`base_url`). |
| Sin query params | Comprobada | Newman registra `"query": []` en la request de las 3 ejecuciones. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries/random
URL final: https://api.openbrewerydb.org/v1/breweries/random
Query Params: Ninguno
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 3 (1 preflight + 1 oficial + 1 repetición de confirmación); el estado se determina con la ejecución oficial
```

---

## 5. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-004` → request *TC-FUN-004 - Cervecería aleatoria* (`GET {{base_url}}/breweries/random`) con las 8 assertions obligatorias y los logs de diagnóstico. Se validaron ambos JSON y se comprobó que Newman estaba instalado.
2. **Preflight** (05:54:15Z UTC) — `200 OK`, 1116 ms, sin query params. La respuesta se procesó correctamente y resultó ser un **arreglo** de longitud 1 (`Tipo raíz: array`). 8 assertions: 3 PASS y 5 FAIL. El fallo se debe a la forma real de la respuesta, **no a un defecto del script**, por lo que la colección no se modificó. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Ejecución oficial** (05:54:32.233Z → 05:54:32.787Z UTC), exit code `1`:
   ```bash
   newman run postman/TC-FUN-004.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-004" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-004-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-004-newman.html \
     > evidencias/TC-FUN-004-newman.txt 2>&1
   ```
4. **Repetición de confirmación** (05:54:34.221Z UTC), según el criterio de rechazo: `200 OK`, 1183 ms, de nuevo un arreglo de longitud 1 (otra cervecería) y el mismo resultado, 3 PASS / 5 FAIL. Evidencia: `evidencias/repeticion-1-newman.*`.
5. **Captura del cuerpo** — Se extrajo de `run.executions[0].response.stream` del reporte JSON oficial y se guardó en `evidencias/response-body.json`, solo con indentación. Se conserva tal cual: un arreglo que contiene un objeto.
6. **Assertions** — Pasaron HTTP 200, Content-Type JSON y JSON válido. Fallaron *objeto JSON*, *no es arreglo*, `id`, `name` y `brewery_type`: los tres últimos porque la raíz es un arreglo y no tiene esas propiedades.
7. **Estado** — Con 5 assertions obligatorias fallidas de forma reproducible y el servicio disponible, el caso queda **RECHAZADO**.

---

## 6. Aserciones ejecutadas

Valores de la ejecución oficial (`evidencias/TC-FUN-004-newman.json`).

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo de respuesta | Object | Array (longitud 1) — `expected [ { …(16) } ] to be an object` | **FAIL** |
| 5 | No es Array | Sí | No; `Array.isArray` = true — `expected true to be false` | **FAIL** |
| 6 | `id` | String no vacío | La raíz no tiene `id` — `expected [ { …(16) } ] to have property 'id'` | **FAIL** |
| 7 | `name` | String no vacío | La raíz no tiene `name` — `expected [ { …(16) } ] to have property 'name'` | **FAIL** |
| 8 | `brewery_type` | String no vacío | La raíz no tiene `brewery_type` — `expected [ { …(16) } ] to have property 'brewery_type'` | **FAIL** |

---

## 7. Resultados obtenidos

```text
URL final: https://api.openbrewerydb.org/v1/breweries/random
Método: GET
Query Params: Ninguno
HTTP: 200 OK
Content-Type: application/json
Response Time: 448 ms
Tamaño de respuesta: 436 bytes
Tipo de respuesta: Array con 1 elemento (no un objeto JSON único)
ID: no presente en la raíz de la respuesta (el elemento [0] tiene id = 51c00792-038b-4a5a-af2c-efade94f169f)
Name: no presente en la raíz de la respuesta (el elemento [0] tiene name = Haymarket Pub and Brewery)
brewery_type: no presente en la raíz de la respuesta (el elemento [0] tiene brewery_type = brewpub)
Assertions ejecutadas: 8
Assertions exitosas: 3
Assertions fallidas: 5
Exit code Newman: 1
Resultado global: Fallido
```

Repetición de confirmación: `200 OK`, 1183 ms, Array de 1 elemento (`7925a3a2-254e-4112-b9d8-0ab1af31664c`, `Cranker's Brewery`, `brewpub`), 3 PASS / 5 FAIL, exit code `1`.
Preflight: `200 OK`, 1116 ms, Array de 1 elemento (`e727713f-2a19-4113-bdb4-3381eb693317`, `Butjenter Brauhaus`, `brewpub`), 3 PASS / 5 FAIL.

---

## 8. Muestra de la respuesta

Respuesta real de la ejecución oficial. La raíz es un **arreglo**; a continuación se muestra con un subconjunto de los campos del único elemento:

```json
[
  {
    "id": "51c00792-038b-4a5a-af2c-efade94f169f",
    "name": "Haymarket Pub and Brewery",
    "brewery_type": "brewpub",
    "city": "Chicago",
    "state": "Illinois",
    "country": "United States"
  }
]
```

El cuerpo completo (arreglo con un objeto de 16 campos) se conserva en `evidencias/response-body.json`.

---

## 9. Consideración sobre aleatoriedad

```text
TC-FUN-004 valida que /random retorne una única cervecería válida.
Este caso no constituye una prueba estadística de aleatoriedad y no
exige que ejecuciones consecutivas produzcan registros distintos.
```

Las tres ejecuciones devolvieron registros distintos. Ese dato se deja solo como constancia: no influye en el resultado.

---

## 10. Evidencias

```text
postman/TC-FUN-004.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-004-newman.json      (reporte JSON — ejecución oficial)
evidencias/TC-FUN-004-newman.txt       (salida de consola — ejecución oficial)
evidencias/TC-FUN-004-newman.html      (reporte HTML htmlextra — ejecución oficial)
evidencias/response-body.json          (cuerpo real — ejecución oficial)
evidencias/preflight-1-newman.json     (preflight — 3 PASS / 5 FAIL)
evidencias/preflight-1-newman.txt
evidencias/repeticion-1-newman.json    (repetición de confirmación — 3 PASS / 5 FAIL)
evidencias/repeticion-1-newman.txt
TC-FUN-004_Informe.md
```

---

## 11. Resultado final

```text
Estado: RECHAZADO

Justificación:
El servicio estuvo disponible: GET /v1/breweries/random (sin query params)
respondió 200 OK con application/json y un cuerpo JSON válido. Sin embargo, la
raíz de la respuesta es un arreglo de 1 elemento y no un objeto JSON único, que
es lo que establece el resultado esperado. Por ello fallaron 5 de las 8
assertions obligatorias: objeto JSON, no es arreglo, id, name y brewery_type
(los tres últimos porque esas propiedades no existen en la raíz). El
comportamiento se reprodujo en 3 de 3 ejecuciones (preflight, oficial y
repetición). Ejecución oficial: 8 assertions, 3 aprobadas, 5 fallidas, exit
code 1.
```

---

## 12. Hallazgos

```text
Descripción: GET /v1/breweries/random devuelve la cervecería envuelta en un arreglo
JSON en lugar de un objeto JSON único.

Comportamiento esperado: Objeto JSON único de una cervecería (raíz de tipo object,
no array), con id, name y brewery_type como strings no vacíos en la raíz.

Comportamiento obtenido: HTTP 200 OK, application/json; raíz = arreglo de longitud
1, p. ej. [ { "id": "51c00792-038b-4a5a-af2c-efade94f169f",
"name": "Haymarket Pub and Brewery", "brewery_type": "brewpub", ... } ].

Reproducibilidad: Reproducible, 3 de 3 ejecuciones (preflight 05:54:15Z, oficial
05:54:32Z y repetición 05:54:34Z UTC). En las tres la raíz fue un arreglo de 1
elemento, con registros distintos en cada una.

Impacto: Fallan 5 de las 8 assertions obligatorias y TC-FUN-004 queda RECHAZADO. Un
cliente que espere un objeto según la definición del caso no puede leer id, name
ni brewery_type directamente de la raíz.

Observación diagnóstica: el único elemento del arreglo sí contiene id, name y
brewery_type como strings no vacíos (en las 3 ejecuciones). La discrepancia está en
la forma de la raíz (Array frente a Object), no en el contenido del registro. Hay que
decidir si es un defecto del servicio o si el resultado esperado del caso debe
revisarse; esa decisión no corresponde a esta ejecución, y las assertions no se
modificaron.
```

---

## 13. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-004
Resultado obtenido: HTTP 200 OK. GET /v1/breweries/random retornó un arreglo JSON con 1 elemento en lugar de un objeto JSON único; el elemento corresponde a la cervecería id 51c00792-038b-4a5a-af2c-efade94f169f, name Haymarket Pub and Brewery, brewery_type brewpub. Se ejecutaron 8 assertions: 3 aprobadas y 5 fallidas (objeto JSON, no es arreglo, id, name y brewery_type en la raíz). Tiempo de respuesta: 448 ms.
Estado: RECHAZADO
Evidencia principal: evidencias/TC-FUN-004-newman.json (complementos: TC-FUN-004-newman.txt, TC-FUN-004-newman.html, response-body.json, repeticion-1-newman.json)
Observaciones: Fallo reproducible en 3 de 3 ejecuciones: la raíz siempre es un Array de 1 elemento. El elemento interno sí contiene id, name y brewery_type válidos. Sin query params. Ejecución con Newman 6.2.2 el 2026-10-01 05:54 UTC; exit code 1.
```
