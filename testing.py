import os
from dotenv import load_dotenv
from backend.models import auditron



# Load environmental variables from .env file
load_dotenv()
audit_db = auditron(user=os.getenv("db_user"),
                    password=os.getenv("db_password"),
                    host=os.getenv("db_host"),
                    port=int(os.getenv("db_port")),
                    database=os.getenv("db_database"))

containers = audit_db.list_docker_containers()
print(containers)
