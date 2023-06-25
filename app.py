from flask import Flask, redirect, url_for, request, render_template
import os
from dotenv import load_dotenv
from backend.models import aur0xus,utils
import os.path
from celery import Celery

# Initialize Flask
app = Flask(__name__)

# Initialize version
version=0.02

# Load environmental variables from .env file
load_dotenv()

utils.print(f"Starting Aur0xus Dashboard v{version}") 




ax = aur0xus(user=os.getenv("db_user"),
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
    containers = ax.list_docker_containers()
    return render_template('config/docker.html',configs=configs,containers=containers)


@app.route('/login',methods = ['GET'])
def login():
    name = request.args.get('name')
    print(name)
    return render_template('hola.html',name=name)


@app.route('/scanning', methods=['GET', 'POST'])
def scanning():
    configs = {"version": version, "title":"Scanning"}
    if request.method == 'GET':
        jobs = ax.get_all_scanning_jobs()
        return render_template('scanning/scan.html',configs=configs,jobs=jobs)
    elif request.method == 'POST':
        scan_ip = request.form.get('scanIp')
        scan_type = request.form.get('scanType')
        if scan_type == "ping":
            # Enqueue the Celery task
            result = ax.ping_scan(scan_ip)
            jobs = ax.get_all_scanning_jobs()
            return render_template('scanning/scan.html',configs=configs,jobs=jobs)



if __name__ == "__main__":
    try:
        app.run(debug=True,host="0.0.0.0",port="7000")
    except Exception as e:
        print(e)
