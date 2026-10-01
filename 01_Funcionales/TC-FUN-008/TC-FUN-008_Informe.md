# Informe de Ejecución — TC-FUN-008

## 1. Identificación

```text
Caso de prueba: TC-FUN-008
Nombre: Paginación personalizada
Tipo: Funcional
API: Open BreweryDB
Endpoint principal: GET /v1/breweries?page=2&per_page=5
Consulta de referencia: GET /v1/breweries?page=1&per_page=5
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T06:13:42.520Z (UTC) — 2026-10-01 01:13:42 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar que Open BreweryDB procesa los parámetros de paginación `page=2&per_page=5`: la página 2 debe responder `200 OK` con un arreglo JSON no vacío de **como máximo 5** registros con `id` válido (es decir, se respeta `per_page=5`), y la lista de IDs de la página 2 **no debe ser idéntica** a la de la página 1 obtenida en el mismo run con el mismo `per_page=5`. El solapamiento parcial de IDs se calcula solo como diagnóstico.

---

## 3. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en las 4 requests (preflight y oficial). |
| Disponibilidad de la API | Comprobada | `200 OK` en las 4 requests. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección válida | Comprobada | Validada con `JSON.parse` antes del preflight. |
| Environment válido | Comprobada | Validado con `JSON.parse`; `page1_ids` y `page1_count` inicialmente vacíos. |
| Sin IDs fijos | Comprobada | Búsqueda de patrones UUID en la colección: 0 coincidencias. El pre-request del Paso 1 vacía `page1_ids` y `page1_count` antes de cada run. |
| Independencia de otros casos | Comprobada | No se leyó ni reutilizó ningún archivo de otros casos. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET (ambas requests)
Request página 1: {{base_url}}/breweries?page=1&per_page=5
Request página 2: {{base_url}}/breweries?page=2&per_page=5   (request principal)
per_page: 5 (en ambas requests)
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Variables dinámicas: page1_ids, page1_count (vacías al inicio; asignadas en el Paso 1)
Número de ejecuciones: 2 runs (1 preflight + 1 oficial), cada uno con 2 requests; el estado se determina con el run oficial
```

---

## 5. Flujo ejecutado

```text
GET /v1/breweries?page=1&per_page=5        → 200 OK, 5 registros (320 ms)
        ↓
captura IDs página 1 → page1_ids (5 IDs)
        ↓
GET /v1/breweries?page=2&per_page=5        → 200 OK, 5 registros (84 ms)
        ↓
captura IDs página 2 (5 IDs)
        ↓
comparación → listas idénticas: No | IDs solapados: 0
```

---

## 6. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`, `page1_ids` vacío, `page1_count` vacío) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-008` con dos requests en orden obligatorio: Paso 1 (página 1 de referencia) y Paso 2 (página 2 personalizada). Se validaron ambos JSON y se comprobó que Newman estaba instalado.
2. **Preflight** (06:13:27Z UTC) — Se ejecutó el flujo completo. El Paso 1 usó `page=1&per_page=5` y el Paso 2 `page=2&per_page=5`. `page1_ids` se generó dinámicamente (5 IDs) y el Paso 2 lo consumió (los IDs de página 1 aparecen en el log del Paso 2). Resultado: 14 assertions, 0 fallidas, exit code 0. No hubo defectos de script. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Extracción de IDs** — En el run oficial, el script de tests del Paso 1 mapeó `page1Response` a sus `id` y guardó `page1_ids` (JSON) y `page1_count`. El Paso 2 leyó `page1_ids` y calculó `page2Ids` dentro de la assertion comparativa.
4. **Run oficial** (06:13:42.520Z → 06:13:43.106Z UTC), exit code `0`:
   ```bash
   newman run postman/TC-FUN-008.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-008" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-008-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-008-newman.html \
     > evidencias/TC-FUN-008-newman.txt 2>&1
   ```
