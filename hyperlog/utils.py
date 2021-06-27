import datetime
from hashlib import md5
# タイムゾーンの生成
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
def isiterable(x):
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True
def md5sum(filename, limit=0):
    fhash = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            fhash.update(chunk)
    return fhash.hexdigest()[-limit:]
def ftimedelta(td):
    p1, p2 = str(td).rsplit(':', 1)
    return ':'.join([p1, '{:02d}'.format(int(float(p2)))])
def getdatetime():
    return datetime.datetime.now(tz=JST)

def unixtojst(timesp):
    return datetime.datetime.fromtimestamp(timesp, JST)

def utctojst(time):
    return time.replace(tzinfo=datetime.timezone.utc).astimezone(JST)