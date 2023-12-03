import sys

sys.path.insert(0, "../")
from flask import render_template, request, session, redirect
from settings import app, adminInit, role_required
from Models import Listing, User
from Models.settings import CustomException
from modules.chat import getUserChats, getChat, sendchatUser


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["GET"])
def userCSChat():
    return render_template(
        "/chats.html", chats=getUserChats("65526e887bd14c16c1c19561")
    )


@app.route("/chat/<string:id>", methods=["POST", "GET"])
def userChat(id):
    if request.method == "POST":
        message = request.form["message"]
        sendchatUser(session.get("user"), message, id)

    return render_template(
        "/user/chat.html", chat=getChat(id), current_user=session.get("user")
    )


@app.route("/login")
def userLogin():
    error = None
    if "error" in session:
        error = session.get("error")
        session.pop("error")

    return render_template("/user/login.html", error=error)


@app.route("/auth", methods=["POST"])
def userAuth():
    email = request.form["email"]
    password = request.form["password"]

    try:
        user = User(email=email, password=password)
        if user and user.validate() and user.login():
            user.reinit()
            session["user"] = user._id
            return redirect("/")
        else:
            raise CustomException("Could not Login", 401)
    except Exception as e:
        print(e.args)
        session["error"] = {"code": e.code, "message": e.message}
        return redirect("/login")
