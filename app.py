from flask import Flask, redirect, url_for, request, render_template
import os
from dotenv import load_dotenv
from backend.models import auditron
import os.path

app = Flask(__name__)
version=0.001

# Load environmental variables from .env file
load_dotenv()
atron = auditron(user=os.getenv("db_user"),
                    password=os.getenv("db_password"),
                    host=os.getenv("db_host"),
                    port=int(os.getenv("db_port")),
                    database=os.getenv("db_database")
                    )

@app.route('/')
def hello():
    configs = {"version": version, "title":"Dashboard"}
    return render_template('index.html',configs=configs)


@app.route('/config/docker')
def config_docker():
    configs = {"version": version, "title":"Configuration / Docker"}
    containers = atron.list_docker_containers()
    return render_template('config/docker.html',configs=configs,containers=containers)


@app.route('/login',methods = ['GET'])
def login():
    name = request.args.get('name')
    print(name)
    return render_template('hola.html',name=name)


if __name__ == "__main__":
    try:
        app.run(debug=True,host="0.0.0.0",port="7000")
    except Exception as e:
        print(e)
