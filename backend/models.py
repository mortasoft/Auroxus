import mariadb
import docker

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
            print(f"You are connected to the database '{self.host}/{self.database}:{self.port}' ")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            exit(1)

        except TypeError as e:
            print(f"You have an error on the port. Should be an integer {e}")
            exit(1)

        except AttributeError as e:
            print(f"Error connecting to MariaDB Platform: {e}")
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

class auditron:
    def __init__(self, user, password,host,port,database):
        self.db = db(user,password,host,port,database)

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