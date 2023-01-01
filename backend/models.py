import mariadb


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
                return (columns,cur.fetchall())


                
        except mariadb.Error as e:
            print(f"Error: {e}")

    def print_results(self,data):
        print(data[0])
        for i in data[1]:
            print(i)


