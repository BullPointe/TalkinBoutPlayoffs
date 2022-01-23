import sqlite3

class DatabaseConnection():

    def __init__(self) -> None:
        self.status = 0
    
    def create_connection(self):
        # self.conn = create_engine('cockroachdb://root@127.0.0.1:26257/stats')
        self.conn = sqlite3.connect('example.db')
        self.cur = self.conn.cursor()
        # self.conn.set_session(autocommit=True)

    def close_connection(self):
        self.conn.close()

    def execute_statement(self,statement: str):
        print(self.conn)
        exe = self.cur.execute(statement)
        self.result = self.cur.fetchall()
        

    
    
    





