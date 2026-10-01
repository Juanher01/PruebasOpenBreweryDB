# Informe de Ejecución — TC-FUN-005

## 1. Identificación

```text
Caso de prueba: TC-FUN-005
Nombre: Consulta de Metadatos
Tipo: Funcional
API: Open BreweryDB
Endpoint: GET /v1/breweries/meta
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora de ejecución: 2026-10-01T06:01:28.428Z (UTC) — 2026-10-01 01:01:28 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que `GET /v1/breweries/meta`, invocado sin parámetros, responde `200 OK` con un objeto JSON de metadatos (no un arreglo) que contiene los campos `total`, `page` y `per_page`. Solo se valida la presencia de esos campos, no sus valores exactos ni el contrato completo.

---

## 3. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en el preflight y en la ejecución oficial. |
| Disponibilidad de la API | Comprobada | `200 OK` en ambas ejecuciones. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección válida | Comprobada | Validada con `JSON.parse` antes del preflight. |
| Environment válido | Comprobada | Validado con `JSON.parse` (`base_url`). |
| Sin query params | Comprobada | Newman registra `"query": []` en la request de ambas ejecuciones. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries/meta
URL final: https://api.openbrewerydb.org/v1/breweries/meta
Query Params: Ninguno
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 2 (1 preflight + 1 oficial); el estado se determina con la ejecución oficial
```

---

## 5. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-005` → request *TC-FUN-005 - Consulta de Metadatos* (`GET {{base_url}}/breweries/meta`) con las 8 assertions obligatorias y los logs de diagnóstico. Se validaron ambos JSON y se comprobó que Newman estaba instalado.
2. **Preflight** (06:01:12Z UTC) — `200 OK`, 422 ms, sin query params, raíz de tipo `object`; 8 assertions, 0 fallidas, exit code 0. La respuesta se procesó correctamente y no hubo defectos de script, por lo que la colección no se modificó. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Ejecución oficial** (06:01:28.428Z → 06:01:28.866Z UTC), exit code `0`:
   ```bash
   newman run postman/TC-FUN-005.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-005" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-005-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-005-newman.html \
     > evidencias/TC-FUN-005-newman.txt 2>&1
   ```
4. **Captura del objeto de metadatos** — Se extrajo de `run.executions[0].response.stream` del reporte JSON oficial y se guardó en `evidencias/response-body.json`, solo con indentación. Se verificó que coincide exactamente con el cuerpo registrado por Newman.
5. **Assertions** — 8 ejecutadas, 8 PASS, 0 FAIL; `run.failures` vacío.
6. **Estado** — Se cumplen todas las condiciones del criterio de aprobación, por lo que el caso queda **APROBADO**.

---

## 6. Aserciones ejecutadas

Valores de la ejecución oficial (`evidencias/TC-FUN-005-newman.json`).

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo de respuesta | Object | Object | PASS |
| 5 | No es Array | Sí | Sí (`Array.isArray` = false) | PASS |
| 6 | Campo `total` | Presente | Presente (`11848`) | PASS |
| 7 | Campo `page` | Presente | Presente (`1`) | PASS |
| 8 | Campo `per_page` | Presente | Presente (`50`) | PASS |

---

## 7. Resultados obtenidos

```text
URL final: https://api.openbrewerydb.org/v1/breweries/meta
Método: GET
Query Params: Ninguno
HTTP: 200 OK
Content-Type: application/json
Response Time: 327 ms
Tamaño de respuesta: 3950 bytes
Tipo de respuesta: Objeto JSON
total: 11848 (number)
page: 1 (number)
per_page: 50 (number)
Assertions ejecutadas: 8
Assertions exitosas: 8
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 8. Muestra de la respuesta

Campos definidos por el caso, con sus valores y tipos reales de la ejecución oficial:

```json
{
  "total": 11848,
  "page": 1,
  "per_page": 50
}
```

La respuesta real contiene además tres campos con conteos agregados, que no forman parte del alcance de TC-FUN-005. Este es el orden real de las claves en la raíz: `total`, `by_state`, `by_country`, `by_type`, `page`, `per_page`.

| Campo adicional | Contenido | Primeras entradas reales |
|---|---|---|
| `by_state` | objeto con 214 claves | `"ACT": 7`, `"Alabama": 52`, `"Alaska": 60` |
| `by_country` | objeto con 23 claves | `"Australia": 514`, `"Austria": 15`, `"Belgium": 478` |
| `by_type` | objeto con 14 claves | `"bar": 41`, `"beergarden": 3`, `"brewpub": 3929` |

El cuerpo completo se conserva en `evidencias/response-body.json`.

---

## 9. Evidencias

```text
postman/TC-FUN-005.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-005-newman.json      (reporte JSON — ejecución oficial)
evidencias/TC-FUN-005-newman.txt       (salida de consola — ejecución oficial)
evidencias/TC-FUN-005-newman.html      (reporte HTML htmlextra — ejecución oficial)
evidencias/response-body.json          (cuerpo real — ejecución oficial)
evidencias/preflight-1-newman.json     (preflight — 8/8 PASS)
evidencias/preflight-1-newman.txt
TC-FUN-005_Informe.md
```

---

## 10. Resultado final

```text
Estado: APROBADO

Justificación:
En la ejecución oficial con Newman, GET /v1/breweries/meta (sin query params)
respondió 200 OK con application/json. El cuerpo es un JSON válido cuya raíz es
un objeto (no un arreglo) y contiene los campos total (11848), page (1) y
per_page (50). Las 8 assertions obligatorias se aprobaron (0 fallidas) y Newman
terminó con código de salida 0. El preflight dio el mismo resultado.
```

---

## 11. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-005.

> Observación (no es hallazgo): la respuesta incluye los campos adicionales `by_state`, `by_country` y `by_type`. El caso exige "como mínimo" `total`, `page` y `per_page`, así que los campos adicionales no afectan al resultado. Se deja constancia por si se quieren revisar en los casos de contrato (TC-CON).

---

## 12. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-005
Resultado obtenido: HTTP 200 OK. GET /v1/breweries/meta retornó un objeto JSON con los campos total=11848, page=1 y per_page=50. Se ejecutaron 8 assertions: 8 aprobadas y 0 fallidas. Tiempo de respuesta: 327 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-005-newman.json (complementos: TC-FUN-005-newman.txt, TC-FUN-005-newman.html, response-body.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 06:01 UTC, sin query params; exit code 0. Preflight previo 8/8 PASS. La respuesta incluye además by_state, by_country y by_type (fuera del alcance funcional). Sin hallazgos.
```
