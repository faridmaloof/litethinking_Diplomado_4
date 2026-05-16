$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$addonPath = Join-Path $scriptDir "mitm_addon_response_override.py"

if (!(Test-Path $addonPath)) {
		Write-Error "No se encontró el addon: $addonPath"
		exit 1
}

Write-Host "Iniciando mitmweb con addon de alteración de respuestas..."
Write-Host "Proxy: 127.0.0.1:8080"
Write-Host "Web UI: http://127.0.0.1:8081"

$commonArgs = @(
	"--listen-host", "127.0.0.1",
	"--listen-port", "8080",
	"--web-host", "127.0.0.1",
	"--web-port", "8081",
	"-s", $addonPath
)

# Opción 1: usar ejecutable mitmweb si está en PATH
$mitmweb = Get-Command mitmweb -ErrorAction SilentlyContinue
if ($mitmweb) {
	& $mitmweb.Source @commonArgs
	exit $LASTEXITCODE
}

# Opción 2: fallback por Python (sin depender de PATH de mitmweb)
$pythonCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
	$pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
	$pythonCmd = "python"
}

if (-not $pythonCmd) {
	Write-Error "No se encontró 'mitmweb' ni un intérprete Python (py/python). Instala Python 3 y mitmproxy."
	exit 1
}

# Verifica que mitmproxy esté instalado en Python
& $pythonCmd -c "import mitmproxy" 2>$null
if ($LASTEXITCODE -ne 0) {
	Write-Error "mitmproxy no está instalado en Python. Ejecuta: python -m pip install mitmproxy"
	exit 1
}

# Ejecuta mitmweb vía módulo de Python
& $pythonCmd -m mitmproxy.tools.main mitmweb @commonArgs
exit $LASTEXITCODE
