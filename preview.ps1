param([int]$Port = 8000)

# Local-only preview for this static website. Stop with Ctrl+C.
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $Port)
$types = @{
    '.html' = 'text/html; charset=utf-8'
    '.css' = 'text/css; charset=utf-8'
    '.js' = 'text/javascript; charset=utf-8'
    '.png' = 'image/png'
    '.ico' = 'image/x-icon'
    '.ttf' = 'font/ttf'
}
$listener.Start()
Write-Host "Development preview: http://localhost:$Port"
Write-Host 'Refresh your browser after saving changes. Press Ctrl+C to stop.'
try {
    while ($true) {
        $client = $listener.AcceptTcpClient()
        try {
            $stream = $client.GetStream()
            $stream.ReadTimeout = 3000
            $reader = [IO.StreamReader]::new($stream)
            $request = $reader.ReadLine()
            if (-not $request) { continue }
            do { $header = $reader.ReadLine() } while ($header)
            $parts = $request.Split(' ')
            $method = $parts[0]
            $relative = [Uri]::UnescapeDataString(($parts[1] -split '\?')[0]).TrimStart('/')
            if (-not $relative) { $relative = 'index.html' }
            # Only public site files, never Git metadata or local documents.
            $allowed = $relative -match '^(index\.html|privacy\.html|favicon(?:-\d+)?\.(png|ico)|assets/[a-zA-Z0-9_-]+\.(png|css|js|ttf))$'
            $status = '404 Not Found'
            $type = 'text/plain; charset=utf-8'
            $body = [Text.Encoding]::UTF8.GetBytes('Not found')
            if ($method -notin @('GET', 'HEAD')) {
                $status = '405 Method Not Allowed'
                $body = [Text.Encoding]::UTF8.GetBytes('Method not allowed')
            } elseif ($allowed -and (Test-Path -LiteralPath (Join-Path $root $relative) -PathType Leaf)) {
                $file = Join-Path $root $relative
                $body = [IO.File]::ReadAllBytes($file)
                $type = $types[[IO.Path]::GetExtension($file)]
                $status = '200 OK'
            }
            $response = "HTTP/1.1 $status`r`nContent-Type: $type`r`nContent-Length: $($body.Length)`r`nCache-Control: no-store`r`nX-Content-Type-Options: nosniff`r`nConnection: close`r`n`r`n"
            $bytes = [Text.Encoding]::ASCII.GetBytes($response)
            $stream.Write($bytes, 0, $bytes.Length)
            if ($method -ne 'HEAD') { $stream.Write($body, 0, $body.Length) }
        } catch {
            Write-Verbose "Preview request ended: $_"
        } finally {
            $client.Dispose()
        }
    }
} finally {
    $listener.Stop()
}
