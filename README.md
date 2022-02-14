# API Proxy
This is a simple `fastapi` app for proxying API calls that require credentials.

The credentials will be sitting behind a proxy so it's not exposed to client applications.

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

## Sample usage

### Sample 1
Assuming an environment variable named `KEY_MY_GOOGLE_TRANSLATE_API=url|key|abcd-efgh-ijkl` was created and set.
This simply means:
- `url`: The API key will be attached to the `url` of the request to the API. Possible value `[url, header]`
- `key`: The word `key` will be added as a query parameter to the `url`
- `abcd-efgh-ijkl`: This is the actual API key and will be the value of the `key` query parameter

This is how the **proxied** request looks like:

```bash
curl -X POST \
  'https://api.ghelo.dev/proxy?url=https://translation.googleapis.com/language/translate/v2' \
  --header 'Accept: */*' \
  --header 'x-api-key-name: key_my_google_translate_api' \
  --header 'Content-Type: application/json' \
  -d '{
  "q": ["Hello world", "My name is Angelo"],
  "target": "tl"
}'
```

And this is how the actual request to the API looks like:

```bash
POST \
  'https://translation.googleapis.com/language/translate/v2?key=abcd-efgh-ijkl' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
```

> `POST` method was inherited from the proxied request


### Sample 2
Assuming an environment variable named `KEY_MY_CUSTOM_API=header|authorization|Bearer abcdefghijkl` was created and set.
This simply means:
- `header`: The API key will be attached as part of the header of the request to the API. Possible value `[url, header]`
- `authorization`: The word `authorization` will be use as an additional key to the request header.
- `Bearer abcdefghijkl`: This is the actual API authorization token and will be the value of the `authorization` header.


This is how the **proxied** request looks like:

```bash
curl -X GET \
  'https://api.ghelo.dev/proxy?url=https://api.service.com/v1/products' \
  --header 'Accept: */*' \
  --header 'x-api-key-name: key_my_custom_api' \
  --header 'Content-Type: application/json' \
```

And this is how the actual request to the API looks like:

```bash
GET \
  'https://api.service.com/v1/products' \
  --header 'Accept: */*' \
  --header 'x-api-key-name: key_my_custom_api' \
  --header 'Content-Type: application/json' \
  --header 'authorization: Bearer abcdefghijkl'
```

> `GET` method was inherited from the proxied request