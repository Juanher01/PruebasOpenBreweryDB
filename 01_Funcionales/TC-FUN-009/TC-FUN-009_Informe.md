# Informe de Ejecución — TC-FUN-009

## 1. Identificación

```text
Caso de prueba: TC-FUN-009
Nombre: Flujo de consulta encadenado
Tipo: Funcional
API: Open BreweryDB
Consulta inicial: GET /v1/breweries?by_state=california
Consulta final: GET /v1/breweries/{id}
Herramientas: Postman (colección v2.1 / Postman Runtime) + Newman 6.2.2
Fecha/hora: 2026-10-01T06:18:50.932Z (UTC) — 2026-10-01 01:18:50 hora local (UTC-5)
```

---

## 2. Objetivo

Verificar la coherencia entre una consulta filtrada y la consulta posterior por identificador. Dentro de un mismo run se obtiene `GET /v1/breweries?by_state=california`, se selecciona dinámicamente un registro, se consulta `GET /v1/breweries/{id}` con su `id` y se comprueba que el detalle responde `200 OK` como objeto JSON, que su `id` coincide con el solicitado y que el objeto completo es **profundamente igual** al elemento seleccionado del listado (ignorando solo el orden de las propiedades).

---

## 3. Precondiciones

| Precondición | Estado | Cómo se comprobó |
|---|---|---|
| Acceso a Internet | Comprobada | Newman recibió respuestas HTTP reales en las 4 requests (preflight y oficial). |
| Disponibilidad de la API | Comprobada | `200 OK` en las 4 requests. |
| Newman operativo | Comprobada | `newman -v` → `6.2.2`; reporter `htmlextra` disponible. |
| Postman (formato/motor) | Comprobada | Colección y environment en formato Postman v2.1, ejecutados con Postman Runtime a través de Newman. El agente no operó la GUI de Postman. |
| Colección válida | Comprobada | Validada con `JSON.parse` antes del preflight. |
| Environment válido | Comprobada | Validado con `JSON.parse`; `brewery_id` y `selected_brewery_snapshot` inicialmente vacíos. |
| Sin IDs fijos | Comprobada | Búsqueda de patrones UUID en la colección: 0 coincidencias. El pre-request del Paso 1 vacía `brewery_id` y `selected_brewery_snapshot` antes de cada run. |
| Independencia de otros casos | Comprobada | No se leyó ni reutilizó ningún archivo de otros casos. |

---

## 4. Configuración utilizada

```text
Base URL: https://api.openbrewerydb.org/v1   (variable {{base_url}})
Método: GET (ambas requests)
Filtro inicial: {{base_url}}/breweries?by_state=california   (único parámetro)
Endpoint de detalle: {{base_url}}/breweries/{{brewery_id}}
Autenticación: Ninguna
Headers personalizados / Body: Ninguno
Variables dinámicas: brewery_id, selected_brewery_snapshot (vacías al inicio; asignadas en el Paso 1)
Número de ejecuciones: 2 runs (1 preflight + 1 oficial), cada uno con 2 requests; el estado se determina con el run oficial
```

---

## 5. Flujo dinámico ejecutado

```text
GET /v1/breweries?by_state=california                    → 200 OK, 50 registros (331 ms)
        ↓
registro seleccionado = californiaResponse[0]  ("10 Barrel Brewing Co")
        ↓
ID = ef970757-fe42-416f-931d-722451f1f59c
        ↓
GET /v1/breweries/ef970757-fe42-416f-931d-722451f1f59c   → 200 OK (82 ms)
        ↓
comparación listado vs detalle → igualdad profunda: Sí (16 campos comparados, 0 diferencias)
```

Trazabilidad del ID (verificada sobre `evidencias/TC-FUN-009-newman.json`):

| Eslabón | Valor |
|---|---|
| ID del elemento seleccionado en el Paso 1 (`elemento-seleccionado.json`) | `ef970757-fe42-416f-931d-722451f1f59c` |
| ID almacenado en `brewery_id` (log del Paso 1) | `ef970757-fe42-416f-931d-722451f1f59c` |
| ID usado en la URL del Paso 2 (request registrada por Newman) | `ef970757-fe42-416f-931d-722451f1f59c` |
| ID retornado por el Paso 2 (`detalle-response.json`) | `ef970757-fe42-416f-931d-722451f1f59c` |
| ¿Los cuatro coinciden? | **Sí** |

---

## 6. Procedimiento ejecutado

