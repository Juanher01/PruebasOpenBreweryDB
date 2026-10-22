# Informe Consolidado de Pruebas de Calidad — API Open BreweryDB

---

## 1. Información general

| Campo | Valor |
|---|---|
| Proyecto | Pruebas de calidad de la API pública Open BreweryDB |
| Sistema bajo prueba | `https://api.openbrewerydb.org/v1` |
| Repositorio | `https://github.com/Juanher01/PruebasOpenBreweryDB` (rama `main`) |
| Equipo de pruebas | Juan Esteban Hernández Lozano · Samuel Alexander Perdomo Fajardo |
| Periodo de ejecución | 01/10/2026 |
| Fecha de emisión del informe | 22/10/2026 |
| Versión del informe | 2.0 |

---

## 2. Objetivo

El presente informe consolida los resultados de la campaña de pruebas ejecutada sobre la API pública Open BreweryDB. Su propósito es presentar de forma detallada el resultado obtenido en cada caso de prueba, los defectos identificados, el grado de cumplimiento de los criterios de aceptación definidos y una recomendación final sobre el estado de calidad del servicio evaluado.

---

## 3. Alcance

La campaña comprendió **28 casos de prueba** distribuidos en cinco tipos de prueba:

| Tipo de prueba | Identificadores | Cantidad | Responsable |
|---|---|---:|---|
| Funcionales | TC-FUN-001 a TC-FUN-009 | 9 | Juan Esteban Hernández Lozano |
| Validación de entradas | TC-VAL-001 a TC-VAL-005 | 5 | Samuel Alexander Perdomo Fajardo |
| Manejo de errores | TC-ERR-001 a TC-ERR-005 | 5 | Samuel Alexander Perdomo Fajardo |
| Contrato y consistencia | TC-CON-001 a TC-CON-004 | 4 | Juan Esteban Hernández Lozano (001–003) · Samuel Alexander Perdomo Fajardo (004) |
| Rendimiento | TC-REN-001 a TC-REN-005 | 5 | Juan Esteban Hernández Lozano |
| **Total** | | **28** | |

Quedan fuera del alcance las pruebas de seguridad, las pruebas de interfaz de usuario y cualquier operación de escritura sobre la API, dado que el servicio es de solo lectura.

---

## 4. Metodología, herramientas y entorno

### 4.1 Herramientas

| Herramienta | Uso |
|---|---|
| Postman (colecciones v2.1) | Definición de solicitudes, variables de entorno y aserciones automatizadas (`pm.expect`) |
| Newman 6.2.2 (Node.js v22.15.1) | Ejecución automatizada de las colecciones y generación de reportes (`cli`, `json`, `htmlextra`) |
| AJV / JSON Schema draft-07 | Validación del contrato de respuesta en las pruebas TC-CON-001, TC-CON-002 y TC-CON-004 |
| Apache JMeter 5.6.3 (Java 22), modo no-GUI | Pruebas de carga concurrente y de throughput (TC-REN-004 y TC-REN-005) |
| Scripts auxiliares (Node.js / Python) | Cálculo de métricas estadísticas sobre los resultados obtenidos |

### 4.2 Prácticas aplicadas

- Ejecución de una verificación previa (*preflight*) separada de la ejecución oficial; los resultados del *preflight* no forman parte de la muestra evaluada.
- Determinación del estado de cada caso a partir de una única ejecución oficial.
- Repetición de confirmación en los casos con resultado fallido, para verificar la reproducibilidad del defecto.
- Obtención dinámica de identificadores durante la ejecución, sin uso de valores fijos.

### 4.3 Entorno de ejecución

- Sistema operativo: Windows 11 (build 10.0.26200).
- Las mediciones de tiempo son de extremo a extremo desde el equipo de ejecución e incluyen la latencia de red, la resolución DNS y la negociación TLS.

---

## 5. Resumen general de resultados

| Indicador | Valor |
|---|---:|
| Casos planificados | 28 |
| Casos ejecutados | 28 (100 %) |
| Casos aprobados | **23 (82,1 %)** |
| Casos rechazados | **5 (17,9 %)** |
| Casos bloqueados | 0 |

