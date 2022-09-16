import mysql.connector
class database:
    def __init__(self):
        self.host = "localhost"
        self.username = "root"
        self.password = ""
        self.database = "amazon_products"

    def connection(self):
        try:
            connection = mysql.connector.connect(host=self.host,user=self.username,password=self.password,database=self.database)
            Conn = connection.cursor(prepared = True);
            return [Conn,connection]
        except:
            print("Error in Connection")

    def insert(self,table,columns,values):
        values_str = "";
        
        try:
            for column in columns:
                values_str += "%s,"
                values_str = values_str[0:len(values_str)-1]+values_str[len(values_str)-1:];
            
            
            statement = "INSERT INTO " + table +"("+ columns + ") VALUES ("+values_str+")";
            connection = self.connection();
            connection[0].execute(statement, values)
            connection[1].commit()
            print(connection[0].rowcount, "record inserted.");
            return connection[0].rowcount;
        except Exception as e:
            print("Error in Insert",e);

        