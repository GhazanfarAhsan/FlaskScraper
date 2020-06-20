import mysql.connector
class database:
    def __init__(self):
        self.host = "localhost"
        self.username = "root"
        self.password = ""
        self.database = "sidea_old"

    def connection(self):
        try:
            sidea_old = mysql.connector.connect(host=self.host,user=self.username,password=self.password,database=self.database)
            Conn = sidea_old.cursor()
            return [Conn,sidea_old]
        except:
            print("Error in Connection")
        