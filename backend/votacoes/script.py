import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database.db as db

def get_votacoes_votos():
    conn = db.get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, votacao_id,  deputado_id, tipo_voto FROM votacoes_votos")
    votacoes  = cursor.fetchall()
    cursor.close()
    conn.close()
    return votacoes

def get_deputado_votos():
    conn = db.get_connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            v.deputado_id,
            d.nome_civil AS nome_deputado,
            v.tipo_voto
        FROM
            votacoes_votos v
        JOIN
            deputados d ON v.deputado_id = d.id
    """)
    deputados = cursor.fetchall()
    cursor.close()
    conn.close()
    return deputados


    
if __name__ == "__main__":

    
    deputados = get_votacoes_votos()
    for deputado in deputados:
        id, votacao_id, deputado_id, tipo_voto = deputado
        print(f"ID: {id}, Votação ID: {votacao_id}, Deputado ID: {deputado_id}, Tipo de Voto: {tipo_voto}")
        print()
        
    print("----- Votos dos Deputados -----")
    deputado_votos = get_deputado_votos()
    for voto in deputado_votos:
        deputado_id, nome_deputado, tipo_voto = voto
        print(f"Deputado ID: {deputado_id}, Nome: {nome_deputado}, Tipo de Voto: {tipo_voto}")
        print()