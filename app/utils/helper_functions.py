import os
from dotenv import load_dotenv

load_dotenv()
PROMPT_LIMIT = os.environ["PROMPT_LIMIT"]

def make_chunks(text, ch_sz=200):
    sentences = text.split(". ")
    chs = []
    
    cur_ch = ""
    for s in sentences:
        # combine if total length will not exceed chunk size
        if len(cur_ch) + len(s) <= ch_sz:
            cur_ch += s + ". "
        # else start new chunk
        else:
            chs.append(cur_ch)
            cur_ch = s + ". "
    
    # if a chunk still remains
    if cur_ch:
        chs.append(cur_ch)
    
    return chs

def build_prompt(query, ctxt_chunks):
    prompt_start = (
        "Answer the question based on the given context. if you don't know" \
        "the answer based on the provided context, just responsed with 'I don't know'." \
        "Return just the answer and nothing else, do not add anything else." \
        "Make sure your response is in markdown format." \
        "\n\nContext:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}"\
        "\nAnswer:"
    )
    PROMPT_LIMIT -= (len(prompt_start) + len(prompt_end))

    prompt = ""
    # find # chunks that can fit in PROMPT_LIMIT
    for i in range(1, len(ctxt_chunks)):
        if len("\n\n---\n\n".join(ctxt_chunks[:i])) >= PROMPT_LIMIT:
            prompt = (
                prompt_start
                + "\n\n---\n\n".join(ctxt_chunks[:i-1])
                + prompt_end
            )
            break
        elif i == len(ctxt_chunks) - 1:
            prompt = (
                prompt_start
                + "\n\n---\n\n".join(ctxt_chunks)
                + prompt_end
            )
    
    return prompt