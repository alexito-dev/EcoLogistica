# Análisis reproducible de SonarQube para EcoLogística (Windows PowerShell).
# Requiere servidor SonarQube accesible, SONAR_TOKEN local, SonarScanner, Node y backend/.venv.
[CmdletBinding()]
param([string]$SonarUrl = "http://localhost:9000")

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$raiz = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $raiz "backend/.venv/Scripts/python.exe"

if ([string]::IsNullOrWhiteSpace($env:SONAR_TOKEN)) {
    throw "Configure SONAR_TOKEN en el entorno local. No publique ni comparta el token."
}
if (-not (Test-Path $python)) {
    throw "Falta backend/.venv/Scripts/python.exe. Cree el entorno virtual e instale requirements.txt."
}
$scanner = Get-Command "sonar-scanner" -ErrorAction SilentlyContinue
if (-not $scanner) { throw "Instale SonarScanner CLI y agregue su carpeta bin a PATH." }
if (-not (Get-Command "npm.cmd" -ErrorAction SilentlyContinue)) {
    throw "Instale Node.js y npm."
}

$revision = (& git -C $raiz rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "No se pudo identificar el commit Git." }
$modificaciones = & git -C $raiz status --porcelain
if ($LASTEXITCODE -ne 0) { throw "No se pudo verificar el estado de Git." }
if ($modificaciones) { throw "Confirme o descarte los cambios locales antes de analizar." }
Write-Host "Analizando commit $revision"

Push-Location (Join-Path $raiz "backend")
try {
    & $python -m pytest --cov=app --cov-report=xml:coverage.xml
    if ($LASTEXITCODE -ne 0) { throw "Fallaron las pruebas/cobertura de Python." }
} finally { Pop-Location }

Push-Location (Join-Path $raiz "frontend")
try {
    & npm.cmd ci
    if ($LASTEXITCODE -ne 0) { throw "Fallo npm ci." }
    & npx.cmd --no-install vitest run --coverage
    if ($LASTEXITCODE -ne 0) { throw "Fallaron las pruebas/cobertura de frontend." }
} finally { Pop-Location }

if (-not (Test-Path (Join-Path $raiz "backend/coverage.xml"))) {
    throw "No se genero backend/coverage.xml."
}
if (-not (Test-Path (Join-Path $raiz "frontend/coverage/lcov.info"))) {
    throw "No se genero frontend/coverage/lcov.info."
}

# SonarScanner lee SONAR_TOKEN del entorno: no lo ponemos en los argumentos o en archivos.
$env:SONAR_HOST_URL = $SonarUrl.TrimEnd("/")
Push-Location $raiz
try {
    & $scanner.Source "-Dsonar.qualitygate.wait=true" "-Dsonar.qualitygate.timeout=300"
    $codigoScanner = $LASTEXITCODE
} finally { Pop-Location }
if ($codigoScanner -ne 0) {
    throw "SonarScanner no finalizo correctamente (codigo $codigoScanner). Revise el Quality Gate y el log."
}

# La API consulta SOLO resultados calculados por SonarQube tras el escaneo exitoso.
$credencial = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($env:SONAR_TOKEN):"))
$cabeceras = @{ Authorization = "Basic $credencial" }
$claves = "coverage,line_coverage,branch_coverage,bugs,vulnerabilities,security_hotspots,code_smells,duplicated_lines_density,sqale_index,ncloc,reliability_rating,security_rating,sqale_rating"
$base = $env:SONAR_HOST_URL
$medidas = Invoke-RestMethod -Uri "$base/api/measures/component?component=ecologistica&metricKeys=$claves" -Headers $cabeceras -TimeoutSec 30
$calidad = Invoke-RestMethod -Uri "$base/api/qualitygates/project_status?projectKey=ecologistica" -Headers $cabeceras -TimeoutSec 30
$valores = @{}
foreach ($medida in $medidas.component.measures) {
    $valores[[string]$medida.metric] = [string]$medida.value
}
function Medida([string]$clave) {
    if ($valores.ContainsKey($clave)) { return $valores[$clave] }
    return "No disponible"
}
function Nota([string]$clave) {
    $valor = Medida $clave
    switch ($valor) {
        "1.0" { return "A" }
        "2.0" { return "B" }
        "3.0" { return "C" }
        "4.0" { return "D" }
        "5.0" { return "E" }
        default { return $valor }
    }
}

$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$lineas = @(
    "# Resultado SonarQube del commit analizado",
    "",
    "**Proyecto:** EcoLogistica Huancayo",
    "",
    "**Fecha de ejecucion:** $fecha",
    "",
    "**Commit:** $revision",
    "",
    "**Origen:** API de SonarQube ($base), tras SonarScanner con Quality Gate verificado",
    "",
    "| Indicador | Resultado |",
    "|---|---:|",
    "| Quality Gate | $($calidad.projectStatus.status) |",
    "| Cobertura combinada | $(Medida 'coverage') % |",
    "| Cobertura de lineas | $(Medida 'line_coverage') % |",
    "| Cobertura de ramas | $(Medida 'branch_coverage') % |",
    "| Bugs | $(Medida 'bugs') |",
    "| Vulnerabilidades detectadas | $(Medida 'vulnerabilities') |",
    "| Security Hotspots | $(Medida 'security_hotspots') |",
    "| Code smells | $(Medida 'code_smells') |",
    "| Duplicacion | $(Medida 'duplicated_lines_density') % |",
    "| Deuda tecnica | $(Medida 'sqale_index') minutos |",
    "| Lineas de codigo | $(Medida 'ncloc') |",
    "| Fiabilidad | $(Nota 'reliability_rating') |",
    "| Seguridad | $(Nota 'security_rating') |",
    "| Mantenibilidad | $(Nota 'sqale_rating') |",
    "",
    "## Interpretacion y limites",
    "",
    "- El Quality Gate solo evalua las condiciones configuradas; un OK no certifica seguridad total.",
    "- Importamos cobertura desde pytest (Cobertura XML) y Vitest (LCOV) antes del escaneo.",
    "- Las metricas del codigo nuevo y del codigo total pueden diferir; revisar ambas en el panel.",
    "- Un valor 'No disponible' significa que la API no lo publico; no equivale a cero.",
    "- Este resultado no sustituye pentesting, pruebas E2E, auditoria WCAG ni verificacion de produccion.",
    "- Registrar incidencias en el panel: regla, severidad, archivo, causa, responsable y remedio.",
    "",
    "**Referencia historica:** [Reporte del Sprint 3](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md).",
    ""
)
$salida = Join-Path $raiz "docs/03 Implementación/Sprint 03/SONARQUBE-ULTIMO-ANALISIS.md"
$lineas -join [Environment]::NewLine | Set-Content -Path $salida -Encoding UTF8
Write-Host "Reporte generado localmente: $salida"
Write-Host "Revise sus resultados y publíquelo mediante un PR. No se publica automaticamente."
