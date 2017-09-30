# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect
import vk, cgi
import base64
from flask import session
import json

app = Flask(__name__)
app.config["DEBUG"] = True

'''api = None;'''

apiArray = dict()

def getApi():
    api = None
    try:
        api = apiArray.get(session["login"])
        if api is None:
            raise Exception('api is none')
        '''api = vk.API(auth.startauth())'''
    except:
        try:
            s= vk.AuthSession('6121793', session["login"], session["password"],scope='photos, wall, messages')
            api = vk.API(s)
            apiArray.update([(session["login"], api)])
        except:
            return None
    return api

@app.route('/')
def index():
    api = None
    try:
        api = getApi()
    except:
        ''''''
    if api is not None:
        return redirect(url_for('im'))
    return render_template("index.html")

@app.route('/auth',methods=["GET", "POST"])
def oauth():
    try:
        import auth
        api = None
        try:
            api = getApi()
        except:
            ''''''
        if api is not None:
            return redirect(url_for('im'))
        import json,sys
        try:
            if request.method == "POST":
                form = request.form
                session["login"] = form["email"]
                session["password"] = form["password"]
        except Exception:
            return "err"
        except:
            error = "Authentication error. Please, check your email and password 1"
            return render_template("index.html",errors=error)
        api = getApi()
        if api is None:
            error = "Authentication error. Please, check your email and password 2"
            return render_template("index.html",errors=error)
        return redirect(url_for('im'))
    except:
        return redirect(url_for('index'))

@app.route('/im',methods=["GET", "POST"])
def im():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        return render_template("autherr.html")
    if request.method == "POST":
        import send
        try:
            form = request.form
            m = form["msg"]
            rid = form["toid"]
            isc = form["isChat"]
            msgid = send.sendMsg(api=api,msg=m,recid=rid,isChat=isc)
            return msgid
        except Exception:
            return 'error'
    #frarr = api.friends.get(fields="uid, first_name, last_name, photo")
    return render_template("im.html")


@app.route('/getmsg',methods=["GET","POST"])
def getmsgs():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    m = None;
    o = None;
    isChat = 0;
    try:
        if request.method == "POST":
            form = request.form
            m = form["uid"]
            o = form["offset"]
            isChat = form["isChat"]
    except Exception:
        return "exception"
    m = m + ""
    msg = None
    msg = api.messages.getHistory(user_id=m,offset=o)
    import json
    def json_list(list):
        lst = []
        for pn in list:
            d = {}
            d['data']=pn
            lst.append(d)
        return json.dumps(lst)
    return json_list(msg)

@app.route('/getChat',methods=["GET","POST"])
def getChat():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    m = None
    try:
        if request.method == "POST":
            form = request.form
            m = form["cid"]
    except Exception:
        return "exception"
    import execute as e
    code = 'var b = API.messages.getChat({"chat_id": ' + str(int(m)-2000000000) + '}); var c  = API.users.get({"user_ids": b.users,"fields": "photo_50,online"});  return {"chat": b, "chat_users": c};'
    msg = e.execute(a=api,c=code)
    return json.dumps(msg)

@app.route('/LPhistory',methods=["GET","POST"])
def lph():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    m = None

    if session["lpts"] == None or session["lpts"]=="":
        import execute as e
        code = 'var a = API.messages.getLongPollServer({"need_pts": 1}); return a;'
        r = e.execute(a=api,c=code)
        session["lpts"] = str(r["ts"])

    lpts = session["lpts"]
    lpfields = "photo,photo_medium_rec,sex,online,screen_name";
    try:
        if request.method == "POST":
            form = request.form
            m = form["max_msg_id"]
    except Exception:
        return "exception"
    '''m = (int)(m)-2'''
    m = (str)(m) + ""
    msg = api.messages.getLongPollHistory(ts=lpts,max_msg_id=m,fields=lpfields);
    import json
    def json_list(list):
        lst = []
        for pn in list:
            d = {}
            d['data']=pn
            lst.append(d)
        return json.dumps(lst)

    return json.dumps(msg)

@app.route('/getmsgprev',methods=["GET","POST"])
def getmsgsprev():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    try:
        if request.method == "POST":
            form = request.form
    except Exception:
        return "exception"
    msg = api.messages.getDialogs()
    import json
    def json_list(list):
        lst = []
        for pn in list:
            d = {}
            d['data']=pn
            lst.append(d)
        return json.dumps(lst)

    return json_list(msg)


