# Informe Consolidado de QA — Open BreweryDB

> Documento de consolidación. Se elaboró **solo a partir de archivos existentes** (plan, informes individuales y evidencias técnicas). No se reejecutó ninguna prueba ni se modificó, movió o eliminó ningún artefacto. Las rutas son relativas a `06_Consolidado/`, salvo los documentos externos al repositorio, que se indican con ruta absoluta.

---

## 1. Información general

| Campo | Valor |
|---|---|
| Proyecto | Pruebas de API — Open BreweryDB (`https://api.openbrewerydb.org/v1`) |
| Repositorio | `https://github.com/Juanher01/PruebasOpenBreweryDB` (rama `main`; último commit analizado `3c79a0a`) |
| Autores del plan | Samuel Alexander Perdomo Fajardo y Juan Esteban Hernández Lozano (según `PLAN DE PRUEBAS (1).docx`) |
| Plan de pruebas localizado | `C:\Users\yoloh\Downloads\PLAN DE PRUEBAS (1).docx` — "Versión 1.0", fecha 27/08/2026. **Fuera del repositorio; no corresponde a la versión definitiva en los criterios de rendimiento** (ver §9 y §8.3) |
| Matriz de resultados | **No localizada** (ver §9) |
| Periodo de ejecución (evidencias) | 2026-10-01 03:19 UTC → 2026-10-01 16:02 UTC |
| Fecha de consolidación | 2026-10-01 |

**Fuentes utilizadas, en orden de prioridad:**
1. Plan de Pruebas: solo se encontró la v1.0, externa al repositorio. Los criterios vigentes de rendimiento se tomaron de la definición de la tarea de consolidación (§7).
2. Matriz de resultados: no disponible.
3. Informes individuales: 18 archivos `*_Informe.md`.
4. Evidencias técnicas: Newman JSON/TXT/HTML, cuerpos de respuesta, JSON Schemas, JTL, logs, Dashboards y JMX de JMeter, y los reportes HTML de Newman de TC-VAL y TC-ERR.

---

## 2. Objetivo

Consolidar el resultado de la campaña de pruebas de la API pública Open BreweryDB, que abarca pruebas funcionales, validación de entradas, manejo de errores, contrato y consistencia, y rendimiento. El consolidado presenta, para cada caso, su estado y su evidencia rastreable, y señala las inconsistencias detectadas entre plan, informes y evidencias.

---

## 3. Alcance ejecutado

El plan v1.0 define **28 casos** en 5 tipos. Los 28 tienen evidencia de ejecución en el repositorio.

| Tipo | IDs | Ubicación | Estructura de evidencia |
|---|---|---|---|
| Funcionales | TC-FUN-001 … TC-FUN-009 | `../01_Funcionales/TC-FUN-00x/` | Por caso: informe `.md`, colección Postman, Newman JSON/TXT/HTML y cuerpos de respuesta |
| Validación de entradas | TC-VAL-001 … TC-VAL-005 | `../02_Validacion_Entradas/` | **Por grupo**: una colección Postman y un reporte HTML de Newman con los 5 casos. Subcarpetas `TC-VAL-00x/` vacías (`.gitkeep`). **Sin informes individuales** |
| Manejo de errores | TC-ERR-001 … TC-ERR-005 | `../03_Manejo_Errores/` | **Por grupo**: una colección Postman y un reporte HTML de Newman con los 5 casos. Subcarpetas `TC-ERR-00x/` vacías (`.gitkeep`). **Sin informes individuales** |
| Contrato y consistencia | TC-CON-001 … TC-CON-004 | `../04_Contrato_Consistencia/TC-CON-00x/` | Por caso: informe, colección, JSON Schema (CON-001/002/004) y evidencias Newman |
| Rendimiento | TC-REN-001 … TC-REN-005 | `../05_Rendimiento/TC-REN-00x/` | Por caso: informe y evidencias Newman (001–003) o JMeter (004–005) |

