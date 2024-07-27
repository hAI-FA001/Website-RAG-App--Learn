

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
