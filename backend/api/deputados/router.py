from fastapi import APIRouter, HTTPException, Query
from datetime import date
import psycopg2
import logging

# Garanta que este import está correto para sua estrutura
import database.db as db

router = APIRouter(
    prefix="/deputados",
    tags=["Deputados"]
)

@router.get("/buscar")
def buscar_deputados(nome: str = Query(..., min_length=2)):
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indisponível: Erro de conexão com o banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            termo_busca = f"{nome}%"
            query = "SELECT id, nome_civil, uf_nascimento FROM deputados WHERE nome_civil ILIKE %s"
            
            cursor.execute(query, (termo_busca,))
            
            resultados = cursor.fetchall()
            
            # A API retorna os dados no formato que o frontend espera: {"resultados": [...]}
            return {"resultados": [{"id": res[0], "nome_civil": res[1], "uf": res[2]} for res in resultados]}

    except psycopg2.Error as e:
        logging.error(f"Erro na query de busca: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a busca.")
    finally:
        if conn: conn.close()

@router.get("/{deputado_id}")
def buscar_perfil_por_id(deputado_id: int):
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indisponível: Erro de conexão com o banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id, nome_civil, email, data_nascimento, escolaridade,
                       uf_nascimento, municipio_nascimento 
                FROM deputados WHERE id = %s
            """
            cursor.execute(query, (deputado_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise HTTPException(status_code=404, detail=f"Deputado com ID {deputado_id} não encontrado.")

            data_nasc = resultado[3]
            data_nasc_iso = data_nasc.isoformat() if isinstance(data_nasc, date) else None
            
            return {
                 "id": resultado[0], "nome_civil": resultado[1], "email": resultado[2],
                 "data_nascimento": data_nasc_iso, "escolaridade": resultado[4],
                 "uf_nascimento": resultado[5], "municipio_nascimento": resultado[6]
            }

    except psycopg2.Error as e:
        logging.error(f"Erro na query de perfil: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar o perfil do deputado.")
    finally:
        if conn: conn.close()