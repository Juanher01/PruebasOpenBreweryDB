# Informe de Ejecución — TC-FUN-003

## 1. Identificación

```text
Caso de prueba: TC-FUN-003
Nombre: Búsqueda por nombre (Search)
Tipo: Funcional
API: Open BreweryDB
Endpoint: GET /v1/breweries/search?query=san
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T05:37:55.366Z (UTC) — 2026-10-01 00:37:55 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que `GET /v1/breweries/search?query=san` procesa el término `san` y retorna `200 OK` con un arreglo JSON no vacío de objetos de cervecerías, todos con `name`, y que **todos los nombres contienen `san`** (sin distinguir mayúsculas/minúsculas), tal como establece el resultado esperado del caso: *"Arreglo JSON con cervecerías que contengan 'san' en su nombre"*.

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
| Término `san` | Comprobada | La request registrada por Newman contiene `"query": [{"key": "query", "value": "san"}]`. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET
Endpoint: {{base_url}}/breweries/search?query=san
URL final: https://api.openbrewerydb.org/v1/breweries/search?query=san
Query: query=san  (único parámetro; sin paginación ni filtros adicionales)
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Número de ejecuciones: 3 (1 preflight + 1 oficial + 1 repetición de confirmación); el estado se determina con la ejecución oficial
```

---

## 5. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-003` → request *TC-FUN-003 - Búsqueda por nombre* (`GET {{base_url}}/breweries/search?query=san`) con las 8 assertions obligatorias y los datos de diagnóstico por consola. Se validaron ambos JSON y se comprobó que Newman estaba instalado.
2. **Preflight** (05:37:33Z UTC) — `200 OK`, 50 resultados, 695 ms. 8 assertions: 7 PASS y 1 FAIL (*Todos los nombres contienen "san"* → `expected 'g8 development, inc.' to include 'san'`). Se confirmó `query=san` y que la respuesta se procesaba bien. El fallo se debe al contenido real de la respuesta, **no a un defecto del script**, por lo que la colección no se modificó. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Ejecución oficial** (05:37:55.366Z → 05:37:56.191Z UTC), exit code `1`:
   ```bash
   newman run postman/TC-FUN-003.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-003" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-003-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-003-newman.html \
     > evidencias/TC-FUN-003-newman.txt 2>&1
   ```
4. **Repetición de confirmación** (05:37:57.720Z UTC), tal como exige el criterio de rechazo ante un comportamiento inesperado: `200 OK`, 50 resultados, 327 ms, 7 PASS / 1 FAIL con el mismo error; se devolvieron los mismos 50 IDs en el mismo orden que en la ejecución oficial. Evidencia: `evidencias/repeticion-1-newman.*`.
5. **Captura de respuesta** — Se extrajo el cuerpo de `run.executions[0].response.stream` del reporte JSON oficial y se guardó en `evidencias/response-body.json`, solo con indentación.
6. **Análisis** — Se evaluaron los 50 nombres del cuerpo oficial con el mismo criterio de la assertion (`name.toLowerCase().includes("san")`): 4 cumplen y 46 no. Como referencia diagnóstica, se observó que los 46 no conformes tienen una ciudad que empieza por "San".
7. **Estado** — Con la assertion obligatoria 8 fallida de forma reproducible y el servicio disponible, el caso queda **RECHAZADO**.

---

## 6. Aserciones ejecutadas

Valores de la ejecución oficial (`evidencias/TC-FUN-003-newman.json`).

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo | Array | Array | PASS |
| 5 | Resultados | > 0 | 50 | PASS |
| 6 | Elementos | Objetos | 50 de 50 objetos | PASS |
| 7 | Campo `name` | Presente en todos | 50 de 50 con `name` string | PASS |
| 8 | Correspondencia | Todos contienen `san` | 4 de 50 contienen `san`; 46 no (primer fallo: `G8 Development, Inc.`) | **FAIL** |

---

## 7. Resultados obtenidos

```text
URL final: https://api.openbrewerydb.org/v1/breweries/search?query=san
Método: GET
Query: query=san
HTTP: 200 OK
Content-Type: application/json
Response Time: 712 ms
Tamaño de respuesta: 21738 bytes
Cantidad de resultados: 50
Resultados que contienen "san": 4
Resultados que no contienen "san": 46
Assertions ejecutadas: 8
Assertions exitosas: 7
Assertions fallidas: 1
Exit code Newman: 1
Resultado global: Fallido (1 assertion obligatoria fallida)
```

Repetición de confirmación: `200 OK`, 327 ms, 50 resultados, 4 conformes / 46 no conformes, 7 PASS / 1 FAIL, exit code `1`.

---

## 8. Muestra de la respuesta