### 5.1 Resultados por tipo de prueba

| Tipo de prueba | Ejecutados | Aprobados | Rechazados | % de aprobación |
|---|---:|---:|---:|---:|
| Funcionales | 9 | 7 | 2 | 77,8 % |
| Validación de entradas | 5 | 2 | 3 | 40,0 % |
| Manejo de errores | 5 | 5 | 0 | 100,0 % |
| Contrato y consistencia | 4 | 4 | 0 | 100,0 % |
| Rendimiento | 5 | 5 | 0 | 100,0 % |
| **Total** | **28** | **23** | **5** | **82,1 %** |

### 5.2 Casos rechazados

| ID | Tipo | Escenario | Motivo del rechazo |
|---|---|---|---|
| TC-FUN-003 | Funcional | Búsqueda por nombre (`query=san`) | 46 de 50 resultados no contienen el término buscado en el nombre |
| TC-FUN-004 | Funcional | Cervecería aleatoria | La respuesta es un arreglo de un elemento en lugar de un objeto JSON único |
| TC-VAL-002 | Validación de entradas | Tipo de cervecería inexistente | La API no valida el valor de `by_type` y devuelve el mensaje de bienvenida |
| TC-VAL-003 | Validación de entradas | Búsqueda sin término | La API devuelve el mensaje de bienvenida en lugar de un arreglo o un mensaje de parámetro requerido |
| TC-VAL-005 | Validación de entradas | Caracteres especiales en búsqueda | La API devuelve el mensaje de bienvenida en lugar de un arreglo |

---

## 6. Resultados detallados por tipo de prueba

### 6.1 Pruebas funcionales — 7 aprobadas, 2 rechazadas

| ID | Escenario | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| TC-FUN-001 | Listado general de cervecerías | HTTP 200; arreglo JSON no vacío de objetos de cervecerías | HTTP 200; arreglo de 50 objetos con paginación por defecto; 6/6 aserciones; 323 ms | APROBADO |
| TC-FUN-002 | Consulta por ID dinámico | HTTP 200; objeto único cuyo `id` coincide con el solicitado e incluye `id`, `name` y `brewery_type` | ID `ae7b3174-8be8-4d53-a3a5-9b8240970eea` obtenido del listado; detalle con el mismo ID y los campos requeridos; 14/14 aserciones; 90 ms | APROBADO |
| TC-FUN-003 | Búsqueda por nombre | HTTP 200; arreglo no vacío cuyos nombres contienen "san" | HTTP 200; 50 resultados, de los cuales solo 4 contienen "san" en el nombre; 7/8 aserciones; 712 ms; defecto reproducido en 3 de 3 ejecuciones | **RECHAZADO** |
| TC-FUN-004 | Cervecería aleatoria | HTTP 200; objeto JSON único (no arreglo) con `id`, `name` y `brewery_type` | HTTP 200; la raíz es un arreglo con 1 elemento; los campos no están en la raíz; 3/8 aserciones; 448 ms; defecto reproducido en 3 de 3 ejecuciones | **RECHAZADO** |
| TC-FUN-005 | Consulta de metadatos | HTTP 200; objeto con `total`, `page` y `per_page` | HTTP 200; `total`=11848, `page`=1, `per_page`=50; 8/8 aserciones; 327 ms | APROBADO |
| TC-FUN-006 | Filtrado por estado (`by_state=california`) | Todos los registros con `state`="California" | 50/50 registros conformes; 8/8 aserciones; 314 ms | APROBADO |
| TC-FUN-007 | Filtrado por tipo (`by_type=micro`) | Todos los registros con `brewery_type`="micro" | 50/50 registros conformes; 8/8 aserciones; 355 ms | APROBADO |
| TC-FUN-008 | Paginación (`page=2&per_page=5`) | Máximo 5 registros; IDs distintos a los de la página 1 | Página 1: 5 registros (320 ms); página 2: 5 registros (84 ms); ningún ID en común; 14/14 aserciones | APROBADO |
| TC-FUN-009 | Flujo de consulta encadenado | El detalle del ID seleccionado es idéntico al elemento del listado | ID `ef970757-fe42-416f-931d-722451f1f59c`; 16/16 campos iguales y 0 diferencias; 12/12 aserciones | APROBADO |