5. **Evidencias** — Los cuerpos de ambas respuestas se extrajeron de `run.executions[0|1].response.stream` del reporte JSON oficial y se guardaron en `evidencias/pagina-1-response.json` y `evidencias/pagina-2-response.json`, solo con indentación.
6. **Assertions** — 6 en el Paso 1 y 8 en el Paso 2: 14 aprobadas, 0 fallidas; `run.failures` vacío. La comparación se recalculó a partir de los cuerpos guardados y coincide: listas idénticas = No, solapamiento = 0.
7. **Estado** — Se cumplen todas las condiciones del criterio de aprobación, por lo que el caso queda **APROBADO**.

---

## 7. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-FUN-008-newman.json`).

### Página 1 de referencia

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| PRE-1 | Código HTTP | 200 | 200 OK | PASS |
| PRE-2a | JSON válido | Sí | Sí | PASS |
| PRE-2b | Tipo de respuesta | Array | Array | PASS |
| PRE-3 | Máximo de registros | ≤ 5 | 5 | PASS |
| PRE-4 | Registros | > 0 | 5 | PASS |
| PRE-5 | `id` en todos los registros | String presente | 5 de 5 | PASS |

### Página 2 principal

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo de respuesta | Array | Array | PASS |
| 5 | `per_page=5` respetado | ≤ 5 | 5 | PASS |
| 6 | Registros | > 0 | 5 | PASS |
| 7 | `id` en todos los registros | String presente | 5 de 5 | PASS |
| 8 | Página 2 difiere de página 1 | Listas de IDs no idénticas | No idénticas (0 IDs en común) | PASS |

---

## 8. Resultados obtenidos

```text
Página 1
URL: https://api.openbrewerydb.org/v1/breweries?page=1&per_page=5
HTTP: 200 OK
Response Time: 320 ms
Cantidad: 5
IDs:
  ae7b3174-8be8-4d53-a3a5-9b8240970eea
  aa7cbe9b-3a0f-4888-9884-6186b0042b55
  1034754f-abf9-4b42-bd6d-37e110ba4b1a
  5128df48-79fc-4f0f-8b52-d06be54d0cec
  9c5a66c8-cc13-416f-a5d9-0a769c87d318

Página 2
URL: https://api.openbrewerydb.org/v1/breweries?page=2&per_page=5
HTTP: 200 OK
Content-Type: application/json
Response Time: 84 ms
Cantidad: 5
IDs:
  34e8c68b-6146-453f-a4b9-1f6cd99a5ada
  21f21cc0-5b2f-4b79-be29-3bc625bcc4c8
  6d14b220-8926-4521-8d19-b98a2d6ec3db
  e2e78bd8-80ff-4a61-a65c-3bfbd9d76ce2
  e432899b-7f58-455f-9c7b-9a6e2130a1e0

Comparación
Máximo permitido por per_page: 5
¿per_page respetado?: Sí (página 2 = 5 registros; página 1 = 5 registros)
¿Listas de IDs idénticas?: No
IDs solapados: ninguno
Cantidad de solapados: 0

Assertions totales: 14 (6 página 1 + 8 página 2)
Assertions exitosas: 14
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 9. Muestra de las respuestas

Muestra real del run oficial (subconjunto de campos).

**Página 1** (`page=1&per_page=5`), primeros 3 registros:

```json
[
  { "id": "ae7b3174-8be8-4d53-a3a5-9b8240970eea", "name": "'s", "brewery_type": "brewpub", "city": "Kronach" },
  { "id": "aa7cbe9b-3a0f-4888-9884-6186b0042b55", "name": "’t Drankorgel", "brewery_type": "micro", "city": "Mol" },
  { "id": "1034754f-abf9-4b42-bd6d-37e110ba4b1a", "name": "'T Kroontje", "brewery_type": "micro", "city": "Lebbeke" }
]
```

**Página 2** (`page=2&per_page=5`), primeros 3 registros:

```json
[
  { "id": "34e8c68b-6146-453f-a4b9-1f6cd99a5ada", "name": "1 of Us Brewing Company", "brewery_type": "micro", "city": "Mount Pleasant" },
  { "id": "21f21cc0-5b2f-4b79-be29-3bc625bcc4c8", "name": "1. Altenberger Brauhaus", "brewery_type": "brewpub", "city": "Oberasbach" },
  { "id": "6d14b220-8926-4521-8d19-b98a2d6ec3db", "name": "10 Barrel Brewing Co", "brewery_type": "large", "city": "Bend" }
]
```

Los cuerpos completos se conservan en `evidencias/pagina-1-response.json` y `evidencias/pagina-2-response.json`.

---

## 10. Comparación de páginas

| Posición | ID página 1 | ID página 2 | ¿Igual? |
|---|---|---|---|
| 1 | `ae7b3174-8be8-4d53-a3a5-9b8240970eea` | `34e8c68b-6146-453f-a4b9-1f6cd99a5ada` | No |
| 2 | `aa7cbe9b-3a0f-4888-9884-6186b0042b55` | `21f21cc0-5b2f-4b79-be29-3bc625bcc4c8` | No |
| 3 | `1034754f-abf9-4b42-bd6d-37e110ba4b1a` | `6d14b220-8926-4521-8d19-b98a2d6ec3db` | No |
| 4 | `5128df48-79fc-4f0f-8b52-d06be54d0cec` | `e2e78bd8-80ff-4a61-a65c-3bfbd9d76ce2` | No |
| 5 | `9c5a66c8-cc13-416f-a5d9-0a769c87d318` | `e432899b-7f58-455f-9c7b-9a6e2130a1e0` | No |

```text
Resultado de comparación global:
Página 2 difiere de página 1: Sí
(0 de 5 posiciones iguales; 0 IDs de página 2 presentes en página 1)
```

---

## 11. Evidencias

```text
postman/TC-FUN-008.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-008-newman.json      (reporte JSON — run oficial)
evidencias/TC-FUN-008-newman.txt       (salida de consola — run oficial)
evidencias/TC-FUN-008-newman.html      (reporte HTML htmlextra — run oficial)
evidencias/pagina-1-response.json      (cuerpo real de page=1&per_page=5 — run oficial)
evidencias/pagina-2-response.json      (cuerpo real de page=2&per_page=5 — run oficial)
evidencias/preflight-1-newman.json     (preflight — 14/14 PASS)
evidencias/preflight-1-newman.txt
TC-FUN-008_Informe.md
```

---

## 12. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman, la página 1 de referencia
(GET /v1/breweries?page=1&per_page=5) respondió 200 OK con 5 registros con id,
y la request principal GET /v1/breweries?page=2&per_page=5 respondió 200 OK
(application/json) con un arreglo JSON de 5 registros: no supera el máximo de 5,
así que se respeta per_page=5. Todos los registros tienen id. La lista de IDs de
la página 2 no es idéntica a la de la página 1 (0 IDs en común). Las 14
assertions se aprobaron (0 fallidas) y Newman terminó con código de salida 0. El
preflight dio el mismo resultado.
```