Las estructuras difieren porque las pruebas las desarrollaron dos integrantes (commit `37e7bf5` "Trabajo de Chayanne (Samuel)" para TC-VAL/TC-ERR). Los casos se identificaron por ID, nombre de request y URL.

---

## 4. Metodología y herramientas

| Herramienta | Uso real (según evidencias) |
|---|---|
| Postman (formato de colección v2.1) | Definición de requests, variables y assertions Chai (`pm.expect`) en todos los casos FUN, VAL, ERR, CON y REN-001 a 003 |
| Newman 6.2.2 (Node.js v22.15.1) | Ejecución headless; reporters `cli`, `json` y `htmlextra` (FUN, CON, REN-001 a 003). TC-VAL y TC-ERR conservan solo el reporte HTML ("Newman Summary Report") |
| AJV / JSON Schema draft-07 | Validación de contrato dentro del sandbox de Newman (`require("ajv")`) en TC-CON-001, 002 y 004 |
| Apache JMeter 5.6.3 (Java 22), modo no-GUI | TC-REN-004 (10 hilos, 1 loop, Synchronizing Timer) y TC-REN-005 (10 hilos, 60 s, loop continuo); JTL CSV y Dashboard HTML |
| Scripts auxiliares (Node.js / Python) | Solo cálculo de métricas sobre evidencia ya generada (`calcular_metricas.js` / `.py`); no hacen peticiones HTTP |

Práctica aplicada en los casos con informe individual:
- **Preflight** separado de la ejecución oficial.
- **Ejecución oficial única** para determinar el estado.
- **Repetición de confirmación** ante fallos (TC-FUN-003 y TC-FUN-004).
- **IDs obtenidos dinámicamente**, sin IDs fijos.
- **Ambiente:** Windows 11 (build 10.0.26200). Las mediciones son end-to-end desde el equipo local; el tipo de conexión y la ubicación no están verificados.

---

## 5. Resumen general

| Indicador | Cantidad |
|---|---:|
| Casos planificados (plan v1.0) | 28 |
| Casos con evidencia de ejecución | 28 |
| Casos con informe individual y estado formal | 18 |
| — APROBADO | 16 |
| — RECHAZADO | 2 (TC-FUN-003, TC-FUN-004) |
| — BLOQUEADO | 0 |
| Casos ejecutados **sin informe ni estado formal** | 10 (TC-VAL-001…005, TC-ERR-001…005) |

**No se asigna un estado formal a TC-VAL ni a TC-ERR** porque no existe informe individual ni matriz que lo declare. En la §6 se reporta su resultado observado en la evidencia (assertions PASS/FAIL), sin convertirlo en APROBADO o RECHAZADO.

---

## 6. Resultados por tipo de prueba

### 6.1 Funcionales (9/9 con informe — 7 APROBADO, 2 RECHAZADO)

| ID | Escenario | Estado | Resultado (informe) |
|---|---|---|---|
| TC-FUN-001 | Listado general | APROBADO | HTTP 200; array de 50 objetos; 6/6 assertions; 323 ms |
| TC-FUN-002 | Detalle por ID dinámico | APROBADO | ID `ae7b3174-…eea` coincide en listado, URL y detalle; 14/14; 90 ms |
| TC-FUN-003 | Búsqueda `query=san` | **RECHAZADO** | 50 resultados; solo 4 nombres contienen "san" y 46 no; 7/8; reproducido 3/3 |
| TC-FUN-004 | Cervecería aleatoria | **RECHAZADO** | `/random` devolvió un **arreglo de 1 elemento**, no un objeto único; 3/8; reproducido 3/3 (ver §8.2) |
| TC-FUN-005 | Metadatos | APROBADO | `total`=11848, `page`=1, `per_page`=50; 8/8 |
| TC-FUN-006 | Filtro `by_state=california` | APROBADO | 50/50 con `state`="California"; 8/8 |
| TC-FUN-007 | Filtro `by_type=micro` | APROBADO | 50/50 con `brewery_type`="micro"; 8/8 |
| TC-FUN-008 | Paginación `page=2&per_page=5` | APROBADO | 5 registros; listas de IDs de páginas 1 y 2 distintas (0 en común); 14/14 |
| TC-FUN-009 | Flujo encadenado | APROBADO | Detalle profundamente igual al elemento del listado (16 campos, 0 diferencias); 12/12 |