**Análisis.** Las operaciones de listado, consulta por identificador, metadatos, filtrado, paginación y flujo encadenado se comportan conforme a lo especificado. Los dos rechazos corresponden a defectos reproducibles del servicio:

- **TC-FUN-003:** los 46 registros no conformes tienen una ciudad que comienza por "San", lo que indica que el endpoint `/search` busca el término en campos distintos del nombre (por ejemplo, la ciudad). El comportamiento no se ajusta al resultado esperado de una búsqueda por nombre.
- **TC-FUN-004:** el endpoint `/random` devuelve la cervecería envuelta en un arreglo, lo que obliga al consumidor a acceder al primer elemento en lugar de recibir directamente el objeto.

### 6.2 Pruebas de validación de entradas — 2 aprobadas, 3 rechazadas

| ID | Escenario | Solicitud | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|---|
| TC-VAL-001 | Parámetro válido | `GET /v1/breweries?by_state=texas` | HTTP 200; arreglo de cervecerías de Texas | HTTP 200; arreglo con todos los registros con `state`="Texas"; 3/3 aserciones | APROBADO |
| TC-VAL-002 | Tipo de cervecería inexistente | `GET /v1/breweries?by_type=xyz` | HTTP 200 con arreglo vacío o HTTP 400 con error de validación | HTTP 200; objeto JSON con el mensaje de bienvenida de la API (`message`, `documentation_url`, `mcp_url`); sin arreglo vacío ni error de validación | **RECHAZADO** |
| TC-VAL-003 | Búsqueda sin término | `GET /v1/breweries/search?query=` | HTTP 200 con arreglo vacío o HTTP 400 con mensaje de parámetro requerido | HTTP 200; objeto JSON con el mensaje de bienvenida; 1/2 aserciones (falló "expected { …(3) } to be an array") | **RECHAZADO** |
| TC-VAL-004 | Ciudad no registrada | `GET /v1/breweries?by_city=atlantida` | HTTP 200; arreglo vacío `[]` | HTTP 200; arreglo vacío; 2/2 aserciones | APROBADO |
| TC-VAL-005 | Caracteres especiales en búsqueda | `GET /v1/breweries/search?query=%20%25%26` | HTTP 200; arreglo vacío o manejo controlado sin error 500 | HTTP 200 sin error 500, pero con el objeto de bienvenida en lugar de un arreglo; 2/3 aserciones (falló "Validación de estructura segura") | **RECHAZADO** |

**Análisis.** La API procesa correctamente los parámetros válidos y los valores inexistentes de filtros de texto libre (TC-VAL-001 y TC-VAL-004). Sin embargo, ante entradas inválidas, vacías o con caracteres especiales no aplica una validación explícita: en lugar de devolver un arreglo vacío o un error controlado (HTTP 400), responde HTTP 200 con el mensaje de bienvenida de la API. Esto produce un cambio en la estructura de la respuesta (objeto en lugar de arreglo) que puede provocar errores en los consumidores. Como aspecto positivo, ninguna de las entradas provocó un error interno del servidor (HTTP 500).

### 6.3 Pruebas de manejo de errores — 5 aprobadas, 0 rechazadas

| ID | Escenario | Solicitud | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|---|
| TC-ERR-001 | ID con formato válido pero inexistente | `GET /v1/breweries/00000000-0000-0000-0000-000000000000` | HTTP 404 con mensaje de error o cuerpo vacío | HTTP 404; página HTML "Not Found" (`text/html`) que indica que el recurso no existe | APROBADO |
| TC-ERR-002 | Formato de ID inválido | `GET /v1/breweries/12345` | HTTP 400 o 404 | HTTP 404; página HTML "Not Found" | APROBADO |
| TC-ERR-003 | Endpoint inexistente | `GET /v1/beers` | HTTP 404 | HTTP 404; página HTML "Not Found"; 2/2 aserciones | APROBADO |
| TC-ERR-004 | Método HTTP no permitido | `POST /v1/breweries` | HTTP 405 o 404 | HTTP 405 "Method Not Allowed"; página HTML de error | APROBADO |
| TC-ERR-005 | Versión de API incorrecta | `GET /v2/breweries` | HTTP 404 | HTTP 404; página HTML "Not Found"; 2/2 aserciones | APROBADO |

