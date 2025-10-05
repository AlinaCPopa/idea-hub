Param(
  [string]$SpecPath = "../../spec/openapi.yaml",
  [string]$OutFile = "../../frontend/src/api/generated/types.ts"
)

if (-Not (Get-Command npx -ErrorAction SilentlyContinue)) {
  Write-Error "npx not found. Ensure Node.js is installed."; exit 1
}

npx openapi-typescript $SpecPath -o $OutFile
Write-Host "Generated types to $OutFile" -ForegroundColor Green
