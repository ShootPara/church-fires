$ErrorActionPreference = 'Stop'

$destination = Join-Path $PSScriptRoot '..\ignore\Deconstructed Original Slides'
New-Item -ItemType Directory -Force -Path $destination | Out-Null

1..102 | ForEach-Object {
    $slideFolder = Join-Path $destination ('{0:D3} Slide {1}' -f $_, $_)
    New-Item -ItemType Directory -Force -Path $slideFolder | Out-Null
}

$slideTwo = Join-Path $destination '002 Slide 2'
New-Item -ItemType Directory -Force -Path (Join-Path $slideTwo '001 Clipping 1') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $slideTwo '002 Clipping 2') | Out-Null

Write-Output "Created slide folders at $destination"