**Análisis.** La API responde en todos los casos con el código de estado HTTP adecuado para cada situación de error (404 para recursos y rutas inexistentes y 405 para métodos no permitidos), por lo que los cinco casos se consideran aprobados. Se registran las siguientes observaciones:

- Las respuestas de error se entregan como páginas HTML y no como objetos JSON. Este formato no es el habitual en una API REST y obliga a los consumidores a tratar el error únicamente por el código de estado.
- En TC-ERR-001 y TC-ERR-002 fallaron aserciones secundarias que esperaban un cuerpo vacío o JSON. El estado se determinó por el código HTTP y por el contenido "Not Found", que cumplen el resultado esperado.
- En TC-ERR-004 el script de pruebas presentó un error de sintaxis (`SyntaxError: Unexpected end of input`), por lo que el código 405 se verificó en la respuesta registrada y no mediante aserción automatizada. Se recomienda corregir el script para futuras ejecuciones.

### 6.4 Pruebas de contrato y consistencia — 4 aprobadas, 0 rechazadas

| ID | Escenario | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| TC-CON-001 | Presencia de campos obligatorios | Objeto JSON con `id`, `name`, `brewery_type`, `city`, `state` y `country` | 6/6 campos presentes; validación AJV sin errores; 16/16 aserciones; 85 ms | APROBADO |
| TC-CON-002 | Tipos de datos | `id` y `name` de tipo String; `latitude` y `longitude` de tipo Number o Null | `id`/`name` string; `latitude`=50.241246 y `longitude`=11.327765 (number); AJV sin errores; 14/14 aserciones; 86 ms | APROBADO |
| TC-CON-003 | Consistencia entre listado y detalle | Igualdad profunda entre el objeto del listado y el del detalle | 16 propiedades comparadas; mismo conjunto de claves; 0 diferencias de valor, tipo o nulabilidad; 14/14 aserciones | APROBADO |
| TC-CON-004 | Estructura de metadatos | `total`, `page` y `per_page` como enteros; se admiten propiedades adicionales | `total`=11848, `page`=1, `per_page`=50 (enteros); propiedades adicionales `by_state`, `by_country` y `by_type`; AJV sin errores; 11/11 aserciones; 311 ms | APROBADO |

**Análisis.** La estructura y los tipos de datos de las respuestas cumplen el contrato definido, y la información de un mismo recurso es consistente entre los endpoints de listado y de detalle.

### 6.5 Pruebas de rendimiento — 5 aprobadas, 0 rechazadas

| ID | Escenario | Criterio de aceptación | Resultado obtenido | Margen | Estado |
|---|---|---|---|---|---|
| TC-REN-001 | Latencia de listado simple | Tiempo de respuesta < 2000 ms | 316 ms; HTTP 200; 20 731 bytes | 1684 ms | APROBADO |
| TC-REN-002 | Latencia de búsqueda | Tiempo de respuesta < 1500 ms | 331 ms; HTTP 200; 21 738 bytes | 1169 ms | APROBADO |
| TC-REN-003 | Estabilidad bajo repetición | 50 solicitudes secuenciales; 100 % HTTP 200; P95 < 2000 ms | 50/50 HTTP 200; P95 = 259 ms (mín. 220, máx. 521, media 239,08, mediana 230,50, desv. est. 41,82 ms; CV 17,49 %) | 1741 ms | APROBADO |
| TC-REN-004 | Carga moderada | 10 hilos concurrentes; ≥ 95 % < 3000 ms; 0 % de errores | 10/10 HTTP 200; 100 % < 3000 ms; 0 % de errores; P95 = 624 ms (mín. 613, máx. 624, media 618,7 ms) | 2376 ms | APROBADO |
| TC-REN-005 | Throughput | 10 hilos durante 60 s; ≥ 99,18 req/s; 100 % HTTP 200; 0 % HTTP 429 | 6200 solicitudes; 103,31 req/s; 6200/6200 HTTP 200; 0 HTTP 429; 0 errores de red; latencia media 96,58 ms y P95 104 ms | +4,13 req/s | APROBADO |