### 6.2 Validación de entradas (5/5 ejecutados — sin informe individual)

Evidencia: `../02_Validacion_Entradas/BreweriesValidacion-2026-10-01-05-24-17-632-0.html` (run del 01/10/2026 00:24, hora del reporte; 5 requests y 12 assertions, de las que 4 fallaron).

| ID | Request ejecutada (según reporte) | HTTP | Assertions | Observación |
|---|---|---:|---|---|
| TC-VAL-001 | `GET /v1/breweries?by_state=texas` | 200 | 3/3 PASS | — |
| TC-VAL-002 | `GET https://api.openbrewerydb.org//v1/breweries?by_type=xyz` | 404 | 0/2 (ambas FAIL) | URL ejecutada con **doble barra** `//v1`; la colección del repositorio tiene `/v1` (ver §8.4) |
| TC-VAL-003 | `GET /v1/breweries/search?query=` | 200 | 1/2 | La API devolvió el objeto de bienvenida (`message`, `documentation_url`, `mcp_url`); la assertion esperaba un array |
| TC-VAL-004 | `GET /v1/breweries?by_city=atlantida` | 200 | 2/2 PASS | Array vacío |
| TC-VAL-005* | `GET /v1/breweries/search?query=%20%25%26` | 200 | 2/3 | Sin error 500; la API devolvió el objeto de bienvenida y la assertion esperaba array u objeto según el código |

\* La request no tiene ID en su nombre ("Caracteres especiales en búsqueda"); se asoció a TC-VAL-005 por escenario y URL, que coinciden con el plan.

### 6.3 Manejo de errores (5/5 ejecutados — sin informe individual)

Evidencia: `../03_Manejo_Errores/BreweriesManejoErrores-2026-10-01-05-42-49-780-0.html` (run del 01/10/2026 00:42; 5 requests y 8 assertions, de las que 2 fallaron, más 1 error de script).

| ID | Request | HTTP | Assertions | Observación |
|---|---|---:|---|---|
| TC-ERR-001 | `GET /v1/breweries/00000000-0000-0000-0000-000000000000` | 404 | 1/2 | Código correcto; el cuerpo es una página HTML "Not Found" y la assertion esperaba cuerpo vacío |
| TC-ERR-002 | `GET /v1/breweries/12345` | 404 | 1/2 | Código dentro de 400/404; cuerpo HTML, no JSON |
| TC-ERR-003 | `GET /v1/beers` | 404 | 2/2 PASS | — |
| TC-ERR-004 | `POST /v1/breweries` | 405 | **0 evaluadas** | `SyntaxError` en el script de test (carácter `s` sobrante tras `oneOf([405, 404]);` en la colección); el 405 observado no fue validado por assertions |
| TC-ERR-005 | `GET /v2/breweries` | 404 | 2/2 PASS | — |

### 6.4 Contrato y consistencia (4/4 con informe — 4 APROBADO)

| ID | Escenario | Estado | Resultado (informe) |
|---|---|---|---|
| TC-CON-001 | Campos obligatorios | APROBADO | 6/6 campos presentes; AJV PASS; 16/16 |
| TC-CON-002 | Tipos de datos | APROBADO | `id`/`name` string; `latitude`/`longitude` **number** (contrato evaluado: Number/Null); AJV PASS — ver §8.2 |
| TC-CON-003 | Listado vs detalle | APROBADO | Igualdad profunda; 16 propiedades y 0 diferencias |
| TC-CON-004 | Estructura de metadatos | APROBADO | `total`/`page`/`per_page` enteros; propiedades adicionales `by_state`, `by_country` y `by_type` **permitidas por el contrato revisado**; AJV PASS — ver §8.2 |