Cinco resultados reales de la ejecución oficial (posiciones 1, 2, 3, 35 y 48), con un subconjunto de campos:

```json
[
  {
    "id": "01b395ba-7b97-4214-a98c-365ad281d9dd",
    "name": "G8 Development, Inc.",
    "city": "San Diego"
  },
  {
    "id": "02131f19-7bde-422c-a363-9288b2df2a9b",
    "name": "South Bay Brewco",
    "city": "San Jose"
  },
  {
    "id": "0338af09-60df-4e16-9fd6-89d3033c9cc2",
    "name": "Deft Brewing",
    "city": "San Diego"
  },
  {
    "id": "28945428-2326-41b3-b2d9-97f6e8154783",
    "name": "Gordon Biersch Brewery Restaurant - San Diego",
    "city": "San Diego"
  },
  {
    "id": "38bb7b37-a035-4e52-bc15-a0ea83eaadce",
    "name": "San Fernando Brewing Co.",
    "city": "San Fernando"
  }
]
```

El cuerpo completo queda en `evidencias/response-body.json`.

---

## 9. Validación del término

```text
Término buscado: san
Cantidad de resultados: 50
Resultados cuyo nombre contiene "san": 4
Resultados que no cumplen: 46
```

Criterio aplicado (idéntico a la assertion 8): `name.toLowerCase().includes("san")`. La columna *Ciudad* se incluye solo como referencia diagnóstica; no forma parte del criterio.

| # | Nombre obtenido | ¿Contiene `san`? | Ciudad (referencia) |
|---|---|---|---|
| 1 | G8 Development, Inc. | **No** | San Diego |
| 2 | South Bay Brewco | **No** | San Jose |
| 3 | Deft Brewing | **No** | San Diego |
| 4 | Beach Chalet Brewing Co | **No** | San Francisco |
| 5 | Mike Hess Brewing - Miramar | **No** | San Diego |
| 6 | Clayton Brewing Co | **No** | San Dimas |
| 7 | Little Miss Brewing | **No** | San Diego |
| 8 | Second Chance Beer Company | **No** | San Diego |
| 9 | Ogopogo Brewing | **No** | San Gabriel |
| 10 | Speakeasy Ales and Lagers | **No** | San Francisco |
| 11 | Ballast Point Brewing Company | **No** | San Diego |
| 12 | Brew Rebellion | **No** | San Bernardino |
| 13 | Mission Brewery | **No** | San Diego |
| 14 | Oda Restaurant | **No** | San Francisco |
| 15 | Pizza Port Ocean Beach | **No** | San Diego |
| 16 | Thorn Brewing Co | **No** | San Diego |
| 17 | Helm's Brewing Company, LLC | **No** | San Diego |
| 18 | Ocean Beach Brewery | **No** | San Diego |
| 19 | Citizen Brewers | **No** | San Diego |
| 20 | Artifex Brewing Company | **No** | San Clemente |
| 21 | Port Brewing Co / The Lost Abbey | **No** | San Marcos |
| 22 | Zero One Ale House | **No** | San Angelo |
| 23 | Alpine Beer Company | **No** | San Diego |
| 24 | Circle 9 Brewing | **No** | San Diego |
| 25 | Wild Barrel Brewing Company | **No** | San Marcos |
| 26 | Modern Times - The Dankness Dojo | **No** | San Diego |
| 27 | Longship Brewery | **No** | San Diego |
| 28 | Pariah Brewing Company | **No** | San Diego |
| 29 | California Wild Ales | **No** | San Diego |
| 30 | Palmia | **No** | San Francisco |
| 31 | Anchor Brewing Co | **No** | San Francisco |
| 32 | Dorcol Distilling and Brewing CO | **No** | San Antonio |
| 33 | Barrel Head Brewhouse | **No** | San Francisco |
| 34 | Black Hammer Brewing | **No** | San Francisco |
| 35 | Gordon Biersch Brewery Restaurant - San Diego | Sí | San Diego |
| 36 | North Park Beer Co. | **No** | San Diego |
| 37 | Weathered Souls Brewing Co. | **No** | San Antonio |
| 38 | Acoustic Ales Brewing Experiment | **No** | San Diego |
| 39 | Sunset Reservoir Brewing Company | **No** | San Francisco |
| 40 | Busted Sandal Brewing Company | Sí | San Antonio |
| 41 | Bitter Brothers Brewing Co. | **No** | San Diego |
| 42 | New English Brewing Co Inc | **No** | San Diego |
| 43 | Automatic Brewing Co. / Blind Lady Alehouse | **No** | San Diego |
| 44 | Southern Pacific Brewing | **No** | San Francisco |
| 45 | Longtab Brewing Company LLC | **No** | San Antonio |
| 46 | Hillcrest Brewing Company | **No** | San Diego |
| 47 | Mikkeller Brewing San Diego | Sí | San Diego |
| 48 | San Fernando Brewing Co. | Sí | San Fernando |
| 49 | 32 North Brewing Co | **No** | San Diego |
| 50 | Ballast Point Brewing Co / Home Brew Mart | **No** | San Diego |

