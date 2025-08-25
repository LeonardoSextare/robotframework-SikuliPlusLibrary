$extensoes = (Get-Content -Path ".vscode\extensions.json" -Raw | ConvertFrom-Json).recommendations
$extensoes_instaladas = code --list-extensions

foreach ($extensao in $extensoes) {
    if ($extensoes_instaladas -contains $extensao) {
        Write-Host "A extensao $extensao ja esta instalada." -ForegroundColor Cyan
        continue
    } 

    Write-Host "Instalando a extensao: $extensao"
    $saida = code --install-extension $extensao
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao instalar a extensao: $extensao. Detalhes do erro: $saida" -ForegroundColor Red
        continue
    }
    Write-Host "Extensao $extensao instalada com sucesso." -ForegroundColor Green
}