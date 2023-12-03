

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
