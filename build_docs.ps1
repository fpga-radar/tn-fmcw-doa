$ErrorActionPreference = "Stop"

$notebooks = @(
    "01_signal_model.ipynb",
    "02_covariance_matrix.ipynb",
    "03_fmcw_mimo.ipynb",
    "04_fft_beamformer.ipynb",
    "05_bartlett.ipynb",
    "06_capon_mvdr.ipynb",
    "07_music.ipynb",
    "08_esprit.ipynb",
    "09_corner_reflectors.ipynb",
    "10_street_scene.ipynb",
    "index.ipynb"
)

$titles = @{
    "01_signal_model.html"          = "Signal Model"
    "02_covariance_matrix.html"     = "Covariance Matrix"
    "03_fmcw_mimo.html"             = "FMCW MIMO DoA Processing"
    "04_fft_beamformer.html"        = "FFT Beamformer"
    "05_bartlett.html"              = "Bartlett Beamformer"
    "06_capon_mvdr.html"            = "Capon / MVDR Beamformer"
    "07_music.html"                 = "MUSIC"
    "08_esprit.html"                = "ESPRIT"
    "09_corner_reflectors.html"     = "Corner Reflectors Validation"
    "10_street_scene.html"          = "Street Scene Validation"
    "index.html"                    = "index"
}

$inputDir = ".\notebooks"
$outputDir = ".\docs"

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

foreach ($notebook in $notebooks) {
    $path = Join-Path $inputDir $notebook

    if (-not (Test-Path $path)) {
        Write-Warning "Skipping missing notebook: $path"
        continue
    }

    Write-Host "Converting $notebook..."

    jupyter nbconvert `
        --to html `
        --template classic `
        $path `
        --output-dir $outputDir

    if ($LASTEXITCODE -ne 0) {
        throw "Conversion failed for $notebook"
    }
}

Write-Host "All notebook pages were generated in $outputDir"


Get-ChildItem .\docs\*.html | ForEach-Object {

    $content = Get-Content $_.FullName -Raw

    # Fix published image paths
    $content = $content.Replace(
        '../docs/images/',
        'images/'
    )

    # Set browser tab title
    if ($titles.ContainsKey($_.Name)) {

        $pageTitle = $titles[$_.Name]

        $content = $content -replace `
            '<title>.*?</title>', `
            "<title>$pageTitle</title>"
    }

    [System.IO.File]::WriteAllText(
        $_.FullName,
        $content,
        [System.Text.UTF8Encoding]::new($false)
    )
}