---

## 10. Evidencias

```text
postman/TC-FUN-003.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-003-newman.json      (reporte JSON — ejecución oficial)
evidencias/TC-FUN-003-newman.txt       (salida de consola — ejecución oficial)
evidencias/TC-FUN-003-newman.html      (reporte HTML htmlextra — ejecución oficial)
evidencias/response-body.json          (cuerpo real — ejecución oficial)
evidencias/preflight-1-newman.json     (preflight — 7 PASS / 1 FAIL)
evidencias/preflight-1-newman.txt
evidencias/repeticion-1-newman.json    (repetición de confirmación — 7 PASS / 1 FAIL)
evidencias/repeticion-1-newman.txt
TC-FUN-003_Informe.md
```

---

## 11. Resultado final

```text
Estado: RECHAZADO

Justificación:
El servicio estuvo disponible: GET /v1/breweries/search?query=san respondió
200 OK con un arreglo JSON de 50 objetos, todos con name. Sin embargo, solo 4
de los 50 nombres contienen "san" (sin distinguir mayúsculas/minúsculas); los
otros 46 no, de modo que la assertion obligatoria 'Todos los nombres contienen
"san"' falló. El resultado esperado del caso ("cervecerías que contengan 'san'
en su nombre") no se cumple. El comportamiento se reprodujo de forma idéntica en
el preflight, en la ejecución oficial y en la repetición de confirmación (mismos
50 IDs; 4 conformes / 46 no conformes en cada una). Ejecución oficial: 8
assertions, 7 aprobadas, 1 fallida, exit code 1.
```

---

## 12. Hallazgos

```text
Descripción: El endpoint de búsqueda GET /v1/breweries/search?query=san devuelve
cervecerías cuyo nombre no contiene el término buscado.

Esperado: Arreglo JSON con cervecerías que contengan "san" en su nombre (todos los
elementos con name que incluya "san", sin distinguir mayúsculas/minúsculas).

Obtenido: Arreglo JSON de 50 elementos; 4 nombres contienen "san" y 46 no
(p. ej. "G8 Development, Inc.", "South Bay Brewco", "Deft Brewing",
"Anchor Brewing Co"). La lista completa está en la sección 9.

Registros afectados: 46 de 50 (los marcados "No" en la tabla de la sección 9).

Reproducibilidad: Reproducible, 3 de 3 ejecuciones (preflight 05:37:33Z, oficial
05:37:55Z y repetición 05:37:57Z UTC), con los mismos 50 IDs en el mismo orden y el
mismo reparto 4 / 46.

Impacto: La assertion principal de TC-FUN-003 falla y el caso se marca RECHAZADO.
La búsqueda no restringe los resultados al nombre de la cervecería.

Observación diagnóstica (no verificada contra documentación): los 46 registros no
conformes tienen todos una ciudad que empieza por "San" (San Diego 26, San
Francisco 9, San Antonio 3, San Marcos 2, San Jose, San Dimas, San Gabriel, San
Bernardino, San Clemente y San Angelo 1 cada una). Esto sugiere que la búsqueda
también busca en otros campos, como la ciudad. Hay que decidir si es un defecto del
servicio o si el resultado esperado del caso debe revisarse; esa decisión no
corresponde a esta ejecución, y el caso no se modificó.
```

---

## 13. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-003
Resultado obtenido: HTTP 200 OK. GET /v1/breweries/search?query=san retornó un arreglo JSON con 50 resultados. Se verificaron 50 nombres: 4 contienen "san" y 46 no cumplen. Se ejecutaron 8 assertions: 7 aprobadas y 1 fallida. Tiempo de respuesta: 712 ms.
Estado: RECHAZADO
Evidencia principal: evidencias/TC-FUN-003-newman.json (complementos: TC-FUN-003-newman.txt, TC-FUN-003-newman.html, response-body.json, repeticion-1-newman.json)
Observaciones: Fallo reproducible en 3 de 3 ejecuciones (mismos 50 IDs). Los 46 resultados no conformes tienen una ciudad que empieza por "San" (San Diego, San Francisco, San Antonio, etc.), lo que indica que la búsqueda no se limita al nombre. Ejecución con Newman 6.2.2 el 2026-10-01 05:37 UTC; exit code 1.
```
