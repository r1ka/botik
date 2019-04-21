# botik

## Environment variables
- `TOKEN` – bot token. Required
- `PROXY` – a proxy url in format `http://0.0.0.0:8080/`. Optional

## Local
1. Install virtualenv and requirements: `make install`
2. Run: `make run`

## Docker
1. Download requirements: `make framework`
2. Build container: `make docker`
3. Run: `make docker-run`
