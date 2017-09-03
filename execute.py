def execute(a,c):
    try:
        r = a.execute(code=c)
    except Exception:
        return None
    return r

