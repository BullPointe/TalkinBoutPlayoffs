import psycopg2

class DatabaseConnection():

    def __init__(self) -> None:
        self.status = 0
    
    def create_connection(self):
        self.conn = psycopg2.connect(
            database='statistics',
            user='playoffsUser',
            host='localhost',
            port=26257
        )
        self.conn.set_session(autocommit=True)

    def execute_statement(self,statement: str):
        print(self.conn)
        self.cur = self.conn.cursor()
        exe = self.cur.execute(statement)
        self.result = self.cur.fetchall()
        

    
    
    





