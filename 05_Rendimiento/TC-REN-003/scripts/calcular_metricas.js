// TC-REN-003 - Cálculo de métricas a partir del reporte oficial de Newman.
//
// No realiza peticiones HTTP: solo lee evidencia ya generada por Newman.
//
// Uso (desde TC-REN-003/):
//   node scripts/calcular_metricas.js [reporte.json] [salida-tiempos.json] [salida-metricas.json] [salida-muestra.json]
// Valores por defecto: el run oficial y los archivos de evidencias definidos por el caso.

const fs = require("fs");
const path = require("path");

const EXPECTED_ITERATIONS = 50;
const REQUEST_NAME = "TC-REN-003 - Estabilidad bajo repetición";
const ENDPOINT_PATH = "breweries/random";

const root = path.join(__dirname, "..");
const args = process.argv.slice(2);
const reportPath = path.resolve(root, args[0] || "evidencias/TC-REN-003-newman.json");
const timesPath = path.resolve(root, args[1] || "evidencias/tiempos-response.json");
const metricsPath = path.resolve(root, args[2] || "evidencias/metricas.json");
const samplePath = args[3] === "-" ? null : path.resolve(root, args[3] || "evidencias/muestra-response.json");

const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
const run = report.run;

// Solo las ejecuciones de la request oficial de TC-REN-003
const executions = run.executions.filter(function (execution) {
    const urlPath = (execution.request && execution.request.url && execution.request.url.path || []).join("/");
    return execution.item && execution.item.name === REQUEST_NAME && urlPath.endsWith(ENDPOINT_PATH);
});

const series = executions.map(function (execution) {
    const response = execution.response;
    const iteration = execution.cursor.iteration + 1;

    if (!response) {
        return {
            iteration: iteration,
            http: null,
            response_time_ms: null,
            error: execution.requestError ? String(execution.requestError.message || execution.requestError) : "sin respuesta"
        };
    }

    return {
        iteration: iteration,
        http: response.code,
        response_time_ms: response.responseTime,
        response_size_bytes: response.responseSize
    };
});

// Tiempos válidos: solo respuestas recibidas (no se inventan tiempos para fallos)
const times = series
    .filter(function (entry) { return typeof entry.response_time_ms === "number"; })
    .map(function (entry) { return entry.response_time_ms; });

const n = times.length;
const sorted = times.slice().sort(function (a, b) { return a - b; });

const sum = times.reduce(function (acc, t) { return acc + t; }, 0);
const mean = n > 0 ? sum / n : null;

// Mediana: promedio de las dos posiciones centrales si N es par
let median = null;
if (n > 0) {
    median = n % 2 === 0
        ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2
        : sorted[(n - 1) / 2];
}

// Desviación estándar poblacional: sqrt( Σ(ti - μ)² / N )
const populationStdDev = n > 0
    ? Math.sqrt(times.reduce(function (acc, t) { return acc + Math.pow(t - mean, 2); }, 0) / n)
    : null;

// P95 nearest-rank: posición = ceil(0.95 × N), base 1
const p95Rank = n > 0 ? Math.ceil(0.95 * n) : null;
const p95 = n > 0 ? sorted[p95Rank - 1] : null;

const cv = mean > 0 ? (populationStdDev / mean) * 100 : null;

const http200Count = series.filter(function (entry) { return entry.http === 200; }).length;
const failures = series.filter(function (entry) { return entry.http !== 200; });

const metrics = {
    case_id: "TC-REN-003",
    source_report: path.relative(root, reportPath).split(path.sep).join("/"),
    run_started_utc: new Date(run.timings.started).toISOString(),
    run_completed_utc: new Date(run.timings.completed).toISOString(),
    total_iterations_expected: EXPECTED_ITERATIONS,
    iterations_reported_by_newman: run.stats.iterations.total,
    total_executions_observed: series.length,
    responses_received: n,
    http_200_count: http200Count,
    failure_count: failures.length,
    failures: failures,
    success_rate_percent: (http200Count / EXPECTED_ITERATIONS) * 100,
    assertions: {
        total: run.stats.assertions.total,
        failed: run.stats.assertions.failed
    },
    response_time_ms: {
        n: n,
        min: n > 0 ? sorted[0] : null,
        max: n > 0 ? sorted[n - 1] : null,
        sum: sum,
        mean: mean,
        median: median,
        population_standard_deviation: populationStdDev,
        p95: p95,
        p95_method: "nearest-rank",
        p95_rank: p95Rank,
        coefficient_of_variation_percent: cv
    },
    standard_deviation_threshold_defined_in_plan: false
};

fs.writeFileSync(timesPath, JSON.stringify(series, null, 2) + "\n");
fs.writeFileSync(metricsPath, JSON.stringify(metrics, null, 2) + "\n");

// Muestra real de una ejecución oficial (la primera con respuesta)
if (samplePath) {
    const firstWithResponse = executions.find(function (execution) { return execution.response; });
    if (firstWithResponse) {
        const body = JSON.parse(Buffer.from(firstWithResponse.response.stream.data).toString("utf8"));
        const sample = {
            iteration: firstWithResponse.cursor.iteration + 1,
            http: firstWithResponse.response.code,
            response_time_ms: firstWithResponse.response.responseTime,
            body: body
        };
        fs.writeFileSync(samplePath, JSON.stringify(sample, null, 2) + "\n");
    }
}

console.log(JSON.stringify(metrics, null, 2));