**Análisis.** La API cumple todos los criterios de rendimiento con márgenes amplios. Los tiempos de respuesta individuales se sitúan entre un 78 % y un 84 % por debajo de los umbrales; el comportamiento bajo repetición es estable (coeficiente de variación del 17,49 %) y, bajo carga concurrente sostenida, la API mantuvo un throughput de 103,31 req/s, con una degradación del 6,25 % respecto de la línea base de 110,198 req/s, sin errores ni limitación de tasa (HTTP 429). El detalle de las métricas se encuentra en [`02_Resumen_Rendimiento.md`](02_Resumen_Rendimiento.md).

---

## 7. Defectos identificados

| ID defecto | Caso | Descripción | Severidad sugerida | Reproducibilidad |
|---|---|---|---|---|
| DEF-01 | TC-FUN-003 | El endpoint `/v1/breweries/search?query=san` devuelve registros cuyo nombre no contiene el término buscado (46 de 50), aparentemente porque la búsqueda incluye otros campos, como la ciudad | Media | 3/3 |
| DEF-02 | TC-FUN-004 | El endpoint `/v1/breweries/random` devuelve un arreglo de un elemento en lugar de un objeto JSON único | Baja | 3/3 |
| DEF-03 | TC-VAL-002 | Un valor inexistente en `by_type` no se valida: la API responde HTTP 200 con el mensaje de bienvenida en lugar de un arreglo vacío o un HTTP 400 | Media | — |
| DEF-04 | TC-VAL-003 | Una búsqueda con término vacío responde HTTP 200 con el mensaje de bienvenida en lugar de un arreglo vacío o un mensaje de parámetro requerido | Media | — |
| DEF-05 | TC-VAL-005 | Una búsqueda con caracteres especiales responde HTTP 200 con el mensaje de bienvenida en lugar de un arreglo | Media | — |

### 7.1 Observaciones adicionales

- **Formato de las respuestas de error:** los errores 404 y 405 se devuelven como páginas HTML en lugar de cuerpos JSON (TC-ERR-001 a TC-ERR-005).
- **Calidad de datos:** el registro `ae7b3174-8be8-4d53-a3a5-9b8240970eea` tiene como nombre el valor `'s`, y la página 2 de TC-FUN-008 incluye dos registros "10 Barrel Brewing Co" en Bend con identificadores distintos. Estas situaciones no afectan al resultado de los casos, pero se reportan para su revisión.
- **Script de pruebas:** la colección de TC-ERR-004 contiene un error de sintaxis que impide ejecutar sus aserciones automatizadas.

---

## 8. Cumplimiento de los criterios de finalización

| Criterio | Resultado | Estado |
|---|---|---|
| 100 % de los casos críticos (TC-FUN y TC-ERR) ejecutados al menos una vez | 14/14 casos ejecutados | Cumple |
| ≥ 95 % del total de casos ejecutados | 28/28 casos ejecutados (100 %) | Cumple |
| Latencia individual: TC-REN-001 < 2000 ms y TC-REN-002 < 1500 ms | 316 ms y 331 ms | Cumple |
| P95 en ejecución múltiple (TC-REN-003 y TC-REN-004) | 259 ms (< 2000 ms) y 624 ms (100 % < 3000 ms) | Cumple |
| Carga moderada: ≥ 95 % < 3000 ms y 0 % de errores (TC-REN-004) | 100 % < 3000 ms; 0 % de errores | Cumple |
| Ausencia de limitación de tasa sostenida (TC-REN-005) | 0 respuestas HTTP 429 en 6200 solicitudes | Cumple |
| Contrato de respuesta validado (TC-CON) | 4/4 casos aprobados | Cumple |
| Defectos identificados documentados | 5 defectos registrados en la sección 7 | Cumple |

