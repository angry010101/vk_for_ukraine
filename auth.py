def startauth():
    from flask import request
    import vk
    if request.method == "POST":
        try:
            form = request.form
            em = form["email"]
            ps = form["password"]
            session = vk.AuthSession('6121793', em, ps,scope='wall, messages')
            '''api = vk.API(session)'''
            return session
        except Exception:
            return None
    return None

startauth()
