$ErrorActionPreference = "Stop"

try {
    $comandoPython = Get-Command python
} catch {
    Write-Host "Python nao encontrado no PATH." -ForegroundColor Red
    exit 1
}

$caminhoVenv = ".vscode\.venv"
$pythonExeAtual = $comandoPython.Source
$pythonExeVenv = "$caminhoVenv\Scripts\python.exe"
$pythonExeGlobal = Resolve-Path "$Env:ProgramFiles\\Python*\\python.exe"
$versaoRecomendada = "3.13.5"
$versaoInstalada = $comandoPython.Version.ToString().Substring(0, 6)

if (-not $pythonExeGlobal) {
    Write-Host "Erro ao obter o Python Global. Verifique a instalacao" -ForegroundColor Red
    exit 1
}

if ($versaoInstalada -notlike "$versaoRecomendada*") {
    Write-Host "Versao Python invalida.`nExigida: $versaoRecomendada`nAtual: $versaoInstalada" -ForegroundColor Red
    exit 1
}

if ($pythonExeAtual -like "*$pythonExeGlobal") {
    Write-Host "Criando o ambiente virtual..."
    & $pythonExeAtual -m venv $caminhoVenv --upgrade-deps
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Falha ao criar o ambiente virtual." -ForegroundColor Red
        exit 1
    }
    Write-Host "Ambiente Virtual criado em: '$caminhoVenv'" -ForegroundColor Green
} else {
    Write-Host "Ambiente Virtual (venv) ja configurado.`n" -ForegroundColor Green
}


Write-Host "Sincronizando as bibliotecas a partir do requirements.txt..."
& $pythonExeGlobal -m pip install pip-tools --upgrade --disable-pip-version-check

& $pythonExeGlobal -m piptools sync requirements.txt --python-executable $pythonExeVenv --pip-args "--disable-pip-version-check --require-virtualenv"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro durante a sincronizacao das bibliotecas." -ForegroundColor Red
    exit 1
}
Write-Host "Bibliotecas sincronizadas com sucesso." -ForegroundColor Green
Write-Host "Pressione alguma tecla para fechar..." -ForegroundColor Yellow