1. **Preparación** — Se crearon `postman/` y `evidencias/`, el environment (`base_url`, `brewery_id` vacío, `selected_brewery_snapshot` vacío) y la colección *Open BreweryDB - Pruebas Funcionales* → carpeta `TC-FUN-009` con dos requests en el orden obligatorio. Se validaron ambos JSON y se comprobó que Newman estaba instalado. *Nota técnica:* el primer intento de generar los artefactos falló porque Bash no pudo interpretar el comando (heredoc); no se llegó a ejecutar nada ni a crear archivos. Los artefactos se generaron después con un script Node auxiliar, sin cambios en el contenido de la prueba.
2. **Preflight** (06:18:33Z UTC) — Se ejecutó el flujo completo. El Paso 1 usó `by_state=california`; el ID se obtuvo dinámicamente y el Paso 2 lo consumió en la URL. El snapshot se conservó correctamente (16 campos comparados, 0 diferencias). Resultado: 12 assertions, 0 fallidas, exit code 0. No hubo defectos de script. Evidencia: `evidencias/preflight-1-newman.*`.
3. **Selección** — En el run oficial, el script del Paso 1 tomó el primer registro disponible (`californiaResponse[0]`) y comprobó que fuera un objeto con `id` string no vacío.
4. **Almacenamiento del snapshot** — `pm.environment.set("brewery_id", selectedBrewery.id)` y `pm.environment.set("selected_brewery_snapshot", JSON.stringify(selectedBrewery))`, sin modificar el objeto.
5. **Consulta de detalle** — `GET https://api.openbrewerydb.org/v1/breweries/ef970757-fe42-416f-931d-722451f1f59c` → `200 OK`, 82 ms.
6. **Comparación** — La assertion oficial `pm.expect(detailResponse).to.deep.equal(selectedSnapshot)` se aprobó. El diagnóstico de campos (unión de claves de ambos objetos) dio 16 campos comparados y 0 diferencias. Como verificación adicional, se recalculó la comparación a partir de los archivos de evidencia y da el mismo resultado: 16/16 campos iguales, mismo orden de claves y serialización idéntica.
7. **Run oficial** (06:18:50.932Z → 06:18:51.534Z UTC), exit code `0`:
   ```bash
   newman run postman/TC-FUN-009.postman_collection.json \
     -e postman/OpenBreweryDB.postman_environment.json \
     --folder "TC-FUN-009" \
     -r cli,json,htmlextra \
     --reporter-json-export evidencias/TC-FUN-009-newman.json \
     --reporter-htmlextra-export evidencias/TC-FUN-009-newman.html \
     > evidencias/TC-FUN-009-newman.txt 2>&1
   ```
8. **Evidencias** — Se extrajeron de `run.executions[0|1].response.stream` del reporte JSON oficial: el listado completo, el elemento `[0]` del listado y el detalle. Se guardaron solo con indentación.
9. **Determinación del estado** — 12/12 assertions aprobadas; se cumplen todas las condiciones del criterio de aprobación, por lo que el caso queda **APROBADO**.

---

## 7. Aserciones ejecutadas

Valores del run oficial (`evidencias/TC-FUN-009-newman.json`).

### Paso 1 — Listado

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| PRE-1 | Código HTTP | 200 | 200 OK | PASS |
| PRE-2 | Content-Type | JSON | `application/json` | PASS |
| PRE-3 | JSON válido | Sí | Sí | PASS |
| PRE-4 | Tipo de respuesta | Array | Array | PASS |
| PRE-5 | Registros | > 0 | 50 | PASS |
| PRE-6 | Registro seleccionado con `id` válido | Objeto con `id` string no vacío | `ef970757-fe42-416f-931d-722451f1f59c` | PASS |

### Paso 2 — Detalle

| # | Validación | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| 1 | Código HTTP | 200 | 200 OK | PASS |
| 2 | Content-Type | JSON | `application/json` | PASS |
| 3 | JSON válido | Sí | Sí | PASS |
| 4 | Tipo de respuesta | Objeto (no Array) | Objeto (`Array.isArray` = false) | PASS |
| 5 | ID retornado = ID solicitado | `ef970757-fe42-416f-931d-722451f1f59c` | `ef970757-fe42-416f-931d-722451f1f59c` | PASS |
| 6 | Detalle = elemento seleccionado (igualdad profunda) | Igualdad completa | Igual (16/16 campos, 0 diferencias) | PASS |

---

## 8. Resultados obtenidos

```text
Listado:
URL: https://api.openbrewerydb.org/v1/breweries?by_state=california
HTTP: 200 OK
Response Time: 331 ms
Cantidad: 50
ID seleccionado: ef970757-fe42-416f-931d-722451f1f59c
Nombre seleccionado: 10 Barrel Brewing Co

Detalle:
URL: https://api.openbrewerydb.org/v1/breweries/ef970757-fe42-416f-931d-722451f1f59c
HTTP: 200 OK
Content-Type: application/json
Response Time: 82 ms
ID retornado: ef970757-fe42-416f-931d-722451f1f59c

Comparación:
ID coincide: Sí
Objeto completo coincide: Sí
Campos comparados: 16
Campos diferentes: 0
Assertions totales: 12 (6 Paso 1 + 6 Paso 2)
Assertions exitosas: 12
Assertions fallidas: 0
Exit code Newman: 0
Resultado global: Exitoso
```

---

## 9. Muestra del elemento seleccionado

Campos seleccionados de `evidencias/elemento-seleccionado.json` (elemento `[0]` del listado oficial):

