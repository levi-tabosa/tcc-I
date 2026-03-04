from fastapi import APIRouter, HTTPException, Query
from datetime import date
import psycopg2
import logging

# Garanta que este import está correto para sua estrutura
import database.db as db

router = APIRouter(
    prefix="/senado",
    tags=["Senado"]
)

@router.get("/lista", summary="Lista todos os senadores ativos")
def get_lista_senadores():
    try:
        conn = db.get_connect_senado()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            cursor.execute("""SELECT 
    codigo,
    nome_parlamentar,
    nome_completo,
    sexo,
    sigla_partido,
    uf,
    email,
    url_foto,
    url_pagina,
    data_nascimento
FROM public.parlamentar
ORDER BY nome_parlamentar ASC;""")
            
            resultados = cursor.fetchall()
            
            return {
                "senadores": [
                {
                    "codigo": r[0],
                    "nomeParlamentar": r[1],
                    "nomeCompleto": r[2],
                    "sexo": r[3],
                    "siglaPartido": r[4],
                    "uf": r[5],
                    "email": r[6],
                    "urlFoto": r[7],
                    "urlPagina": r[8],
                    "dataNascimento": r[9]
                }
                for r in resultados
            ]
        }
    except Exception as e:
        logging.error(f"Erro ao buscar senadores: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senadores")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/{senador_codigo}", summary="Obtém o perfil detalhado de um senador")
def get_perfil_senador(senador_codigo: int):
    try:
        conn = db.get_connect_senado()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """SELECT 
    codigo,
    nome_parlamentar,
    nome_completo,
    sexo,
    sigla_partido,
    uf,
    email,
    url_foto,
    url_pagina,
    data_nascimento
FROM public.parlamentar
WHERE codigo = %s;"""
            cursor.execute(query, (senador_codigo,))
            resultado = cursor.fetchone()

            if not resultado:
                raise HTTPException(status_code=404, detail="Senador não encontrado")
            
            return {
                "senador": {
                    "codigo": resultado[0],
                    "nomeParlamentar": resultado[1],
                    "nomeCompleto": resultado[2],
                    "sexo": resultado[3],
                    "siglaPartido": resultado[4],
                    "uf": resultado[5],
                    "email": resultado[6],
                    "urlFoto": resultado[7],
                    "urlPagina": resultado[8],
                    "dataNascimento": resultado[9]
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senador")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/{senador_codigo}/despesas", summary="Obtém o extrato de despesas de um senador")
def get_despesas_senador(senador_codigo: int):
    try:
        conn = db.get_connect_senado()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar as 12 despesas mais recentes
            query_recente = """SELECT 
    ano, 
    mes, 
    tipo_despesa, 
    fornecedor, 
    valor_reembolsado, 
    data_despesa
FROM public.despesa_ceaps
WHERE cod_senador = %s  
  AND data_despesa >= CURRENT_DATE - INTERVAL '12 months'
ORDER BY data_despesa DESC; """
            cursor.execute(query_recente, (senador_codigo,))
            resultado = cursor.fetchall()

            # 2. Buscar o resumo por categoria (considerando TODA a história)
            query_categorias = """
                SELECT 
                    tipo_despesa, 
                    SUM(valor_reembolsado) as total
                FROM public.despesa_ceaps
                WHERE cod_senador = %s
                GROUP BY tipo_despesa
                ORDER BY total DESC;
            """
            cursor.execute(query_categorias, (senador_codigo,))
            categorias_raw = cursor.fetchall()
            
            total_geral = sum(float(c[1]) for c in categorias_raw) if categorias_raw else 0.0
            
            return {
                "despesas": [
                    {
                        "ano": r[0],
                        "mes": r[1],
                        "tipoDespesa": r[2],
                        "fornecedor": r[3],
                        "valorReembolsado": float(r[4]),
                        "dataDespesa": r[5].isoformat() if hasattr(r[5], 'isoformat') else str(r[5]) if r[5] else None
                    }
                    for r in resultado
                ],
                "total_despesas": total_geral,
                "categorias": [
                    {"categoria": c[0], "valor": float(c[1])}
                    for c in categorias_raw
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senador")
    finally:
        if 'conn' in locals() and conn:
            conn.close()