---

## 13. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-008.

> Observación (fuera del alcance de TC-FUN-008, no es hallazgo del caso): en la página 2 aparecen dos registros con el mismo `name` ("10 Barrel Brewing Co") y la misma `city` ("Bend") pero distinto `id` (`6d14b220-8926-4521-8d19-b98a2d6ec3db` y `e2e78bd8-80ff-4a61-a65c-3bfbd9d76ce2`). Podrían ser dos ubicaciones distintas o un posible duplicado de datos. TC-FUN-008 no valida la unicidad del contenido, por lo que no afecta al resultado. Se deja constancia por si se quiere revisar en pruebas de consistencia (TC-CON).

---

## 14. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-008
Resultado obtenido: HTTP 200 OK. GET /v1/breweries?page=2&per_page=5 retornó 5 registros, respetando el máximo de 5 elementos definido por per_page. La página 1 retornó 5 registros y la página 2 5. Las listas de IDs fueron diferentes (0 IDs en común). Se ejecutaron 14 assertions: 14 aprobadas y 0 fallidas. Tiempo de respuesta de página 2: 84 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-008-newman.json (complementos: TC-FUN-008-newman.txt, TC-FUN-008-newman.html, pagina-1-response.json, pagina-2-response.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 06:13 UTC; exit code 0. Página 1 obtenida en el mismo run (200 OK, 320 ms). Preflight previo 14/14 PASS. Sin hallazgos. La página 2 contiene dos registros "10 Barrel Brewing Co" (Bend) con IDs distintos (fuera del alcance funcional).
```
