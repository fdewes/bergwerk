from datetime import datetime
from data import db as data

def track_text(uid, role, text, buttons):
    ts = datetime.now().timestamp()
    data.track_text(uid, role, text, buttons, ts)
    