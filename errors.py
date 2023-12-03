from flask import render_template
from settings import app


@app.errorhandler(429)
def toomanyrequests(error):
    message = "too many requests" if not error.description else error.description
    status = 429
    return render_template("error.html", error={"code": status, "message": message})


@app.errorhandler(500)
def internalServerError(error):
    message = "Internal Server Error" if not error.description else error.description
    status = 500
    return render_template("error.html", error={"code": status, "message": message})


@app.errorhandler(404)
def Error404(error):
    message = "Page not found" if not error.description else error.description
    status = 404

    return render_template("error.html", error={"code": status, "message": message})


@app.errorhandler(401)
def ErrorUnAuth(error):
    message = "Unauthorized" if not error.description else error.description
    status = 401
    return render_template("error.html", error={"code": status, "message": message})


@app.errorhandler(403)
def Error(error):
    message = "Error Occured" if not error.description else error.description
    status = 403
    return render_template("error.html", error={"code": status, "message": message})


@app.errorhandler(406)
def internalServerError(error):
    message = "Not Acceptable" if not error.description else error.description
    status = 406
    return render_template("error.html", error={"code": status, "message": message})