```json
{
  "id": "ef970757-fe42-416f-931d-722451f1f59c",
  "name": "10 Barrel Brewing Co",
  "brewery_type": "large",
  "city": "San Diego",
  "state": "California",
  "country": "United States"
}
```

---

## 10. Muestra del detalle

Campos seleccionados de `evidencias/detalle-response.json`:

```json
{
  "id": "ef970757-fe42-416f-931d-722451f1f59c",
  "name": "10 Barrel Brewing Co",
  "brewery_type": "large",
  "city": "San Diego",
  "state": "California",
  "country": "United States"
}
```

---

## 11. Comparación listado vs detalle

```text
¿Coincidencia profunda?: Sí
```

**No existen diferencias.** Comparación campo a campo de los 16 campos (unión de claves de ambos objetos), con valores reales del run oficial:

| Campo | Valor listado | Valor detalle | ¿Coincide? |
|---|---|---|---|
| `id` | `ef970757-fe42-416f-931d-722451f1f59c` | `ef970757-fe42-416f-931d-722451f1f59c` | Sí |
| `name` | `10 Barrel Brewing Co` | `10 Barrel Brewing Co` | Sí |
| `brewery_type` | `large` | `large` | Sí |
| `address_1` | `1501 E St` | `1501 E St` | Sí |
| `address_2` | `null` | `null` | Sí |
| `address_3` | `null` | `null` | Sí |
| `city` | `San Diego` | `San Diego` | Sí |
| `state_province` | `California` | `California` | Sí |
| `postal_code` | `92101-6618` | `92101-6618` | Sí |
| `country` | `United States` | `United States` | Sí |
| `longitude` | `-117.129593` | `-117.129593` | Sí |
| `latitude` | `32.714813` | `32.714813` | Sí |
| `phone` | `6195782311` | `6195782311` | Sí |
| `website_url` | `http://10barrel.com` | `http://10barrel.com` | Sí |
| `state` | `California` | `California` | Sí |
| `street` | `1501 E St` | `1501 E St` | Sí |

---

## 12. Evidencias

```text
postman/TC-FUN-009.postman_collection.json
postman/OpenBreweryDB.postman_environment.json
evidencias/TC-FUN-009-newman.json               (reporte JSON — run oficial)
evidencias/TC-FUN-009-newman.txt                (salida de consola — run oficial)
evidencias/TC-FUN-009-newman.html               (reporte HTML htmlextra — run oficial)
evidencias/listado-california-response.json     (cuerpo real de GET ?by_state=california — run oficial)
evidencias/elemento-seleccionado.json           (elemento [0] del listado — run oficial)
evidencias/detalle-response.json                (cuerpo real de GET /breweries/{id} — run oficial)
evidencias/preflight-1-newman.json              (preflight — 12/12 PASS)
evidencias/preflight-1-newman.txt
TC-FUN-009_Informe.md
```

---

## 13. Resultado final

```text
Estado: APROBADO

Justificación:
En el run oficial con Newman, GET /v1/breweries?by_state=california respondió
200 OK con un arreglo JSON de 50 registros. Se seleccionó dinámicamente el
primero (id ef970757-fe42-416f-931d-722451f1f59c) y con ese mismo ID se ejecutó
GET /v1/breweries/ef970757-fe42-416f-931d-722451f1f59c, que respondió 200 OK
(application/json) con un objeto JSON cuyo id coincide con el solicitado. El
objeto del detalle es profundamente igual al elemento seleccionado del listado
(16 campos comparados, 0 diferencias). Las 12 assertions se aprobaron (0
fallidas) y Newman terminó con código de salida 0. El preflight dio el mismo
resultado.
```

---

## 14. Hallazgos

No se identificaron hallazgos durante la ejecución de TC-FUN-009.

---

## 15. Datos para registrar en Excel

### Registro para Excel

```text
ID: TC-FUN-009
Resultado obtenido: HTTP 200 OK en ambas solicitudes. Se obtuvo dinámicamente el ID ef970757-fe42-416f-931d-722451f1f59c desde GET /v1/breweries?by_state=california y se consultó GET /v1/breweries/ef970757-fe42-416f-931d-722451f1f59c. El ID retornado coincide con el solicitado y el objeto del detalle coincide con el elemento correspondiente del listado. Se ejecutaron 12 assertions: 12 aprobadas y 0 fallidas. Tiempo de respuesta del detalle: 82 ms.
Estado: APROBADO
Evidencia principal: evidencias/TC-FUN-009-newman.json (complementos: TC-FUN-009-newman.txt, TC-FUN-009-newman.html, listado-california-response.json, elemento-seleccionado.json, detalle-response.json)
Observaciones: Ejecución con Newman 6.2.2 el 2026-10-01 06:18 UTC; exit code 0. Listado: 200 OK, 50 registros, 331 ms. Igualdad profunda listado vs detalle: 16 campos comparados, 0 diferencias. Preflight previo 12/12 PASS. Sin hallazgos.
```
