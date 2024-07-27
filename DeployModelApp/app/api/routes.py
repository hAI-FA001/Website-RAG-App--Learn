from . import api_blueprint
from flask import request, jsonify
from app.services import scraping_service, model_service, pinecone_service
from app.utils.helper_functions import make_chunks

import os
from dotenv import load_dotenv

PINECONE_INDEX_NAME = os.environ['PINECONE_INDEX_NAME']

@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    # scrape the url, generate embedding, upload to vector db
    url = request.json["url"]
    url_txt = scraping_service.scrape(url)
    
    chs = make_chunks(url_txt)
    pinecone_service.embed_and_upload(chs, PINECONE_INDEX_NAME)

    res_json = {
        "message": "Chunks embedded and uploaded to Pinecone"
    }

    return jsonify(res_json)

@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
    # embed user's query, find relevant docs from vector db, build prompt, send to LLM API
    pass
