def sendMsg(api,msg,recid):
    from flask import request
    if request.method == "POST":
        try:
            resp = api.messages.send(user_id=recid, message=msg)
            return resp
        except Exception:
            return 'Error'
    return 'Error'