### 6.5 Rendimiento (5/5 con informe — 5 APROBADO)

Resumen en la §7; detalle en `02_Resumen_Rendimiento.md`.

---

## 7. Resultados de rendimiento

Criterios vigentes (versión definitiva indicada para la consolidación). Se verificó que los 5 informes vigentes los aplican.

| ID | Criterio vigente | Resultado real | Estado | ¿Informe compatible? |
|---|---|---|---|---|
| TC-REN-001 | Response Time < 2000 ms | 316 ms (HTTP 200) | APROBADO | Sí |
| TC-REN-002 | Response Time < 1500 ms | 331 ms (HTTP 200, `query=san`) | APROBADO | Sí |
| TC-REN-003 | 50 secuenciales, 100 % HTTP 200, P95 < 2000 ms | 50/50 HTTP 200; P95 = 259 ms (nearest-rank, posición 48) | APROBADO | Sí (informe actualizado, commit `dae6dcb`) |
| TC-REN-004 | 10 hilos; ≥ 95 % < 3000 ms; 0 % errores | 10/10 HTTP 200; 100 % < 3000 ms; P95 = 624 ms | APROBADO | Sí |
| TC-REN-005 | 10 hilos × 60 s; ≥ 99.18 req/s; 100 % HTTP 200; 0 % HTTP 429 | 103.31 req/s; 6200/6200 HTTP 200; 0 HTTP 429 | APROBADO | Sí (informe actualizado, commit `dae6dcb`) |

Las versiones anteriores de TC-REN-003 y TC-REN-005, ejecutadas con los criterios del plan v1.0 (desviación estándar sin umbral y línea base sin mínimo), **no se usan como definitivas**. Se conservan en el historial de git (commit `0b9d9b2`).

---

## 8. Hallazgos relevantes

### 8.1 Hallazgos sobre el servicio (documentados en informes)

| # | Caso | Hallazgo | Reproducibilidad |
|---|---|---|---|
| H-1 | TC-FUN-003 | `GET /v1/breweries/search?query=san` devuelve 46 de 50 registros cuyo nombre no contiene "san". Los 46 tienen ciudad que empieza por "San", lo que sugiere que la búsqueda considera otros campos, como la ciudad (observación diagnóstica del informe) | 3/3 ejecuciones |
| H-2 | TC-FUN-004 | `GET /v1/breweries/random` devuelve un **arreglo de 1 elemento**; el paquete ejecutado esperaba un objeto único (ver §8.2) | 3/3 ejecuciones |

Observaciones de datos, fuera del alcance de los casos y no tratadas como hallazgos: el registro `ae7b3174-…` tiene `name` = `'s` (TC-FUN-002 y TC-CON-001/002/003), y la página 2 de TC-FUN-008 contiene dos registros "10 Barrel Brewing Co" en Bend con IDs distintos.

### 8.2 Discrepancias entre el plan localizado (v1.0) y los criterios aplicados en los informes

**Requieren decisión del equipo. No se resuelven en este consolidado.**

| Caso | Plan v1.0 (`PLAN DE PRUEBAS (1).docx`) | Criterio aplicado en el informe | Impacto |
|---|---|---|---|
| TC-FUN-004 | "Arreglo JSON con **un solo elemento** aleatorio" | "Objeto JSON único… no un arreglo" | El informe es **RECHAZADO**. La respuesta observada (arreglo de 1 elemento) coincidiría con la redacción del plan v1.0. El estado depende de cuál sea el resultado esperado vigente |
| TC-CON-002 | `latitude`/`longitude` (**String**/Null) | Number/Null | El informe es **APROBADO** con valores numéricos. Con la redacción del plan v1.0 esos valores **no** cumplirían |
| TC-CON-004 | "estrictamente total, page, per_page" | Contrato revisado: campos mínimos; adicionales permitidos | El informe vigente es **APROBADO**. Una ejecución previa con contrato estricto resultó RECHAZADA (según la nota del propio informe), pero **su evidencia no se conservó**: no está en git ni en la carpeta |
| TC-REN-003 / TC-REN-005 | Desviación "baja" sin umbral / línea base sin mínimo | P95 < 2000 ms / ≥ 99.18 req/s | Coinciden con la versión definitiva indicada para la consolidación, que **no se localizó como documento** |

