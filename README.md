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
Assuming an environment variable named `KEY_MY_GOOGLE_TRANSLATE_API=url|key|abcd-efgh-ijkl` was created and set.
This simply means:
- `url`: The API key will be attached to the `url` of the request to the API. Possible value `[url, header]`
- `key`: The word `key` will be added as a query parameter to the `url`
- `abcd-efgh-ijkl`: This is the actual API key and will be the value of the `key` query parameter

The actual request to the API will look like this:
```
https://translation.googleapis.com/language/translate/v2?key=abcd-efgh-ijkl
```

This is how the proxied request looks like:

```bash
# request
curl -X POST \
  'https://api.ghelo.dev/proxy?url=https://translation.googleapis.com/language/translate/v2' \
  --header 'Accept: */*' \
  --header 'x-api-key-name: key_my_google_translate_api' \
  --header 'Content-Type: application/json' \
  -d '{
  "q": ["Hello world", "My name is Angelo"],
  "target": "tl"
}'

# response
{
  "data": {
    "translations": [
      {
        "translatedText": "Hello mundo",
        "detectedSourceLanguage": "en"
      },
      {
        "translatedText": "Ang pangalan ko ay Angelo",
        "detectedSourceLanguage": "en"
      }
    ]
  }
}
```