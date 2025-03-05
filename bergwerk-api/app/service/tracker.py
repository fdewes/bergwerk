from datetime import datetime
from data import db as data_db

def track_text(uid, role, text, buttons):
    ts = datetime.now().timestamp()
    data_db.track_text(uid, role, text, buttons, ts)
    