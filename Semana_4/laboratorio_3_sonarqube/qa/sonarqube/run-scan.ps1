param(
    [string]$SonarToken = $env:SONAR_TOKEN
)

if ([string]::IsNullOrWhiteSpace($SonarToken)) {
    throw 'Define SONAR_TOKEN o pasa -SonarToken al ejecutar el script.'
}

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..\src')
$qaRoot = Resolve-Path $PSScriptRoot
$projectRootPath = ($projectRoot.Path -replace '\\', '/')
$qaRootPath = ($qaRoot.Path -replace '\\', '/')

docker run --rm `
  -e SONAR_HOST_URL=http://host.docker.internal:9000 `
  -e SONAR_TOKEN=$SonarToken `
    -v "$($projectRootPath):/usr/src/project" `
    -v "$($qaRootPath)/sonar-project.properties:/usr/src/project/sonar-project.properties" `
  -w /usr/src/project `
  sonarsource/sonar-scanner-cli:latest
