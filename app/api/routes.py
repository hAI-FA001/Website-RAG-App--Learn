from . import api_blueprint
from flask import request, jsonify, Response, stream_with_context, json
from app.services import scraping_service, model_service, pinecone_service
from app.utils.helper_functions import make_chunks, build_prompt

import os
from dotenv import load_dotenv

load_dotenv()
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
    q = request.json["question"]
    h = request.json["chatHistory"]
    
    ctxt_chunks = pinecone_service.get_similar_chunks(q, PINECONE_INDEX_NAME)
    p = build_prompt(q, ctxt_chunks)


    def generate():
        ans = model_service.get_llm_answer(p, h, stream=True)
        for chunk in ans:
            yield chunk.text

    return Response(stream_with_context(generate()))

@api_blueprint.route('/delete-index', methods=['POST'])
def delete_index():
    pinecone_service.delete_index(PINECONE_INDEX_NAME)
    return jsonify({
        "message": f"Index {PINECONE_INDEX_NAME} deleted successfully."
    })