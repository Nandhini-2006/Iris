# Run Jaeger all-in-one with OTLP HTTP receiver enabled
# Port 4318 = OTLP HTTP (traces from your FastAPI app)
# Port 16686 = Jaeger UI  -> http://localhost:16686

docker run --rm -d `
    --name jaeger `
    -p 4318:4318 `
    -p 16686:16686 `
    -p 4317:4317 `
    -e COLLECTOR_OTLP_ENABLED=true `
    jaegertracing/all-in-one:latest

Write-Host "Jaeger started! Open http://localhost:16686 and look for 'ai-debugger-api' service."
