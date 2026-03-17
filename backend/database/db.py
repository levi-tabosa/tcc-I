from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def get_connect_camara():
    try:
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            conn = psycopg2.connect(db_url, options="-c search_path=camara")
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "fiscaliza_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
                options="-c search_path=camara"
            )
            
        print("Conectado ao PostgreSQL com sucesso (Schema: camara)!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None

def get_connect_senado():
    try:
        db_url = os.getenv("DATABASE_URL")

        if db_url:
            conn = psycopg2.connect(db_url, options="-c search_path=senado")
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "fiscaliza_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
                options="-c search_path=senado"
            )
        print("Conectado ao PostgreSQL com sucesso (Schema: senado)!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None