import os
import json
import requests

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
EMB_MODEL = os.environ["EMB_MODEL"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


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

def get_llm_answer(prompt):
    res = model.generate_content(prompt)
    return res.text