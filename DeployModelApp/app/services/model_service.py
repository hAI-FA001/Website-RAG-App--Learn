import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

EMB_MODEL = os.environ["EMB_MODEL"]

def get_embedding(chunk):
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{EMB_MODEL}"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {os.environ["HF_TOKEN"]}",
        }

    res = requests.post(api_url, headers=headers, json={
        "inputs": chunk,
        "options": {
            "wait_for_model": True
        }
    })

    return res.json()
