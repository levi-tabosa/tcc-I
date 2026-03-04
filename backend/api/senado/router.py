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


@router.get("/comparar")
def get_comparativo_senadores(id1: int, id2: int, ano: int = None):
  
        conn = db.get_connect_senado()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        if id1 == id2:
            raise HTTPException(status_code=400, detail="Os senadores devem ser diferentes")
        
        try:
            with conn.cursor() as cursor:
                query_perfil = """
   SELECT 
    codigo, 
    nome_parlamentar, 
    nome_completo, 
    sexo,
    sigla_partido, 
    uf, 
    email,
    url_foto,
    data_nascimento
FROM public.parlamentar
WHERE codigo IN (%s, %s);
"""             
                cursor.execute(query_perfil, (id1, id2))
                resultado = cursor.fetchall()

                if not resultado:
                    raise HTTPException(status_code=404, detail="Senador não encontrado")
                
                query_despesas = """
                SELECT 
    cod_senador, 
    tipo_despesa, 
    SUM(valor_reembolsado) as total,
    COUNT(*) as qtd
FROM public.despesa_ceaps
WHERE cod_senador IN (%s, %s)
GROUP BY cod_senador, tipo_despesa;
"""
                cursor.execute(query_despesas, (id1, id2))
                reultados_despesas = cursor.fetchall()

                query_despesas_recentes = """SELECT 
    ano, 
    mes, 
    tipo_despesa, 
    valor_reembolsado, 
    data_despesa
FROM public.despesa_ceaps
WHERE cod_senador = %s
  AND data_despesa >= CURRENT_DATE - INTERVAL '12 months'
ORDER BY data_despesa DESC;
"""
                cursor.execute(query_despesas_recentes, (id1,))
                despesas_recentes_1 = cursor.fetchall()
                cursor.execute(query_despesas_recentes, (id2,))
                despesas_recentes_2 = cursor.fetchall()


                # Fix mapping to ensure correct IDs map to correct keys regardless of SQL return order
                senador_1_data = next((r for r in resultado if r[0] == id1), None)
                senador_2_data = next((r for r in resultado if r[0] == id2), None)
                
                if not senador_1_data or not senador_2_data:
                    raise HTTPException(status_code=404, detail="Um ou ambos os senadores não foram encontrados")

                return{ 
                    "senador1": {
                        "codigo": senador_1_data[0],
                        "nomeParlamentar": senador_1_data[1],
                        "nomeCompleto": senador_1_data[2],
                        "sexo": senador_1_data[3],
                        "siglaPartido": senador_1_data[4],
                        "uf": senador_1_data[5],
                        "email": senador_1_data[6],
                        "urlFoto": senador_1_data[7],
                        "dataNascimento": senador_1_data[8]
                    },
                    "senador2": {
                        "codigo": senador_2_data[0],
                        "nomeParlamentar": senador_2_data[1],
                        "nomeCompleto": senador_2_data[2],
                        "sexo": senador_2_data[3],
                        "siglaPartido": senador_2_data[4],
                        "uf": senador_2_data[5],
                        "email": senador_2_data[6],
                        "urlFoto": senador_2_data[7],
                        "dataNascimento": senador_2_data[8]
                    },
                    "despesas": [           
                        {
                            "senador": r[0],
                            "tipoDespesa": r[1],
                            "total": float(r[2]),
                            "qtd": r[3]
                        }
                        for r in reultados_despesas
                    ],
                    "despesas_recentes_1": [
                        {
                            "ano": r[0],
                            "mes": r[1],
                            "tipoDespesa": r[2],
                            "valor": float(r[3]),
                            "data_despesa": r[4].isoformat() if hasattr(r[4], 'isoformat') else str(r[4])
                        }
                        for r in despesas_recentes_1
                    ],
                    "despesas_recentes_2": [
                        {
                            "ano": r[0],
                            "mes": r[1],
                            "tipoDespesa": r[2],
                            "valor": float(r[3]),
                            "data_despesa": r[4].isoformat() if hasattr(r[4], 'isoformat') else str(r[4])
                        }
                        for r in despesas_recentes_2
                    ]       
                }
        except Exception as e:
            logging.error(f"Erro ao buscar senador: {e}")
            raise HTTPException(status_code=500, detail="Erro ao processar senador")
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


