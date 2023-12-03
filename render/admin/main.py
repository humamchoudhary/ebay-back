import sys

sys.path.insert(0, "../")
from flask import render_template, request, session, redirect
from settings import app, adminInit, role_required
from Models import Listing, User, Moderator, SuperUser, Developer, CustomerService
from Models.settings import CustomException
from modules.chat import getUserChats, getChat, sendchatUser


@app.route("/admin/")
def adminIndex():
    curUser = session.get("user")
    if curUser:
        adminUser = adminInit(id=curUser)
        if adminUser:
            session["adminType"] = adminUser
            return redirect("/admin/dashboard")
    else:
        return redirect("/admin/login")


@app.route("/admin/logs", methods=["POST", "GET"])
@role_required("developer", "superuser")
def adminLogs():
    logs = []
    with open("record.log") as f:
        for line in f:
            try:
                parts = line.split(" : ")
                date_level = parts[0]
                date, level = date_level.rsplit(" ", 1)
                message = parts[1].rstrip()
                logs.append((date, level, message))
            except:
                pass
    return render_template("/admin/logs.html", logs=logs)


@app.route("/admin/logs/filter", methods=["POST", "GET"])
def adminLogFilter():
    filterLevel = request.form.get("filterBy")
    query = request.form.get("query")

    logs = []
    with open("record.log") as f:
        for line in f:
            try:
                parts = line.split(" : ")
                date_level = parts[0]
                date, level = date_level.rsplit(" ", 1)
                message = parts[1].rstrip()

                if (filterLevel and filterLevel == level) or not filterLevel:
                    if (query and query in message) or not query:
                        logs.append((date, level, message))

            except Exception as e:
                print(e)

    print(filterLevel)
    print(query)
    return render_template(
        "/admin/frags/logTable.html",
        logs=logs,
        filters={"q": query, "level": filterLevel},
    )


@app.route("/admin/login")
def adminLogin():
    error = None
    if "error" in session:
        error = session.get("error")
        session.pop("error")

    return render_template("/admin/login.html", error=error)


@app.route("/admin/auth", methods=["POST"])
def adminAuth():
    email = request.form["email"]
    password = request.form["password"]
    adminType = adminInit(email=email)

    try:
        if adminType == "moderator":
            admin = Moderator(email, password=password)
        elif adminType == "superuser":
            admin = SuperUser(email, password=password)
        elif adminType == "customerservice":
            admin = CustomerService(email, password=password)
        elif adminType == "developer":
            admin = Developer(email, password=password)
        else:
            raise CustomException("Could not Login", 401)
        # admin = Admin(email=email, password=password)
        if admin and admin.validate() and admin.login():
            admin.reinit()
            session["user"] = admin._id
            session["adminType"] = adminType
            return redirect("/admin/dashboard")
        else:
            raise CustomException("Could not Login", 401)
    except Exception as e:
        session["error"] = {"code": e.code, "message": e.message}
        return redirect("/admin/login")


@app.route("/admin/logout")
def adminLogOut():
    session.pop("user")
    return redirect("/admin/")


@app.route("/admin/dashboard")
def adminDashboard():
    if session.get("user") and session.get("adminType"):
        return render_template("/admin/dashboard.html", role=session.get("adminType"))
    else:
        return redirect("/admin/login")


@app.route("/admin/search")
def adminSearch():
    item = Listing()
    res = item.find()
    return render_template("/admin/search.html", fragTag="lol", res=res)


@app.route("/admin/search/filter")
def adminSearchItem():
    item = Listing(name=request.args.get("name"))
    res = item.find()
    return render_template("/admin/frags/searchItems.html", res=res)


@app.route("/admin/search/changeFilter", methods=["POST"])
def adminChangeFilter():
    session["filterBy"] = request.args.get("filterBy")
    return "asd"


@app.route("/admin/superuser")
@role_required("superuser")
def adminSuperUser():
    return "Super User"


@app.route("/admin/addAdmin")
@role_required("superuser")
def addAdmin():
    error = None

    if "error" in session:
        error = session.get("error")
        session.pop("error")
    return render_template("/admin/adminSignup.html", error=error)


@app.route("/admin/signup", methods=["POST"])
@role_required("superuser")
def adminSignup():
    email = request.form["email"]
    password = request.form["password"]
    username = request.form["username"]
    role = request.form["role"]
    try:
        if role == "moderator":
            admin = Moderator(email, password=password, username=username)
        elif role == "superuser":
            admin = SuperUser(email, password=password, username=username)
        elif role == "customerservice":
            admin = CustomerService(email, password=password, username=username)
        elif role == "developer":
            admin = Developer(email, password=password, username=username)
        else:
            raise CustomException("Could not Login", 401)
        # admin = Admin(email=email, password=password)
        if admin and admin.validate() and admin.signup():
            session["error"] = {"code": 200, "message": "Successfull"}

        else:
            raise CustomException("Could not add Admin", 401)
    except Exception as e:
        session["error"] = {"code": e.code, "message": e.message}
    return redirect("/admin/addAdmin")
