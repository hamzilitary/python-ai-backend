import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="agent_db",
        user="postgres",
        password="postgres" 
        )
    