### 8.3 Documentación faltante

- **Plan definitivo:** no está en el repositorio. El único plan de Open BreweryDB localizado (v1.0, externo) no contiene los criterios vigentes de TC-REN-003 y TC-REN-005.
- **Matriz de resultados:** no localizada. Fuera del repositorio solo hay una plantilla vacía (`C:\Users\yoloh\Downloads\Plantilla CasosPruebas.xlsx`, solo encabezados y responsable) y tres CSV `Casos_Prueba(Matriz de Trazabilidad)*.csv` de otro proyecto (SGPMP). **No se pudo contrastar el estado consolidado contra una matriz.**
- **TC-VAL-001 a 005 y TC-ERR-001 a 005:** sin informe individual. Los fallos observados no tienen análisis ni clasificación documentados.

### 8.4 Inconsistencias en la evidencia de TC-VAL y TC-ERR

- **TC-VAL-002:** el reporte HTML muestra la URL `https://api.openbrewerydb.org//v1/breweries?by_type=xyz` (doble barra), que respondió con una página HTML 404. La colección versionada contiene `https://api.openbrewerydb.org/v1/breweries?by_type=xyz`. **La evidencia no corresponde a la colección actual**, así que el resultado no permite evaluar el comportamiento real del parámetro `by_type=xyz`.
- **TC-ERR-004:** la colección contiene un error de sintaxis (`…oneOf([405, 404]);s`) que impidió evaluar las assertions. El código observado, 405, coincide con el esperado (405/404), pero no quedó validado automáticamente.
- **TC-VAL-003:** el plan especifica `GET /v1/breweries/search` sin parámetro, pero se ejecutó `GET /v1/breweries/search?query=` (parámetro vacío).
- **TC-VAL-005:** la request no lleva el ID del caso en su nombre.

---

## 9. Limitaciones

1. **Plan y matriz:** la versión definitiva del plan y la matriz de resultados no están en el repositorio ni se localizaron. Los criterios de rendimiento vigentes se tomaron de la definición de la tarea de consolidación.
2. **TC-VAL y TC-ERR:** solo hay un reporte HTML por grupo. No hay JSON de Newman, cuerpos de respuesta en archivo ni informes. El resultado observado se extrajo del HTML.
3. **Medición end-to-end** desde un único equipo Windows. La ubicación del runner y el tipo de conexión no están verificados, y los tiempos incluyen red, DNS y TLS.
4. **Datos vivos:** Open BreweryDB es un servicio público con datos cambiantes; los IDs y conteos corresponden al momento de cada ejecución.
5. **JMeter 5.6.3** se instaló fuera del repositorio (`C:\tools\apache-jmeter-5.6.3`) durante TC-REN-004, con autorización y verificación SHA-512 según su informe.
6. El **preflight en la GUI de Postman** no se realizó en TC-FUN-001 (se hizo con Newman, según su informe).

---

## 10. Cumplimiento de criterios de finalización

Criterios de finalización del plan v1.0, evaluados contra la evidencia:

