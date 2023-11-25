from flask import jsonify
from settings import app, create_response


@app.errorhandler(429)
def toomanyrequests(error):
    return create_response(
        message="too many requests" if not error.description else error.description,
        error=True,
        status=429,
    )


@app.errorhandler(500)
def internalServerError(error):
    print(error.description)
    return create_response(
        message="Internal Server Error" if not error.description else error.description,
        error=True,
        status=500,
    )


@app.errorhandler(404)
def Error404(error):
    print(error.description)
    return create_response(
        message="Page not found" if not error.description else error.description,
        error=True,
        status=404,
    )


@app.errorhandler(401)
def ErrorUnAuth(error):
    return create_response(
        message="Unauthorized" if not error.description else error.description,
        error=True,
        status=401,
    )


@app.errorhandler(403)
def Error(error):
    return create_response(
        message="Error Occured" if not error.description else error.description,
        error=True,
        status=403,
    )


@app.errorhandler(406)
def internalServerError(error):
    return create_response(
        message="Not Acceptable" if not error.description else error.description,
        error=True,
        status=406,
    )
