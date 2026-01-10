from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def get_connect():
    try:
        # Tenta pegar a URL completa primeiro (que está no seu Docker)
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            # Se tiver a URL, conecta direto com ela
            conn = psycopg2.connect(db_url)
        else:
            # Se não tiver URL, tenta pegar as variáveis individuais (bom para rodar local sem docker)
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            
        print("Conectado ao PostgreSQL com sucesso!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None