| Criterio | Evaluación | Estado |
|---|---|---|
| 100 % de casos críticos (TC-FUN y TC-ERR) ejecutados al menos una vez | TC-FUN 9/9 con evidencia; TC-ERR 5/5 con evidencia Newman. En TC-ERR-004 no se evaluaron assertions | Cumple en ejecución, con la salvedad de TC-ERR-004 |
| ≥ 95 % de casos totales ejecutados | 28/28 con evidencia de ejecución (100 %) | Cumple |
| 0 hallazgos críticos sin documentar | Los fallos de TC-VAL-002/003/005 y TC-ERR-001/002/004 **no están analizados ni clasificados en ningún informe** | **No cumple / pendiente** |
| Latencia individual: REN-001 < 2000 ms y REN-002 < 1500 ms | 316 ms y 331 ms | Cumple |
| P95 en ejecución múltiple (REN-003 y REN-004) | 259 ms (< 2000 ms) y 624 ms (100 % < 3000 ms) | Cumple |
| Carga moderada: ≥ 95 % < 3000 ms y 0 % errores (REN-004) | 100 % < 3000 ms; 0 % errores | Cumple |
| Sin rate limiting sostenido (REN-005) | 0 HTTP 429 en 6200 muestras | Cumple |
| Contrato validado (TC-CON) | 4/4 APROBADO según informes, pero CON-002 y CON-004 aplican un contrato distinto del plan v1.0 (§8.2) | Cumple según informes; **pendiente de confirmar el contrato vigente** |
| Informe final con recomendación Go/No-Go | Este consolidado. **No se emite Go/No-Go definitivo** por los puntos pendientes (§11) | Parcial |

---

## 11. Conclusiones

1. **Cobertura:** los 28 casos planificados tienen evidencia de ejecución. Los 18 casos con informe individual dan 16 APROBADO, 2 RECHAZADO y 0 BLOQUEADO.
2. **Funcionalidad:** el listado, el detalle, los metadatos, los filtros por estado y tipo, la paginación y el flujo encadenado funcionan según los informes. Hay dos defectos reproducibles: la búsqueda por nombre devuelve resultados que no contienen el término (TC-FUN-003), y `/random` devuelve un arreglo de un elemento (TC-FUN-004), cuya calificación depende del resultado esperado vigente.
3. **Contrato:** los campos obligatorios, la consistencia entre listado y detalle y los tipos numéricos de las coordenadas se cumplen según los contratos aplicados. Hay que confirmar si el contrato vigente de TC-CON-002 (Number frente a String) y de TC-CON-004 (estricto frente a mínimo) es el aplicado en los informes.
4. **Rendimiento:** los 5 casos cumplen los criterios vigentes, con márgenes amplios. No se observó rate limiting (HTTP 429) con 10 hilos a unos 103 req/s.
5. **Validación de entradas y errores:** se ejecutaron, pero **no tienen informe ni estado formal**. Su evidencia presenta inconsistencias (TC-VAL-002 con URL distinta de la colección y TC-ERR-004 con error de script) que impiden concluir sobre esos casos sin corregir y reejecutar, lo que queda fuera del alcance de este consolidado.
6. **Recomendación:** antes de emitir el Go/No-Go se debe (a) localizar o versionar en el repositorio el plan definitivo y la matriz de resultados, (b) resolver las discrepancias de la §8.2, y (c) documentar y, si procede, corregir los casos TC-VAL y TC-ERR.

---

## 12. Referencia a evidencias

- Índice completo por caso, con rutas verificadas: [`03_Indice_Evidencias.md`](03_Indice_Evidencias.md)
- Consolidado de rendimiento: [`02_Resumen_Rendimiento.md`](02_Resumen_Rendimiento.md)
- Informes individuales: `../01_Funcionales/TC-FUN-00x/`, `../04_Contrato_Consistencia/TC-CON-00x/` y `../05_Rendimiento/TC-REN-00x/` (archivo `TC-XXX-00x_Informe.md` en cada carpeta)
- Evidencia de TC-VAL y TC-ERR: `../02_Validacion_Entradas/` y `../03_Manejo_Errores/` (colección y reporte HTML)
- Versiones anteriores en git: commit `0b9d9b2` (TC-REN-003 y TC-REN-005 con los criterios del plan v1.0)
