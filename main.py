from http.client import HTTPException
import requests
import urllib.parse

from types import SimpleNamespace

from config import config, API_KEY_NAME

from fastapi import FastAPI, Request, HTTPException, Response

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "ghelo.dev api"
    }


@app.get("/proxy")
@app.post("/proxy")
async def proxy(request: Request):

    url: str = urllib.parse.unquote(
        request.query_params.get("url", "")
    )

    req: SimpleNamespace = SimpleNamespace(
        method=request.method,
        url=url,
        headers={
            k: v for k, v in request.headers.items()
            if k not in [
                "host", "connection", "accept-encoding",
                "content-length", "content-type"
            ]
        },
        params={},
        data=None,
    )
    if req.method == "POST":
        req.data = await request.body()

    if req.url == "":
        raise HTTPException(
            status_code=400,
            detail=(
                "Destination URL was not provided. "
                "Add `/proxy?url={destination-url}` "
                "to the request."
            )
        )
    if API_KEY_NAME not in req.headers:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Missing required header `{API_KEY_NAME}`."
            )
        )

    api_key_name_value: str = req.headers[API_KEY_NAME]

    if api_key_name_value not in config:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unexpected `{API_KEY_NAME}` value."
            )
        )

    part: str = config[api_key_name_value]["part"]
    key: str = config[api_key_name_value]["key"]
    value: str = config[api_key_name_value]["value"]

    if part == "url":
        req.params[key] = value
    elif part == "header":
        req.headers[key] = value
    else:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unprocessable key configuration."
            )
        )

    resp: requests.models.Response = requests.request(
        req.method,
        req.url,
        headers=req.headers,
        params=req.params,
        data=req.data,
    )

    return Response(
        content=resp.text,
        status_code=resp.status_code,
        media_type=resp.headers["content-type"],
    )
