import logging
from fastapi import APIRouter, HTTPException, Query
import database.db as db

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)

@router.get("/estatisticas")
def estatisticas_empresas():
    """
    Retorna estatísticas gerais sobre empresas que receberam recursos
    """
    conn = db.get_connect()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            # Total de empresas e valor total pago
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT cnpj_cpf_fornecedor) as total_empresas,
                    COALESCE(SUM(valor_documento), 0) as total_pago,
                    COUNT(*) as total_contratos
                FROM deputados_despesas
                WHERE LENGTH(cnpj_cpf_fornecedor) > 11
            """)
            stats = cursor.fetchone()
            
            return {
                "total_empresas": stats[0] or 0,
                "total_pago": float(stats[1]) if stats[1] else 0,
                "total_contratos": stats[2] or 0
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas de empresas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        conn.close()
        
        
@router.get("/ranking")
def ranking_empresas(limit: int = 20):
    conn = db.get_connect()
    if conn is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT SUM(valor_documento) 
                FROM deputados_despesas 
                WHERE LENGTH(cnpj_cpf_fornecedor) > 11
            """
            )
            
            total_geral_empresas = cursor.fetchone()[0] or 1.0
            
            query =  """
            WITH top_fornecedores AS (
                SELECT 
                    cnpj_cpf_fornecedor,
                    MAX(nome_fornecedor) as nome,
                    SUM(valor_documento) as total_valor,
                    COUNT(*) as qtd_contratos
                FROM deputados_despesas
                WHERE LENGTH(cnpj_cpf_fornecedor) > 11
                GROUP BY cnpj_cpf_fornecedor
                ORDER BY total_valor DESC
                LIMIT %s
            ),
            partidos_pagadores AS (
                SELECT 
                    d.cnpj_cpf_fornecedor,
                    m.sigla_partido,
                    SUM(d.valor_documento) as valor
                FROM deputados_despesas d
                JOIN deputados_mandatos m ON d.mandato_id = m.id
                JOIN top_fornecedores tf ON d.cnpj_cpf_fornecedor = tf.cnpj_cpf_fornecedor
                GROUP BY d.cnpj_cpf_fornecedor, m.sigla_partido
            )
            SELECT 
                tf.cnpj_cpf_fornecedor,
                tf.nome,
                tf.total_valor,
                tf.qtd_contratos,
                (
                    SELECT string_agg(sub.sigla_partido, ', ')
                    FROM (
                        SELECT pp.sigla_partido
                        FROM partidos_pagadores pp
                        WHERE pp.cnpj_cpf_fornecedor = tf.cnpj_cpf_fornecedor
                        ORDER BY pp.valor DESC
                        LIMIT 3
                    ) sub
                ) as principais_partidos
            FROM top_fornecedores tf
            ORDER BY tf.total_valor DESC;
            """
            cursor.execute(query, (limit,))
            resultados = cursor.fetchall()
            
            lista_formatada = []
            
            for i, row in enumerate(resultados):
                cnpj = row[0]
                nome_bruto = row[1]
                
                nome_limpo = nome_bruto.split("-")[0].strip().title() if nome_bruto else "Não Informado"
                    
                valor_empresa = float(row[2]) 
                
                percentual =  (valor_empresa /  float(total_geral_empresas)) * 100
                 
                                    
                lista_formatada.append({
                    "rank": i + 1,
                    "cnpj": cnpj,
                    "nome": nome_limpo,
                    "valor_total": float(row[2]),
                    "contratos": int(row[3]),
                    "principais_partidos": row[4] if row[4] else "N/A",
                    "percentual": round(percentual, 2)
                    
                })
            
            return lista_formatada
    except Exception as e:  
        logging.error(f"Erro ao buscar ranking de empresas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar ranking de empresas")
    finally:
        conn.close()
