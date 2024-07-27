import pinecone
from app.services.model_service import get_embedding
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
EMB_DIM = os.environ['EMB_DIM']

pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

def embed_and_upload(chunks, index_name):
    if index_name in pc.list_indexes():
        pc.delete_index(name=index_name)
    
    pc.create_index(
        name=index_name,
        dimension=int(EMB_DIM),
        metric='cosine',
        spec={
            "serverless": {
                "cloud": "aws",
                "region": "us-east-1"
            }
        }
    )
    index = pc.Index(index_name)

    embs_with_ids = []
    for i, ch in enumerate(chunks):
        emb = get_embedding(ch)
        embs_with_ids.append((str(i), emb, ch))
    
    upserts = [(id_, vec, {"chunk_text": text})
               for id_, vec, text in embs_with_ids]
    
    index.upsert(upserts)

def get_similar_chunks(query, index_name):
    q_emb = get_embedding(query)
    
    idx = pc.Index(index_name)
    q_results = idx.query(
        vector=q_emb,
        top_k=3,
        include_metadata=True
    )

    ctxt_chunks = [
        x["metadata"]["chunk_text"]
        for x in q_results["matches"]
    ]
    
    return ctxt_chunks