def sendMsg(api,msg,recid,isChat):
    from flask import request
    if request.method == "POST":
        if isChat == "1":
            try:
                recid = int(recid)-2000000000
                resp = api.messages.send(chat_id=recid, message=msg)
                return resp
            except Exception:
                return "chatErr"
        else:
            try:
                resp = api.messages.send(user_id=recid, message=msg)
                return "msg"
            except Exception:
                return 'msgError'
    return 'mainError'