# Levanta EcoLogística para una demostración: API (puerto 8001) y pantalla (puerto 3000), sin Docker ni base de datos.
# Usa datos sintéticos de Huancayo y archivos temporales; no toca ninguna base real. Uso:
#   powershell -ExecutionPolicy Bypass -File scripts\iniciar-demo.ps1
$raiz = Split-Path -Parent $PSScriptRoot
$clave = 'Demo-Prueba-2026!'

$api = @"
`$host.UI.RawUI.WindowTitle = 'EcoLogistica API (8001)'
Set-Location '$raiz\backend'
`$env:DATABASE_URL = ''
`$env:DEMO_PEDIDOS = 'true'
`$env:DEMO_CLAVE = '$clave'
`$env:JWT_SECRET = 'demo-firma-suficientemente-larga-0123456789'
`$env:USUARIOS_ARCHIVO = "`$env:TEMP\eco-demo-usuarios.json"
`$env:RUTAS_ARCHIVO = "`$env:TEMP\eco-demo-rutas.json"
python -m uvicorn app.main:app --app-dir src --port 8001
"@

$web = @"
`$host.UI.RawUI.WindowTitle = 'EcoLogistica Pantalla (3000)'
Set-Location '$raiz\frontend'
`$env:VITE_API_URL = 'http://localhost:8001/api/v1'
npm run dev
"@

# -EncodedCommand evita problemas de comillas al pasar el script a cada ventana nueva.
function Codificar($texto) { [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($texto)) }
Start-Process powershell -ArgumentList '-NoExit', '-EncodedCommand', (Codificar $api)
Start-Process powershell -ArgumentList '-NoExit', '-EncodedCommand', (Codificar $web)
Start-Sleep -Seconds 8
Start-Process 'http://localhost:3000'

Write-Host ''
Write-Host 'EcoLogística está arrancando. Abra http://localhost:3000' -ForegroundColor Green
Write-Host "Cuentas: planificador@ecologistica.test y conductor@ecologistica.test | contraseña: $clave"
Write-Host 'En el primer ingreso escanee el código QR con Google Authenticator o Microsoft Authenticator.'
Write-Host 'Para detener todo, cierre las dos ventanas de PowerShell que se abrieron.'
