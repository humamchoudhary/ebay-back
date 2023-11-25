from settings import app
from flask import render_template, request, session, redirect, flash
from Models import Listing, User, Admin
from Models.settings import CustomException


@app.route("/admin/")
def adminIndex():
    curUser = session.get("user")
    if curUser:
        adminUser = Admin(id=curUser)
        if adminUser:
            return redirect("/admin/dashboard")
    else:
        return redirect("/admin/login")


@app.route("/")
def test():
    raise ValueError("adsd")


@app.route("/admin/login")
def adminLogin():
    error = None
    if "error" in session:
        print("ASdsa")
        error = session.get("error")
        session.pop("error", None)

    return render_template("/admin/login.html", error=error)


@app.route("/admin/auth")
def adminAuth():
    email = request.args.get("email")
    password = request.args.get("password")
    print(email)
    print(password)
    admin = Admin(email=email, password=password)
    try:
        if admin.validate() and admin.login():
            admin.reinit()
            session["user"] = admin._id
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
    return "dashboard"


@app.route("/admin/search")
def adminSearch():
    query = request.args.get("name")
    # l = Listing()
    return render_template("/admin/search.html", fragTag="lol")


@app.route("/admin/search/changeFilter", methods=["POST"])
def adminChangeFilter():
    session["filterBy"] = request.args.get("filterBy")
    print(request.form.get("filterBy"))
    return "asd"


# @app.route("/admin/")
# def indexADmin():
#     return render_template("adminindex.html")


# @app.route("/")
# def index():
#     item = Listing()

#     return render_template("index.html", products=item.find())


# @app.route("/cart")
# def cart():
#     u = User(id=session.get("user"))
#     cartData = u.find()[0]["cart"]
#     cartItems = []
#     for cartItem in cartData:
#         print(cartItem)
#         cartItems.append(
#             {**Listing(id=cartItem["id"]).find()[0], "amount": cartItem["amount"]}
#         )
#     print(cartItems)
#     return render_template("cart.html", cart=cartItems)


# @app.route("/cart")
# def cart():
#     u = User(id=session.get("user"))
#     cartData = u.find()[0]["cart"]
#     cartItems = []
#     for cartItem in cartData:
#         print(cartItem)
#         cartItems.append(
#             {**Listing(id=cartItem["id"]).find()[0], "amount": cartItem["amount"]}
#         )
#     print(cartItems)
#     return render_template("cartItem.html", cartItem=cartItems)


# @app.route("/admin/search")
# def adminSearchItem():
#     item = Listing(name=request.args.get("name"))
#     res = item.find()
#     print(res)
#     return render_template("adminsearchArea.html", results=res)


# @app.route("/admin/verify", methods=["POST"])
# def adminVerify():
#     item = Listing(id=request.form.get("id"))
#     item._valid = True
#     item.verify("6559d5872ad0ba7a85470b4d")
#     res = item.find()[0]
#     print(res)
#     return render_template("components/renderItem.html", item=res)


# @app.route("/admin/renderItem")
# def renderAdminItem():
#     item = Listing(name=request.args.get("name"))
#     res = item.find()[0]
#     return render_template("components/renderItem.html", item=res)
