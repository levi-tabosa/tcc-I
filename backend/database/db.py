from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def get_db_connection():
    try:
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            conn = psycopg2.connect(db_url)
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "fiscaliza_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres")
            )
            
        print("Conectado ao PostgreSQL com sucesso!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None