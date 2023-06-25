import mariadb
import docker
import datetime
from colorama import Fore, Style
from celery import Celery
import nmap
import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

class db:
    def __init__(self, user, password,host,port,database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connect()

    def connect(self):
        try:
            self.conn = mariadb.connect(
                            user=self.user,
                            password=self.password,
                            host=self.host,
                            port=self.port,
                            database=self.database
                        )
            utils.print(f"Connected to the database '{self.host}/{self.database}:{self.port}' ")
        except mariadb.Error as e:
            utils.print(f"Error connecting to MariaDB Platform: {e}")
            exit(1)

        except TypeError as e:
            utils.print(f"You have an error on the port. Should be an integer {e}")
            exit(1)

        except AttributeError as e:
            utils.print(f"Error connecting to MariaDB Platform: {e}")
            exit(1)
        
        except Exception as e:
            utils.print(f"Unknown Error: {e}")
            exit(1)

    def execute_query(self, query,type="S",*params):
        try:
            cur = self.conn.cursor()
            cur.execute(query,*params)
            
            if type == "I":
                self.conn.commit()
                return cur.lastrowid
            else:
                columns = [i[0] for i in cur.description]
                self.conn.commit()
                return (columns,cur.fetchall())


                
        except mariadb.Error as e:
            print(f"Error: {e}")

    def print_results(self,data):
        print(data[0])
        for i in data[1]:
            print(i)

class aur0xus:
    def __init__(self, user, password,host,port,database):
        self.db = db(user,password,host,port,database)

    @app.task
    def ping_scan(target):
        arguments = '-R -sP'
        nm = nmap.PortScanner()
        nm.scan(target, arguments=arguments)
        result = []
        for host in nm.all_hosts():
            hostname = nm[host]['hostnames'][0]['name']
            ip_address = nm[host]['addresses']['ipv4']
            try:
                mac_address = nm[host]['addresses']['mac']
                vendor = nm[host]['vendor'][mac_address]
            except KeyError:
                mac_address = 'NULL'
                vendor = 'NULL'
            state = nm[host].state()
            result.append([datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), hostname,ip_address,mac_address,vendor,state ])
        print(result)


    def get_all_scanning_jobs(self):
        try:
            columns,data = self.db.execute_query("SELECT * FROM scanning_jobs")
            self.db.conn.cursor().close()
            return data
        except Exception as e:
            print(e)   

    def list_docker_containers(self):
        try:

            columns,data = self.db.execute_query("SELECT * FROM containers order by container_name asc")
            self.db.conn.cursor().close()
            containers=[]
            client = docker.from_env()

            for row in data:
                container_name = row[0]
                container_image = row[1]
                container_desc = row[2]
                try:
                    docker_container = client.containers.get(container_name)
                    print("The container exists")
                    containers.append([docker_container.id,container_name,docker_container.status,docker_container.image.tags[0],container_desc])
                except Exception as e:
                    print(f"The container {container_name} do not exists")
                    containers.append([None,container_name,"Non existant",container_image,container_desc])
                
            return containers
        except Exception as e:
            print(e)

class net_scan:
    def __init__(self):
        pass

class utils:
    """docstring for utils."""
    def print(text):
        date = datetime.datetime.now().strftime("%x %X")
        result = f"[{Fore.GREEN}{date}{Style.RESET_ALL}] {text}"
        print(result)

    def json_response(result, message, data):
        return {"result": result, "message": message, "data": data}
    