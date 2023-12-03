from settings import app
import backend
import errors
import render
import settings

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
