# Informe de Ejecución — TC-FUN-006

## 1. Identificación

```text
Caso de prueba: TC-FUN-006
Nombre: Filtrado por Estado
Tipo: Funcional
API: Open BreweryDB
Endpoint: GET /v1/breweries?by_state=california
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora de ejecución: 2026-10-01T06:04:26.516Z (UTC) — 2026-10-01 01:04:26 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que Open BreweryDB procesa el filtro `by_state=california` en `GET /v1/breweries` y responde `200 OK` con un arreglo JSON no vacío de objetos en el que **todos** los registros tienen el campo `state` con valor `"California"` (comparación sin distinguir mayúsculas/minúsculas, sin modificar el valor recibido).

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
| Filtro exacto | Comprobada | Newman registra `"query": [{"key": "by_state", "value": "california"}]` como único parámetro. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries?by_state=california
URL final: https://api.openbrewerydb.org/v1/breweries?by_state=california
Filtro: by_state=california  (único parámetro; sin paginación ni filtros adicionales)
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 2 (1 preflight + 1 oficial); el estado se determina con la ejecución oficial
```

---

## 5. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-006` → request *TC-FUN-006 - Filtrado por Estado* (`GET {{base_url}}/breweries?by_state=california`) con las 8 assertions obligatorias y el diagnóstico por consola (cantidad, estados retornados y no conformes). Se validaron ambos JSON y se comprobó que Newman estaba instalado.
2. **Preflight** (06:04:10Z UTC) — `200 OK`, 791 ms, URL con `by_state=california`; 8 assertions, 0 fallidas, exit code 0. La respuesta se procesó correctamente y no hubo defectos de script, por lo que la colección no se modificó. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Ejecución oficial** (06:04:26.516Z → 06:04:26.938Z UTC), exit code `0`:
   ```bash
   newman run postman/TC-FUN-006.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-006" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-006-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-006-newman.html \
     > evidencias/TC-FUN-006-newman.txt 2>&1
   ```
4. **Captura del response body** — Se extrajo de `run.executions[0].response.stream` del reporte JSON oficial y se guardó en `evidencias/response-body.json`, solo con indentación. Se verificó que coincide exactamente con el cuerpo registrado por Newman.
5. **Evaluación de todos los registros** — Se recorrieron los 50 registros del cuerpo oficial con el mismo criterio de la assertion 8 (`state.toLowerCase() === "california"`): 50 cumplen y 0 no cumplen. Los 50 tienen `state` = `"California"` de forma literal, sin variantes de mayúsculas/minúsculas.
6. **Assertions** — 8 ejecutadas, 8 PASS, 0 FAIL; `run.failures` vacío. El diagnóstico de consola también reporta `Registros no conformes: 0`.
7. **Estado** — Se cumplen todas las condiciones del criterio de aprobación, por lo que el caso queda **APROBADO**.

---

## 6. Aserciones ejecutadas

Valores de la ejecución oficial (`evidencias/TC-FUN-006-newman.json`).

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo de respuesta | Array | Array | PASS |
| 5 | Registros | > 0 | 50 | PASS |
| 6 | Elementos | Objetos | 50 de 50 objetos | PASS |
| 7 | Campo `state` | Presente en todos | 50 de 50 con `state` string | PASS |
| 8 | Estado de todos los registros | California | 50 de 50 con `state` = `"California"` | PASS |

---

## 7. Resultados obtenidos

```text
URL final: https://api.openbrewerydb.org/v1/breweries?by_state=california
Método: GET
Filtro utilizado: by_state=california
HTTP: 200 OK
Content-Type: application/json
Response Time: 314 ms
Tamaño de respuesta: 21469 bytes
Cantidad de registros: 50
Registros con state="California": 50
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
    "id": "ef970757-fe42-416f-931d-722451f1f59c",
    "name": "10 Barrel Brewing Co",
    "city": "San Diego",
    "state": "California"
  },
  {
    "id": "5ae467af-66dc-4d7f-8839-44228f89b596",
    "name": "101 North Brewing Company",
    "city": "Petaluma",
    "state": "California"
  },
  {
    "id": "4788221a-a03b-458c-9084-4cadd69ade6d",
    "name": "14 Cannons Brewing Company",
    "city": "Westlake Village",
    "state": "California"
  },
  {
    "id": "fe6b9893-b93e-43d5-a9f6-3e0c89a3f13c",
    "name": "1850 Brewing Company",
    "city": "Mariposa",
    "state": "California"
  },
  {
    "id": "5ec3b488-48bd-49a7-9828-05bd90195cd5",
    "name": "2 Tread Brewing Co",
    "city": "Santa Rosa",
    "state": "California"
  }
]
```

El cuerpo completo (50 registros) se conserva en `evidencias/response-body.json`.

---

## 9. Validación del filtro

```text
Filtro solicitado: california
Total evaluado: 50
Cumplen state="California": 50
No cumplen: 0
```

**No existen registros no conformes.** Los 50 registros devueltos tienen el campo `state` presente, de tipo string y con valor literal `"California"`.

Nota sobre campos alternativos: el campo oficial evaluado es `state`, que está presente en todos los registros. La respuesta también incluye `state_province`, con valor `"California"` en los 50 registros. Ese campo no se usó como sustituto ni influye en el resultado.

---

## 10. Evidencias

```text
postman/TC-FUN-006.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-006-newman.json      (reporte JSON — ejecución oficial)
evidencias/TC-FUN-006-newman.txt       (salida de consola — ejecución oficial)
evidencias/TC-FUN-006-newman.html      (reporte HTML htmlextra — ejecución oficial)
evidencias/response-body.json          (cuerpo real — ejecución oficial)
evidencias/preflight-1-newman.json     (preflight — 8/8 PASS)
evidencias/preflight-1-newman.txt
TC-FUN-006_Informe.md
```

---

## 11. Resultado final

```text
Estado: APROBADO

Justificación:
En la ejecución oficial con Newman, GET /v1/breweries?by_state=california
respondió 200 OK con application/json y un arreglo JSON válido de 50 objetos.
Los 50 registros contienen el campo state con valor "California" (0 no
conformes). Las 8 assertions obligatorias se aprobaron (0 fallidas) y Newman
terminó con código de salida 0. El preflight dio el mismo resultado.
```

---

## 12. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-006.

---

## 13. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-006
Resultado obtenido: HTTP 200 OK. GET /v1/breweries?by_state=california retornó un arreglo JSON con 50 registros. Se verificaron 50 registros: 50 presentan state="California" y 0 no cumplen. Se ejecutaron 8 assertions: 8 aprobadas y 0 fallidas. Tiempo de respuesta: 314 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-006-newman.json (complementos: TC-FUN-006-newman.txt, TC-FUN-006-newman.html, response-body.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 06:04 UTC; exit code 0. Preflight previo 8/8 PASS. Se evaluó el campo state (presente en todos); state_province también vale "California" en los 50 registros, pero no se usó como sustituto. Sin hallazgos.
```
