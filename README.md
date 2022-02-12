# API Proxy
This is a simple `fastapi` app for proxying API calls that require credentials.

The credentials will be sitting behing the proxy so it's not exposed to client applications.

## Environment variables
```
# pattern
# ENV var must start with KEY_*
KEY_NAME_OF_API={part}|{key}|{api_key_value}

# example
# attach the API key to the url via `key` parameter
KEY_GOOGLE_API=url|key|abcd-efgh-ijkl

# attach the API key to header via `authorization` header key
KEY_AWS_API=header|authorization|Bearer token
```

## Running locally
- Initialize virtual environment (`venv` or `direnv`)
- Create a `.env` with the key values
- Run `make setup_uvicorn`
- Run `make run` to run locally

## Deployment
- Run `deta new` to deploy the app to `deta.sh`
- Run `deta deploy` for subsequent change deployment
- Run `deta update -e .env` to update the instance environment variables
