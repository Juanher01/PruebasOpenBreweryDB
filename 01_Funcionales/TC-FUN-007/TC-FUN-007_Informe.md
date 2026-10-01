# Informe de Ejecución — TC-FUN-007

## 1. Identificación

```text
Caso de prueba: TC-FUN-007
Nombre: Filtrado por Tipo
Tipo: Funcional
API: Open BreweryDB
Endpoint: GET /v1/breweries?by_type=micro
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora de ejecución: 2026-10-01T06:09:44.213Z (UTC) — 2026-10-01 01:09:44 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que Open BreweryDB procesa el filtro `by_type=micro` en `GET /v1/breweries` y responde `200 OK` con un arreglo JSON no vacío de objetos en el que **todos** los registros tienen el campo `brewery_type` con valor `"micro"`. No se aceptan como equivalentes valores como `brewpub`, `regional`, `large` o `microbrewery`.

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
| Filtro exacto | Comprobada | Newman registra `"query": [{"key": "by_type", "value": "micro"}]` como único parámetro. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries?by_type=micro
URL final: https://api.openbrewerydb.org/v1/breweries?by_type=micro
Filtro: by_type=micro  (único parámetro; sin paginación ni filtros adicionales)
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 2 (1 preflight + 1 oficial); el estado se determina con la ejecución oficial
```

---

## 5. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-007` → request *TC-FUN-007 - Filtrado por Tipo* (`GET {{base_url}}/breweries?by_type=micro`) con las 8 assertions obligatorias y el diagnóstico por consola (cantidad, tipos retornados y no conformes). Se validaron ambos JSON y se comprobó que Newman estaba instalado.
2. **Preflight** (06:09:29Z UTC) — `200 OK`, 751 ms, URL con `by_type=micro`; 50 registros, todos `micro`; 8 assertions, 0 fallidas, exit code 0. No hubo defectos de script, por lo que la colección no se modificó. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Ejecución oficial** (06:09:44.213Z → 06:09:44.685Z UTC), exit code `0`:
   ```bash
   newman run postman/TC-FUN-007.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-007" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-007-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-007-newman.html \
     > evidencias/TC-FUN-007-newman.txt 2>&1
   ```
4. **Captura del response body** — Se extrajo de `run.executions[0].response.stream` del reporte JSON oficial y se guardó en `evidencias/response-body.json`, solo con indentación. Se verificó que coincide exactamente con el cuerpo registrado por Newman.
5. **Evaluación de todos los registros** — Se recorrieron los 50 registros del cuerpo oficial con el mismo criterio de la assertion 8 (`brewery_type.toLowerCase() === "micro"`): 50 cumplen y 0 no cumplen. El único valor observado de `brewery_type` es `"micro"`, en minúsculas y de forma literal.
6. **Assertions** — 8 ejecutadas, 8 PASS, 0 FAIL; `run.failures` vacío. El diagnóstico de consola también reporta `Registros no conformes: 0`.
7. **Estado** — Se cumplen todas las condiciones del criterio de aprobación, por lo que el caso queda **APROBADO**.

---

## 6. Aserciones ejecutadas

Valores de la ejecución oficial (`evidencias/TC-FUN-007-newman.json`).

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo de respuesta | Array | Array | PASS |
| 5 | Registros | > 0 | 50 | PASS |
| 6 | Elementos | Objetos | 50 de 50 objetos | PASS |
| 7 | Campo `brewery_type` | Presente en todos | 50 de 50 con `brewery_type` string | PASS |
| 8 | Tipo de todos los registros | micro | 50 de 50 con `brewery_type` = `"micro"` | PASS |

---

## 7. Resultados obtenidos

```text
URL final: https://api.openbrewerydb.org/v1/breweries?by_type=micro
Método: GET
Filtro utilizado: by_type=micro
HTTP: 200 OK
Content-Type: application/json
Response Time: 355 ms
Tamaño de respuesta: 20561 bytes
Cantidad de registros: 50
Registros con brewery_type="micro": 50
Registros no conformes: 0
Assertions ejecutadas: 8
Assertions exitosas: 8
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 8. Muestra de la respuesta

Primeros 5 registros reales de la ejecución oficial, con un subconjunto de campos:

```json
[
  {
    "id": "aa7cbe9b-3a0f-4888-9884-6186b0042b55",
    "name": "’t Drankorgel",
    "brewery_type": "micro",
    "city": "Mol"
  },
  {
    "id": "1034754f-abf9-4b42-bd6d-37e110ba4b1a",
    "name": "'T Kroontje",
    "brewery_type": "micro",
    "city": "Lebbeke"
  },
  {
    "id": "5128df48-79fc-4f0f-8b52-d06be54d0cec",
    "name": "(405) Brewing Co",
    "brewery_type": "micro",
    "city": "Norman"
  },
  {
    "id": "9c5a66c8-cc13-416f-a5d9-0a769c87d318",
    "name": "(512) Brewing Co",
    "brewery_type": "micro",
    "city": "Austin"
  },
  {
    "id": "34e8c68b-6146-453f-a4b9-1f6cd99a5ada",
    "name": "1 of Us Brewing Company",
    "brewery_type": "micro",
    "city": "Mount Pleasant"
  }
]
```

El cuerpo completo (50 registros) se conserva en `evidencias/response-body.json`.

---

## 9. Validación del filtro

```text
Filtro solicitado: micro
Total evaluado: 50
Cumplen brewery_type="micro": 50
No cumplen: 0
```

**No existen registros no conformes.** Los 50 registros devueltos tienen el campo `brewery_type` presente, de tipo string y con valor literal `"micro"`. No aparecen valores alternativos (`brewpub`, `regional`, `large`, `microbrewery`, etc.).

---

## 10. Evidencias

```text
postman/TC-FUN-007.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-007-newman.json      (reporte JSON — ejecución oficial)
evidencias/TC-FUN-007-newman.txt       (salida de consola — ejecución oficial)
evidencias/TC-FUN-007-newman.html      (reporte HTML htmlextra — ejecución oficial)
evidencias/response-body.json          (cuerpo real — ejecución oficial)
evidencias/preflight-1-newman.json     (preflight — 8/8 PASS)
evidencias/preflight-1-newman.txt
TC-FUN-007_Informe.md
```

---

## 11. Resultado final

```text
Estado: APROBADO

Justificación:
En la ejecución oficial con Newman, GET /v1/breweries?by_type=micro respondió
200 OK con application/json y un arreglo JSON válido de 50 objetos. Los 50
registros contienen el campo brewery_type con valor "micro" (0 no conformes).
Las 8 assertions obligatorias se aprobaron (0 fallidas) y Newman terminó con
código de salida 0. El preflight dio el mismo resultado.
```

---

## 12. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-007.

---

## 13. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-007
Resultado obtenido: HTTP 200 OK. GET /v1/breweries?by_type=micro retornó un arreglo JSON con 50 registros. Se verificaron 50 registros: 50 presentan brewery_type="micro" y 0 no cumplen. Se ejecutaron 8 assertions: 8 aprobadas y 0 fallidas. Tiempo de respuesta: 355 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-007-newman.json (complementos: TC-FUN-007-newman.txt, TC-FUN-007-newman.html, response-body.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 06:09 UTC; exit code 0. Preflight previo 8/8 PASS. Único valor de brewery_type observado: "micro". Sin hallazgos.
```
