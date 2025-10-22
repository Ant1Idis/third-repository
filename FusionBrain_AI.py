import requests
import json
import asyncio
import config

HEADERS = {
    "X-Key": f"Key {config.API_KEY}",
    "X-Secret": f"Secret {config.SECRET_KEY}",
}

URL = 'https://api-key.fusionbrain.ai/'

def get_pipeline():
    response = requests.get(URL + 'key/api/v1/pipelines', headers=HEADERS)
    data = response.json()
    return data[0]['id']

async def generate(prompt, style="kandinsky", size="medium"):
    # Map size to resolution (width and height)
    size_map = {
        "small": 248,
        "medium": 496,
        "big": 1080
    }
    resolution = size_map.get(size.lower(), 496)  # Default to medium if invalid

    params = {
        "type": "GENERATE",
        "style": style.lower(),  # Ensure style is lowercase for consistency
        "numImages": 1,
        "width": resolution,
        "height": resolution,
        "generateParams": {"query": prompt},
    }
    files = {
        "pipeline_id": (None, get_pipeline()),
        "params": (None, json.dumps(params), "application/json"),
    }
    response = requests.post(URL + "key/api/v1/pipeline/run", headers=HEADERS, files=files)
    data = response.json()
    attempts = 0
    while attempts < 40:
        response = requests.get(URL + f"key/api/v1/pipeline/status/{data['uuid']}", headers=HEADERS)
        data = response.json()
        if data["status"] == "DONE":
            return data["result"]["files"]
        attempts += 1
        await asyncio.sleep(3)
    return None