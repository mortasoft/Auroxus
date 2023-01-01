from flask import Flask, render_template
from flask import redirect


app = Flask(__name__)
version=0.001

@app.route('/')
def hello():
    configs = {"version": version, "title":"Dashboard"}
    return render_template('index.html',configs=configs)


if __name__ == "__main__":
    try:
        app.run(debug=True,host="0.0.0.0",port="5000")
    except Exception as e:
        print(e)
