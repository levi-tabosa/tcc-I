import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database.db as db

def get_deputados():
    conn = db.get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_civil, cpf, sexo, data_nascimento, data_falecimento, uf_nascimento, municipio_nascimento, escolaridade, email FROM deputados")
    deputados = cursor.fetchall()
    cursor.close()
    conn.close()
    return deputados

if __name__ == "__main__":
    deputados = get_deputados()
    for deputado in deputados:
        id, nome_civil, cpf, sexo, data_nascimento, data_falecimento, uf_nascimento, municipio_nascimento, escolaridade, email = deputado
        print(f"ID: {id}, Nome: {nome_civil}, CPF: {cpf}, Sexo: {sexo}, Data de Nascimento: {data_nascimento}, Data de Falecimento: {data_falecimento if data_falecimento else 'N/A'}, UF de Nascimento: {uf_nascimento}, Município de Nascimento: {municipio_nascimento}, Escolaridade: {escolaridade}, Email: {email if email else 'N/A'}")
        print()


    