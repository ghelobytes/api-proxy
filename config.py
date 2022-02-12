import os

API_KEY_NAME = "x-api-key-name"

config = {
    "google": {
        "part": "url",
        "key": "key",
        "value": os.getenv("GOOGLE_VISION_API_KEY", "NOT_SET")
    },
    "aws": {
        "part": "header",
        "key": "x-api-key",
        "value": os.getenv("AWS_API_KEY", "NOT_SET")
    }
}