---

## 9. Riesgos y limitaciones

1. **Mediciones de extremo a extremo:** los tiempos se registraron desde un único equipo con Windows e incluyen la latencia de red, por lo que pueden variar según la ubicación y la conexión utilizada.
2. **Datos dinámicos:** Open BreweryDB es un servicio público con datos que cambian con el tiempo; los identificadores, totales y conteos reportados corresponden al momento de la ejecución.
3. **Carga limitada:** las pruebas de rendimiento se realizaron con un máximo de 10 hilos concurrentes. No se evaluó el comportamiento con volúmenes de carga superiores.
4. **Servicio de terceros:** la API no está bajo control del equipo de pruebas, por lo que los defectos identificados solo pueden reportarse al proveedor.

---

## 10. Conclusiones

1. **Cobertura:** se ejecutaron los 28 casos planificados (100 %), con 23 aprobados (82,1 %), 5 rechazados (17,9 %) y ningún caso bloqueado.
2. **Funcionalidad:** las capacidades principales de la API (listado, consulta por identificador, metadatos, filtros por estado y tipo, paginación y flujo encadenado) funcionan correctamente. Se identificaron dos defectos reproducibles: la búsqueda por nombre devuelve resultados que no contienen el término buscado y el endpoint de cervecería aleatoria devuelve un arreglo en lugar de un objeto.
3. **Validación de entradas:** es el área más débil de la campaña (40 % de aprobación). La API no valida los parámetros inválidos, vacíos o con caracteres especiales y responde con el mensaje de bienvenida en lugar de una respuesta estructurada coherente o un error controlado.
4. **Manejo de errores:** la API devuelve los códigos de estado HTTP adecuados en todos los escenarios evaluados, aunque el cuerpo de las respuestas de error está en formato HTML en lugar de JSON.
5. **Contrato y consistencia:** las respuestas cumplen el contrato definido en cuanto a campos obligatorios, tipos de datos y estructura de metadatos, y son consistentes entre los endpoints de listado y de detalle.
6. **Rendimiento:** la API cumple todos los criterios con márgenes amplios, mantiene un comportamiento estable bajo repetición y bajo carga concurrente moderada, y no presenta limitación de tasa con aproximadamente 103 solicitudes por segundo.

---

## 11. Recomendación

Con base en la evidencia recopilada, se emite un dictamen **GO CONDICIONADO** para el uso de la API Open BreweryDB como fuente de consulta de datos:

- La API es **apta** para consumos de listado, consulta por identificador, filtrado, paginación y metadatos, con un rendimiento y una consistencia de datos satisfactorios.
- Los consumidores deben **implementar medidas de mitigación** frente a los defectos identificados:
  - validar en el cliente los parámetros antes de enviarlos y verificar que la respuesta sea un arreglo antes de procesarla (DEF-03, DEF-04 y DEF-05);
  - filtrar en el cliente los resultados de la búsqueda cuando se requiera una coincidencia estricta por nombre (DEF-01);
  - tratar la respuesta de `/random` como un arreglo y tomar su primer elemento (DEF-02);
  - gestionar los errores a partir del código de estado HTTP y no del cuerpo de la respuesta.
- Se recomienda **reportar los defectos DEF-01 a DEF-05 al proveedor** del servicio y **corregir el script de TC-ERR-004** antes de una nueva ronda de regresión.

---

## 12. Referencias

- Índice de evidencias por caso: [`03_Indice_Evidencias.md`](03_Indice_Evidencias.md)
- Resumen de rendimiento: [`02_Resumen_Rendimiento.md`](02_Resumen_Rendimiento.md)
- Evidencias de pruebas funcionales: `../01_Funcionales/`
- Evidencias de validación de entradas: `../02_Validacion_Entradas/`
- Evidencias de manejo de errores: `../03_Manejo_Errores/`
- Evidencias de contrato y consistencia: `../04_Contrato_Consistencia/`
- Evidencias de rendimiento: `../05_Rendimiento/`
