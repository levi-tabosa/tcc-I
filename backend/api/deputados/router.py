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
                SELECT d.id, d.nome_civil, d.cpf, d.sexo, d.email, d.data_nascimento, 
                       d.escolaridade, d.uf_nascimento, d.municipio_nascimento, 
                       m.sigla_partido
                FROM deputados d
                LEFT JOIN deputados_mandatos m ON d.id = m.deputado_id
                WHERE d.id = %s
                ORDER BY m.id DESC
                LIMIT 1
            """
            cursor.execute(query, (deputado_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise HTTPException(status_code=404, detail=f"Deputado com ID {deputado_id} não encontrado.")

            data_nasc = resultado[5]
            data_nasc_iso = data_nasc.isoformat() if isinstance(data_nasc, date) else None
            
            return {
                 "id": resultado[0], 
                 "nome_civil": resultado[1], 
                 "cpf": resultado[2],
                 "sexo": resultado[3],
                 "email": resultado[4],
                 "data_nascimento": data_nasc_iso, 
                 "escolaridade": resultado[6],
                 "uf_nascimento": resultado[7], 
                 "municipio_nascimento": resultado[8],
                 "sigla_partido": resultado[9], 
                 "foto": f"https://www.camara.leg.br/internet/deputado/bandep/{resultado[0]}.jpg"
            }

    except psycopg2.Error as e:
        logging.error(f"Erro na query de perfil: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar o perfil do deputado.")
    finally:
        if conn: conn.close()
        
        
@router.get("/{deputado_id}/despesas")
def buscar_despesas_deputado(deputado_id: int):
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indisponível: Erro de conexão com o banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    desp.ano, 
                    desp.mes, 
                    desp.tipo_despesa, 
                    desp.valor_documento, 
                    desp.url_documento
                FROM deputados_despesas AS desp
                JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
                ORDER BY desp.ano DESC, desp.mes DESC;
            """
            cursor.execute(query, (deputado_id,))
            despesas = cursor.fetchall()
            
            resultado_formatado = [
                {
                    "ano": d[0],
                    "mes": d[1],
                    "tipo_despesa": d[2],
                    "valor": d[3],
                    "url_documento": d[4]
                }
                for d in despesas
            ]
            
            return {"despesas": resultado_formatado}

    except psycopg2.Error as e:
        logging.error(f"Erro na query de despesas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as despesas do deputado.")
    finally:
        if conn: conn.close()        
        
        
        
