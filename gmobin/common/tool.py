from datetime import datetime, timezone
import email.utils as eut
import base64

def get_current_time():
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    return now

def get_today_date(split=""):
    now = datetime.now().strftime(f"%Y{split}%m{split}%d")
    return now

def decode_gmo_base64_to_str(s):
    _s = s.split("\"")[1]
    bs = base64.urlsafe_b64decode(_s + '=' * (-len(_s) % 4))
    bl = []
    for b in bs:
        if b > 100:
            bl.append(44)
        else:
            bl.append(b)
    bs2 = bytearray(bl)
    r = bs2.decode("utf-8").split(",")
    return list(filter(lambda x: x != '', r))
