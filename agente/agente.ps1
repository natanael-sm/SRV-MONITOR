# AGENTE SRV-MONITOR

# URL API
$apiUrl = "http://127.0.0.1:5000/api/equipos/checkin"

# HOSTNAME
$hostname = $env:COMPUTERNAME

# IP
$ip = (
    Get-NetIPAddress `
    -AddressFamily IPv4 |
    Where-Object {
        $_.IPAddress -notlike "127.*"
    } |
    Select-Object -First 1
).IPAddress

# SISTEMA OPERATIVO
$sistema_operativo = (
    Get-CimInstance Win32_OperatingSystem
).Caption

# CPU %

$cpuCounter = New-Object System.Diagnostics.PerformanceCounter(
    "Processor",
    "% Processor Time",
    "_Total"
)

$null = $cpuCounter.NextValue()

Start-Sleep -Seconds 1

$cpu = $cpuCounter.NextValue()

$cpu = [math]::Round($cpu,2)

# RAM %

$os = Get-CimInstance Win32_OperatingSystem

$totalRAM = $os.TotalVisibleMemorySize
$freeRAM = $os.FreePhysicalMemory

$usedRAM = $totalRAM - $freeRAM

$ramPercent = ($usedRAM / $totalRAM) * 100

$ramPercent = [math]::Round($ramPercent,2)

# DISCO %

$disk = Get-CimInstance Win32_LogicalDisk `
    -Filter "DeviceID='C:'"

$diskUsed = (
    ($disk.Size - $disk.FreeSpace) / $disk.Size
) * 100

$diskUsed = [math]::Round($diskUsed,2)

# JSON

$body = @{

    hostname = $hostname
    ip = $ip
    sistema_operativo = $sistema_operativo
    estado = "Online"

    cpu_actual = $cpu
    ram_actual = $ramPercent
    disco_actual = $diskUsed

} | ConvertTo-Json

# ENVIAR API

Invoke-RestMethod `
    -Uri $apiUrl `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host ""
Write-Host "Check-in enviado correctamente"
Write-Host ""

Write-Host "CPU: $cpu %"
Write-Host "RAM: $ramPercent %"
Write-Host "DISCO: $diskUsed %"