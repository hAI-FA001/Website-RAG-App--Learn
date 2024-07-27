# Website RAG App

## About
App to learn about making a Generative AI full-stack app, using Flask backend with React frontend <br>
This app allows Retrieval-Augmented Generation on the input URL. <br>

Difference from the <a href="https://shwinda.medium.com/build-a-full-stack-llm-application-with-openai-flask-react-and-pinecone-part-1-f3844429a5ef"> tutorial </a>:
  - Gemini as LLM
  - "all-MiniLM-L6-v2" from HuggingFace as Embedding model
  - Some other fixes/changes to make it work

<br>

## How to run
To run backend: `python run.py` <br>
To run frontend `npm start` (inside frontend/client/)


<br>

## Environment variables setup
Setup the following private environment variables:
  - GEMINI_API_KEY
  - PINECONE_API_KEY
  - HF_TOKEN

Other environment variables used:
  - FLASK_ENV (e.g. "development")
  - EMB_MODEL (link to HF embedding model)
  - EMB_DIM (embedding dimension of the model)
  - PINECONE_INDEX_NAME (index you want to create)
  - PROMPT_LIMIT (limit on the length of prompt)