@app.route('/getusers',methods=["GET","POST"])
def getusers():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    ulist = None
    try:
        if request.method == "POST":
            form = request.form
            ulist = form["user_ids"];
    except Exception:
        return "exception"
    r = api.users.get(user_ids=ulist,fields="photo_50,online")
    import json
    return json.dumps(r)

@app.route('/execute',methods=["GET","POST"])
def execute():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    startLongPolling = 0
    ts = 0
    try:
        if request.method == "GET":
            startLongPolling = int(request.args.get('startLongPolling'))
            ts = int(request.args.get('ts'))
    except Exception:
        pass
    dlgsOffset = 0
    try:
        if request.method == "GET":
            dlgsOffset = int(request.args.get('dialogsOffset'))
    except Exception:
        pass
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    import execute as e
    import json
    import requests
    code = ""
    if startLongPolling == 1:
        code = 'var a = API.messages.getLongPollServer({"need_pts": 1}); return a;'
        r = e.execute(a=api,c=code)
        session["lpserver"] = str(r["server"])
        session["lpkey"] = str(r["key"])
        session["lpts"] = str(r["ts"])
        url = "https://" + str(r["server"]) + "?act=a_check&key=" + str(r["key"]) + "&ts=" + str(r["ts"]) +"&wait=25&mode=2&version=2";
        quotes = requests.get(url)
        contents_file = quotes.text
        return str(contents_file)
        '''code = 'var b = API.messages.getLongPollHistory({"ts":' + str(r["ts"]) + ',"max_msg_id":' + str(lastMsgId) + '}); return b;'''
    elif startLongPolling == 2:
        ts = session["lpts"]
        try:
            if request.method == "GET":
                ts = int(request.args.get('ts'))
        except Exception:
            pass
        session["lpts"] = ts
        url = "https://" + session["lpserver"] + "?act=a_check&key=" + session["lpkey"] + "&ts=" + str(ts) +"&wait=25&mode=2&version=2";
        quotes = requests.get(url)
        contents_file = quotes.text
        return str(contents_file)
    else:
        code = 'var c = API.messages.getDialogs({"offset":' + str(dlgsOffset) + '}); var b = API.users.get({"user_ids": c@.uid,"fields": "photo_50,online"}); var a = API.users.get({"fields": "photo_50"}); return {"msgs": c,"users":b,"me": a};'
    r = e.execute(a=api,c=code)
    if startLongPolling == 1:
        pass
    return json.dumps(r)


@app.route('/gets',methods=["GET"])
def gets():

    '''
    code = 'var c = API.messages.getDialogs();  return {"msgs": c};
    '''
    u = ""
    try:
        if request.method == "GET":
            u = request.args.get('url')
    except Exception:
        return "exception"
    import urllib.request as urllib2
    r = urllib2.urlopen(u)
    return r.read()


@app.route('/offline',methods=["GET"])
def offline():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    if api is None:
        error = "Authentication error"
        return render_template("index.html",errors=error)
    r = api.account.setOffline();
    import json
    return json.dumps(r)

@app.route('/logout',methods=["GET"])
def logout():
    apiArray.pop(session["login"])
    session.pop('login', None)
    return redirect(url_for('index'))

@app.route('/getUsers',methods=["GET"])
def getUsers():
    api = None
    import execute as e

    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    uids = ""
    try:
        if request.method == "GET":
            uids = str(request.args.get('uids'))
    except:
        return "err"
    if api is None:
        error = "Authentication error"
        return redirect(url_for('index'),errors=error)
    code = 'var c = API.users.get({"user_ids": "' + uids + '"}); return c;'
    r = e.execute(a=api,c=code)
    return json.dumps(r)

@app.route('/file_upload',methods=["POST","GET"])
def fUpload():
    api = None
    try:
        api = getApi()
    except:
        return redirect(url_for('index'))
    upserv = api.photos.getMessagesUploadServer();


    form = cgi.FieldStorage()
    r = form.getvalue('file')

    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

    url = upserv["upload_url"]
    post_fields = {'photo': r}

    request = Request(url, urlencode(post_fields).encode())
    json1 = urlopen(request).read().decode()

    return json.dumps(json1)



app.secret_key = 'F13Zr47j\3yX R~X@@H(jmM]Lwf/,?KT'
