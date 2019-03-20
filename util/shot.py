import os, re, time, pad
from datetime import datetime

def num(contents):
    se = re.search(r'S\d{2}E\d{2}', contents, re.IGNORECASE)
    sq = re.search(r'SQ\d{4}', contents, re.IGNORECASE)
    sh = re.search(r'SH\d{4}', contents, re.IGNORECASE)

    season = contents[se.start(0)+1:se.start(0)+3]
    episode = contents[se.start(0)+4:se.start(0)+6]
    sequence = contents[sq.start(0)+2:sq.start(0)+6]
    shot = contents[sh.start(0)+2:sh.start(0)+6]

    return {"season": season, "episode": episode, "sequence": sequence, "shot": shot}


def created(file_path):
    create_date = os.path.getmtime(file_path)
    dt = datetime.fromtimestamp(create_date)
    created = {
        "year": dt.year, 
        "month": pad.two(dt.month), 
        "day": pad.two(dt.day), 
        "hour": pad.two(dt.hour), 
        "second": pad.two(dt.second)}
    
    return created