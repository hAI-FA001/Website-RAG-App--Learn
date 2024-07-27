from . import api_blueprint

@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    # scrape the url, generate embedding, upload to vector db
    pass

@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
    # embed user's query, find relevant docs from vector db, build prompt, send to LLM API
    pass
