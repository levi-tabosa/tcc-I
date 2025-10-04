import psycopg2

def get_connect():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5435,
            database="postgres",
            user="postgres",
            password=""
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None
    

