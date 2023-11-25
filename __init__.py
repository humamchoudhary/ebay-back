from settings import app
import errors
import backend
import render

if __name__ == "__main__":
    # t = threading.Thread(target=run_schedule)
    # t.start()
    app.run(host="0.0.0.0", debug=True)
