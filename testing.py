from backend.models import db

database = db(user="root",password="Trapped-Hungrily3-Tipping",host="mortasoft.xyz",port=3366,database="hacking")

result = database.execute_query("INSERT INTO domain (name,url,description) VALUES (?,?,?)","I", ("Mortasoft.com","www.mortasoft.com","Sitio Mortasoft"))
print(result)

import docker
client = docker.from_env()
for container in client.containers.list():
  print(f"{container.name} {container.image}")