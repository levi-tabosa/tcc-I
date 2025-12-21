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
        

@router.get("/estatisticas/geral")
def buscar_estatisticas_geral():    
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indisponível: Erro de conexão com o banco de dados.")

    try:
        with conn.cursor() as cursor:
            # 1. Gastos por Categoria (Global)
            cursor.execute(
                """
                SELECT 
                    desp.tipo_despesa,
                    SUM(desp.valor_documento) AS total
                FROM deputados_despesas AS desp
                GROUP BY desp.tipo_despesa
                ORDER BY total DESC;
                """
            )
            gastos_categoria = [{"categoria": r[0], "valor": float(r[1])} for r in cursor.fetchall()]

            # 2. Evolução Mensal (Global - Últimos 12 meses)
            cursor.execute(
                """
                SELECT ano, mes, SUM(valor_documento) as total
                FROM deputados_despesas
                GROUP BY ano, mes
                ORDER BY ano DESC, mes DESC
                LIMIT 12;
                """
            )

            gastos_mensais = [{"ano": r[0], "mes": r[1], "valor": float(r[2])} for r in cursor.fetchall()]
            
            # 3. Gastos por Estado (Precisa de JOIN com a tabela de deputados)
            cursor.execute("""
                SELECT d.uf_nascimento, SUM(desp.valor_documento) as total
                FROM deputados d
                JOIN deputados_mandatos m ON d.id = m.deputado_id
                JOIN deputados_despesas desp ON m.id = desp.mandato_id
                WHERE d.uf_nascimento IS NOT NULL
                GROUP BY d.uf_nascimento
                ORDER BY total DESC
                LIMIT 10;
            """)
            gastos_estado = [{"estado": r[0], "valor": float(r[1])} for r in cursor.fetchall()]

            cursor.execute("SELECT SUM(valor_documento) from deputados_despesas")
            total_geral = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) from deputados")
            total_deputados = cursor.fetchone()[0] or 0

            return{
                "total_gastos": float(total_geral),
                "total_parlamentares": total_deputados,
                "gastos_por_categoria": gastos_categoria,
                "gastos_por_mes": gastos_mensais,
                "gastos_por_estado": gastos_estado
            }
         
    except psycopg2.Error as e:
        logging.error(f"Erro na query de estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as estatísticas.")
    finally:
        conn.close()
    
