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
def get_lista_senadores(legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT ON (p.codigo)
                    p.codigo,
                    p.nome_parlamentar,
                    p.nome_completo,
                    p.sexo,
                    p.sigla_partido,
                    p.uf,
                    p.email,
                    p.url_foto,
                    p.url_pagina,
                    p.data_nascimento
                FROM senado.parlamentar p
                INNER JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
            """
            params = []
            if legislatura:
                query += " WHERE m.codigo_legislatura = %s"
                params.append(legislatura)
                
            query += " ORDER BY p.codigo, p.nome_parlamentar ASC"
            cursor.execute(query, tuple(params))
            
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


@router.get("/estatisticas")
def get_estatisticas_senado(legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query_total = "SELECT COUNT(DISTINCT codigo_parlamentar) FROM senado.mandato"
            params = []
            if legislatura:
                query_total += " WHERE codigo_legislatura = %s"
                params.append(legislatura)
            
            cursor.execute(query_total, tuple(params))
            total_senadores = cursor.fetchone()[0]
            total_senadores = cursor.fetchone()[0]

            query_gastos = "SELECT COALESCE(SUM(valor_reembolsado), 0) FROM senado.despesa_ceaps"
            # TODO: If we had a direct link to legislatura in despesa_ceaps or via mandato
            # For now, let's keep it global or filter by year if we assume fixed years for legislatures
            cursor.execute(query_gastos)
            total_gastos = cursor.fetchone()[0] or 0

            # Distribuição por Região
            query_regiao = """
                SELECT 
                    CASE
                        WHEN p.uf IN ('AC','AP','AM','PA','RO','RR','TO') THEN 'Norte'
                        WHEN p.uf IN ('AL','BA','CE','MA','PB','PE','PI','RN','SE') THEN 'Nordeste'
                        WHEN p.uf IN ('DF','GO','MT','MS') THEN 'Centro-Oeste'
                        WHEN p.uf IN ('ES','MG','RJ','SP') THEN 'Sudeste'
                        WHEN p.uf IN ('PR','RS','SC') THEN 'Sul'
                        ELSE 'Outros'
                    END AS regiao,
                    COUNT(DISTINCT p.codigo) AS quantidade
                FROM senado.parlamentar p
                INNER JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
            """
            params_reg = []
            if legislatura:
                query_regiao += " WHERE m.codigo_legislatura = %s"
                params_reg.append(legislatura)
                
            query_regiao += " GROUP BY regiao ORDER BY quantidade DESC"
            cursor.execute(query_regiao, tuple(params_reg))
            regioes = cursor.fetchall()
            
            return {
                "total_senadores": total_senadores,
                "total_gastos": total_gastos,
                "senadores_por_regiao": [
                    {"name": r[0], "value": int(r[1])}
                    for r in regioes
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/comparar")
def get_comparativo_senadores(id1: int, id2: int, ano: int = None, legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        if id1 == id2:
            raise HTTPException(status_code=400, detail="Os senadores devem ser diferentes")

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
FROM senado.parlamentar
WHERE codigo IN (%s, %s);
"""             
            cursor.execute(query_perfil, (id1, id2))
            resultado = cursor.fetchall()

            if not resultado:
                raise HTTPException(status_code=404, detail="Senador não encontrado")
            
            query_despesas = """
SELECT 
    d.cod_senador, 
    d.tipo_despesa, 
    SUM(d.valor_reembolsado) as total,
    COUNT(*) as qtd
FROM senado.despesa_ceaps d
INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
WHERE d.cod_senador IN (%s, %s)
            """
            params_stat = [id1, id2]
            if legislatura:
                # We need to filter despesas by legislature. Since despesa_ceaps has ano/mes, 
                # and mandato has primeira_legislatura/segunda_legislatura, this is tricky.
                # However, the user wants it to work, so we filter by mandato's legislature.
                query_despesas += " AND m.codigo_legislatura = %s"
                params_stat.append(legislatura)
                
            query_despesas += " GROUP BY d.cod_senador, d.tipo_despesa"
            cursor.execute(query_despesas, tuple(params_stat))
            resultados_despesas = cursor.fetchall()

            query_despesas_recentes = """SELECT 
    ano, 
    mes, 
    tipo_despesa, 
    valor_reembolsado, 
    data_despesa
FROM senado.despesa_ceaps
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
                    for r in resultados_despesas
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
def get_perfil_senador(senador_codigo: int, legislatura: int = Query(None)):    
    try:
        conn = db.get_db_connection()
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
FROM senado.parlamentar
WHERE codigo = %s;"""
            cursor.execute(query, (senador_codigo,))
            resultado = cursor.fetchone()

            if not resultado:
                raise HTTPException(status_code=404, detail="Senador não encontrado")
            
            # 2. Buscar Resumo de Emendas
            query_emendas = """
                SELECT SUM(e.valor_pago) as total_emendas
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                WHERE s.codigo = %s
            """
            cursor.execute(query_emendas, (senador_codigo,))
            emendas_res_row = cursor.fetchone()
            total_emendas = float(emendas_res_row[0]) if emendas_res_row and emendas_res_row[0] else 0.0

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
                    "dataNascimento": resultado[9],
                    "total_emendas": total_emendas
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senador")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/{senador_codigo}/despesas", summary="Obtém o extrato de despesas de um senador")
def get_despesas_senador(senador_codigo: int, legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar as 12 despesas mais recentes
            query_recente = """SELECT 
    d.ano, 
    d.mes, 
    d.tipo_despesa, 
    d.fornecedor, 
    d.valor_reembolsado, 
    d.data_despesa
FROM senado.despesa_ceaps d
INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
WHERE d.cod_senador = %s 
"""
            params_rec = [senador_codigo]
            if legislatura:
                query_recente += " AND m.codigo_legislatura = %s"
                params_rec.append(legislatura)
                
            query_recente += " ORDER BY d.data_despesa DESC LIMIT 50"
            cursor.execute(query_recente, tuple(params_rec))
            resultado = cursor.fetchall()

            # 2. Buscar o resumo por categoria (considerando TODA a história)
            query_categorias = """
                SELECT 
                    d.tipo_despesa, 
                    SUM(d.valor_reembolsado) as total
                FROM senado.despesa_ceaps d
                INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
                WHERE d.cod_senador = %s
            """
            params_cat = [senador_codigo]
            if legislatura:
                query_categorias += " AND m.codigo_legislatura = %s"
                params_cat.append(legislatura)
            
            query_categorias += " GROUP BY d.tipo_despesa ORDER BY total DESC"
            cursor.execute(query_categorias, tuple(params_cat))
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

@router.get("/despesas/estatisticas")
def get_despesas_estatisticas(legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
           SELECT COALESCE(SUM(d.valor_reembolsado), 0) AS total_gastos
           FROM senado.despesa_ceaps d
           INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
           WHERE 1=1
"""
            params = []
            if legislatura:
                query += " AND m.codigo_legislatura = %s "
                params.append(legislatura)
            
            cursor.execute(query, tuple(params))
            res_total = cursor.fetchone()
            total_gastos = res_total[0] if res_total else 0

            query = """SELECT 
    COALESCE(SUM(valor_reembolsado) / NULLIF(COUNT(DISTINCT cod_senador), 0), 0) AS media_por_senador
FROM senado.despesa_ceaps;
"""
            cursor.execute(query)
            res_media = cursor.fetchone()
            media_por_senador = res_media[0] if res_media else 0
            
            query = """WITH total_geral AS (
    SELECT COALESCE(SUM(valor_reembolsado), 1) as soma_total 
    FROM senado.despesa_ceaps 
)
SELECT 
    p.sigla_partido,
    SUM(d.valor_reembolsado) AS total_valor,
    ROUND(
        (SUM(d.valor_reembolsado) / (SELECT soma_total FROM total_geral)) * 100, 
        2
    ) AS percentual
FROM senado.despesa_ceaps d
JOIN senado.parlamentar p ON d.cod_senador = p.codigo
GROUP BY p.sigla_partido
ORDER BY total_valor DESC;
"""
            cursor.execute(query)
            partidos = cursor.fetchall()
            
            query = """WITH ranking_categorias AS (
    SELECT 
        tipo_despesa, 
        SUM(valor_reembolsado) AS valor,
        ROW_NUMBER() OVER (ORDER BY SUM(valor_reembolsado) DESC) as rank
    FROM senado.despesa_ceaps
    GROUP BY tipo_despesa
)
SELECT 
    CASE WHEN rank <= 9 THEN tipo_despesa ELSE 'Outros' END AS categoria,
    SUM(valor) AS total_valor
FROM ranking_categorias
GROUP BY 1
ORDER BY (CASE WHEN rank <= 9 THEN tipo_despesa ELSE 'Outros' END = 'Outros'), total_valor DESC;
"""
            # Refined the ORDER BY slightly for Postgres compatibility and used GROUP BY index
            cursor.execute(query.replace("GROUP BY categoria", "GROUP BY 1").replace("(categoria = 'Outros')", "(CASE WHEN rank <= 9 THEN tipo_despesa ELSE 'Outros' END = 'Outros')"))
            categorias = cursor.fetchall()
            
            query = """SELECT 
    p.codigo, 
    p.nome_parlamentar, 
    p.sigla_partido, 
    p.uf, 
    p.url_foto,
    SUM(d.valor_reembolsado) AS total_valor
FROM senado.despesa_ceaps d
JOIN senado.parlamentar p ON d.cod_senador = p.codigo
GROUP BY p.codigo, p.nome_parlamentar, p.sigla_partido, p.uf, p.url_foto
ORDER BY total_valor DESC
LIMIT 10;
"""
            cursor.execute(query)
            top_10 = cursor.fetchall()

            # Evolução Mensal (últimos 12 meses com dados disponíveis)
            query = """SELECT 
    EXTRACT(YEAR FROM data_despesa)::int AS ano,
    EXTRACT(MONTH FROM data_despesa)::int AS mes,
    SUM(valor_reembolsado) AS valor
FROM senado.despesa_ceaps
WHERE data_despesa IS NOT NULL
  AND EXTRACT(YEAR FROM data_despesa) BETWEEN 2000 AND EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY 1, 2
ORDER BY 1 DESC, 2 DESC
LIMIT 12;
"""
            cursor.execute(query)
            gastos_mensais = cursor.fetchall()

            query = """SELECT 
    COALESCE(SUM(valor_reembolsado), 0) AS total_geral
FROM senado.despesa_ceaps;
"""
            cursor.execute(query)
            total_12_meses = cursor.fetchone()[0] or 0
            
            return {
                "total_gastos": float(total_gastos),
                "media_por_senador": float(media_por_senador),
                "total_12_meses": float(total_12_meses),
                "gastos_por_mes": [
                    {"ano": r[0], "mes": r[1], "valor": float(r[2])}
                    for r in gastos_mensais
                ],
                "partidos": [
                    {
                        "partido": r[0],
                        "total": float(r[1]),
                        "percentual": float(r[2])
                    }
                    for r in partidos
                ],
                "categorias": [
                    {
                        "categoria": r[0],
                        "total": float(r[1])
                    }
                    for r in categorias
                ],
                "top_10": [
                    {
                        "codigo": r[0],
                        "nome": r[1],
                        "partido": r[2],
                        "uf": r[3],
                        "foto": r[4],
                        "total": float(r[5])
                    }
                    for r in top_10
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/materia/listar")
def get_materia_listar(
    siglaTipo: str = Query(None),
    ano: int = Query(None),
    ementa: str = Query(None),
    senador: str = Query(None),
    legislatura: int = Query(None),
    pagina: int = 1
):
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina

    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT
                    m.codigo AS id,
                    m.sigla,
                    m.numero,
                    m.ano,
                    m.ementa,
                    m.data,
                    autor.nome_parlamentar AS autor_principal
                FROM senado.materia m
                LEFT JOIN senado.autoria a ON a.codigo_materia = m.codigo AND a.autor_principal = true
                LEFT JOIN senado.parlamentar autor ON a.codigo_parlamentar = autor.codigo
            """
            params = []

            if senador:
                query += """
                    INNER JOIN senado.votacao_parlamentar vp ON m.codigo = vp.codigo_materia
                    INNER JOIN senado.parlamentar p ON vp.codigo_parlamentar = p.codigo
                """

            query += " WHERE 1=1"

            if siglaTipo:
                query += " AND m.sigla = %s"
                params.append(siglaTipo)
            if ano:
                query += " AND m.ano = %s"
                params.append(ano)
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query += " AND m.ano BETWEEN %s AND %s"
                params.extend([start_year, end_year])
            if ementa:
                query += " AND m.ementa ILIKE %s"
                params.append(f"%{ementa}%")
            if senador:
                query += " AND p.nome_parlamentar ILIKE %s"
                params.append(f"%{senador}%")

            query += " ORDER BY m.ano DESC, m.sigla, m.numero LIMIT %s OFFSET %s"
            params.extend([itens_por_pagina, offset])

            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            return {
                "materia": [
                    {
                        "id": r[0],
                        "siglaTipo": r[1],
                        "numero": r[2],
                        "ano": r[3],
                        "ementa": r[4],
                        "dataApresentacao": r[5].isoformat() if hasattr(r[5], 'isoformat') else str(r[5]) if r[5] else None,
                        "autor_principal": r[6]
                    }
                    for r in resultados
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar matéria: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar matéria")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/emendas", summary="Busca uma lista de emendas parlamentares do Senado")
def get_lista_emendas(
    nome_senador: str = Query(None),
    ano: int = Query(None),
    pagina: int = 1
):
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina

    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    s.nome_parlamentar as senador,
                    e.codigo_emenda as codigo,
                    e.ano,
                    e.tipo_emenda as tipo,
                    e.valor_empenhado,
                    e.valor_liquidado,
                    e.valor_pago,
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                WHERE 1=1
            """
            params = []
            if nome_senador:
                query += " AND s.nome_parlamentar ILIKE %s"
                params.append(f"%{nome_senador}%")
            if ano:
                query += " AND e.ano = %s"
                params.append(ano)
                
            query += " ORDER BY e.ano DESC, e.valor_pago DESC LIMIT %s OFFSET %s"
            params.extend([itens_por_pagina, offset])

            cursor.execute(query, tuple(params))
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            for r in resultados:
                r["valorEmpenhado"] = float(r["valor_empenhado"]) if r["valor_empenhado"] else 0.0
                r["valorLiquidado"] = float(r["valor_liquidado"]) if r["valor_liquidado"] else 0.0
                r["valorPago"] = float(r["valor_pago"]) if r["valor_pago"] else 0.0
                del r["valor_empenhado"]
                del r["valor_liquidado"]
                del r["valor_pago"]
                
            return resultados
    except Exception as e:
        logging.error(f"Erro ao buscar emendas do senado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/emendas/resumo", summary="Obtém resumo das emendas do Senado")
def get_resumo_emendas():
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Totais Gerais
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT e.nome_autor) as total_senadores,
                    COUNT(DISTINCT e.localidade_gasto) as total_municipios,
                    COUNT(DISTINCT e.funcao) as total_areas
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
            """)
            totais = cursor.fetchone()
            
            # 2. Distribuição por Área
            cursor.execute("""
                SELECT e.funcao, SUM(e.valor_pago) as valor_total
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                GROUP BY e.funcao
                ORDER BY valor_total DESC
            """)
            areas_raw = cursor.fetchall()
            valor_total_global = sum(float(r[1]) for r in areas_raw) if areas_raw else 1

            areas_formatadas = [
                {
                    "nome": r[0] if r[0] else "Outros",
                    "valor": float(r[1]),
                    "percentual": round((float(r[1]) / valor_total_global) * 100, 1)
                }
                for r in areas_raw
            ]

            # 3. Top 10 Senadores
            cursor.execute("""
                SELECT 
                    s.codigo, s.nome_parlamentar, s.sigla_partido, s.uf, s.url_foto,
                    SUM(e.valor_pago) as total_valor
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                GROUP BY s.codigo, s.nome_parlamentar, s.sigla_partido, s.uf, s.url_foto
                ORDER BY total_valor DESC
                LIMIT 10
            """)
            top_senadores = cursor.fetchall()

            return {
                "totais": {
                    "senadores": totais[0],
                    "municipios": totais[1],
                    "areas": totais[2],
                    "valor_total": valor_total_global
                },
                "areas": areas_formatadas,
                "ranking": [
                    {
                        "id": r[0],
                        "nome": r[1],
                        "partido": r[2] if r[2] else "S/P",
                        "estado": r[3] if r[3] else "BR",
                        "emendasTotal": float(r[5]),
                        "foto": r[4] if r[4] else f"https://ui-avatars.com/api/?name={r[1]}&background=random"
                    }
                    for r in top_senadores
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar resumo emendas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/materia/votacao", summary="Obtém o histórico de votações de um projeto legislativo")
def get_votacao_materia(codigo_materia: int):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    m.sigla || ' ' || m.numero || '/' || m.ano AS materia,
                    m.ementa,
                    p.nome_parlamentar,
                    p.sigla_partido,
                    p.uf,
                    vp.sigla_descricao_voto AS voto,
                    vp.descricao_resultado AS resultado
                FROM senado.votacao_parlamentar vp
                JOIN senado.materia m ON vp.codigo_materia = m.codigo
                JOIN senado.parlamentar p ON vp.codigo_parlamentar = p.codigo
                WHERE vp.codigo_materia = %s
                  AND vp.sigla_descricao_voto NOT IN ('P-NRV', 'AP', 'Presidente (art. 51 RISF)', 'LS', 'NCom')
                ORDER BY m.ano DESC, m.sigla, m.numero, p.nome_parlamentar
            """
            cursor.execute(query, (codigo_materia,))
            resultados = cursor.fetchall()
            return {
                "votacao": [
                    {
                        "materia": r[0],
                        "ementa": r[1],
                        "nomeParlamentar": r[2],
                        "siglaPartido": r[3],
                        "uf": r[4],
                        "voto": r[5],
                        "resultado": r[6]
                    }
                    for r in resultados
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar votação: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar votação")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/materia/votacao", summary="Obtém o histórico de votações de um projeto legislativo")
def get_votacao_materia(codigo_materia: int):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    m.sigla || ' ' || m.numero || '/' || m.ano AS materia,
                    m.ementa,
                    p.nome_parlamentar,
                    p.sigla_partido,
                    p.uf,
                    vp.sigla_descricao_voto AS voto,
                    vp.descricao_resultado AS resultado
                FROM senado.votacao_parlamentar vp
                JOIN senado.materia m ON vp.codigo_materia = m.codigo
                JOIN senado.parlamentar p ON vp.codigo_parlamentar = p.codigo
                WHERE vp.codigo_materia = %s
                  AND vp.sigla_descricao_voto NOT IN ('P-NRV', 'AP', 'Presidente (art. 51 RISF)', 'LS', 'NCom')
                ORDER BY m.ano DESC, m.sigla, m.numero, p.nome_parlamentar
            """
            cursor.execute(query, (codigo_materia,))
            resultados = cursor.fetchall()
            return {
                "votacao": [
                    {
                        "materia": r[0],
                        "ementa": r[1],
                        "nomeParlamentar": r[2],
                        "siglaPartido": r[3],
                        "uf": r[4],
                        "voto": r[5],
                        "resultado": r[6]
                    }
                    for r in resultados
                ]
            }
    
    except Exception as e:
        logging.error(f"Erro ao buscar histórico de votação: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar histórico de votação")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/estatisticas", summary="Obtém estatísticas gerais dos senadores")
def get_estatisticas_gerais():
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """SELECT COUNT(DISTINCT codigo) AS total_senadores
FROM senado.parlamentar;"""
            cursor.execute(query)
            total_senadores = cursor.fetchone()[0]

            query = """SELECT COUNT(DISTINCT
    CASE
        WHEN uf IN ('AC','AP','AM','PA','RO','RR','TO') THEN 'Norte'
        WHEN uf IN ('AL','BA','CE','MA','PB','PE','PI','RN','SE') THEN 'Nordeste'
        WHEN uf IN ('DF','GO','MT','MS') THEN 'Centro-Oeste'
        WHEN uf IN ('ES','MG','RJ','SP') THEN 'Sudeste'
        WHEN uf IN ('PR','RS','SC') THEN 'Sul'
    END
) AS total_regioes
FROM senado.parlamentar
WHERE uf IS NOT NULL; """
            cursor.execute(query)
            total_regioes = cursor.fetchone()[0]

            query = """SELECT COUNT(DISTINCT sigla_partido) AS total_partidos
FROM senado.parlamentar
WHERE sigla_partido IS NOT NULL;"""
            cursor.execute(query)
            total_partidos = cursor.fetchone()[0]
            
            query = """SELECT COUNT(DISTINCT uf) AS total_estados
FROM senado.parlamentar
WHERE uf IS NOT NULL;"""
            cursor.execute(query)
            total_estados = cursor.fetchone()[0]

            query = """SELECT ano, mes, SUM(valor_reembolsado) AS valor
FROM senado.despesa_ceaps
WHERE data_despesa >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY ano, mes
ORDER BY ano DESC, mes DESC;"""
            cursor.execute(query)
            despesas = cursor.fetchall()

            query = """SELECT sigla_partido, COUNT(DISTINCT codigo) AS total_senadores
FROM senado.parlamentar
WHERE sigla_partido IS NOT NULL
GROUP BY sigla_partido
ORDER BY total_senadores DESC
LIMIT 6;"""
            cursor.execute(query)
            partidos = cursor.fetchall()

            query = """SELECT 
    CASE
        WHEN uf IN ('AC','AP','AM','PA','RO','RR','TO') THEN 'Norte'
        WHEN uf IN ('AL','BA','CE','MA','PB','PE','PI','RN','SE') THEN 'Nordeste'
        WHEN uf IN ('DF','GO','MT','MS') THEN 'Centro-Oeste'
        WHEN uf IN ('ES','MG','RJ','SP') THEN 'Sudeste'
        WHEN uf IN ('PR','RS','SC') THEN 'Sul'
        ELSE 'Outros'
    END AS regiao,
    COUNT(DISTINCT codigo) AS quantidade
FROM senado.parlamentar
WHERE uf IS NOT NULL
GROUP BY regiao
ORDER BY quantidade DESC;"""
            cursor.execute(query)
            regioes = cursor.fetchall()
            
            return {
                "total_senadores": total_senadores,
                "total_regioes": total_regioes,
                "total_partidos": total_partidos,
                "total_estados": total_estados,
                "despesas_12_meses":[
                    {
                        "ano": r[0],
                        "mes": r[1],
                        "valor": float(r[2])
                    }
                    for r in despesas
                ],
                "partidos":[
                    {
                        "sigla": r[0],
                        "total_senadores": r[1]
                    }
                    for r in partidos
                ]
                ,
                "regioes":[
                    {
                        "regiao": r[0],
                        "quantidade": r[1]
                    }
                    for r in regioes
                ]
            
            }
            
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas gerais: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas gerais")

@router.get("/{senador_codigo}/emendas/lista", summary="Obtém a lista de emendas parlamentares de um senador")
def get_emendas_lista_senador(senador_codigo: int):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    e.codigo_emenda as codigo,
                    e.ano,
                    e.tipo_emenda as tipo,
                    e.valor_empenhado,
                    e.valor_liquidado,
                    e.valor_pago,
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                WHERE s.codigo = %s
                ORDER BY e.ano DESC, e.valor_pago DESC
            """
            cursor.execute(query, (senador_codigo,))
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            for r in resultados:
                r["valorEmpenhado"] = float(r["valor_empenhado"]) if r["valor_empenhado"] else 0.0
                r["valorLiquidado"] = float(r["valor_liquidado"]) if r["valor_liquidado"] else 0.0
                r["valorPago"] = float(r["valor_pago"]) if r["valor_pago"] else 0.0
                del r["valor_empenhado"]
                del r["valor_liquidado"]
                del r["valor_pago"]
                
            return resultados
    except Exception as e:
        logging.error(f"Erro ao buscar emendas do senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@router.get("/empresas/estatisticas", summary="Obtém estatísticas gerais das empresas")
def get_estatisticas_empresas():
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
               SELECT
                    COUNT(DISTINCT cpf_cnpj) as total_empresas,
                    SUM(valor_reembolsado) as total_pago,
                    COUNT(*) as total_contratos
                FROM senado.despesa_ceaps;
            """
            cursor.execute(query)
            resultados_gerais = cursor.fetchall()

            query = """
                SELECT
                    fornecedor as empresa,
                    SUM(valor_reembolsado) as valor_total
                FROM senado.despesa_ceaps
                GROUP BY fornecedor
                ORDER BY valor_total DESC
                LIMIT 10;
            """
            cursor.execute(query)
            resultados_top_10 = cursor.fetchall()
            
            query = """WITH EmpresaStats AS (
    -- Agrupa os gastos por fornecedor e CNPJ
    SELECT
        fornecedor,
        cpf_cnpj,
        SUM(valor_reembolsado) as valor_total,
        COUNT(*) as contratos
    FROM senado.despesa_ceaps
    GROUP BY fornecedor, cpf_cnpj
),
TotalGeral AS (
    -- Calcula o total de tudo para fazer a porcentagem
    SELECT SUM(valor_reembolsado) as soma_total FROM senado.despesa_ceaps
),
EmpresaPartidos AS (
    -- Identifica quais partidos de senadores pagaram para cada empresa
    SELECT
        d.fornecedor,
        d.cpf_cnpj,
        STRING_AGG(DISTINCT p.sigla_partido, ', ') as partidos
    FROM senado.despesa_ceaps d
    LEFT JOIN senado.parlamentar p ON d.cod_senador = p.codigo
    GROUP BY d.fornecedor, d.cpf_cnpj
)
SELECT
    ROW_NUMBER() OVER (ORDER BY es.valor_total DESC) as rank,
    es.fornecedor as empresa,
    COALESCE(ep.partidos, 'N/A') as partidos,
    es.cpf_cnpj as cnpj,
    es.valor_total,
    es.contratos,
    ROUND((es.valor_total / tg.soma_total) * 100, 2) as percentual
FROM EmpresaStats es
JOIN EmpresaPartidos ep ON es.fornecedor = ep.fornecedor AND es.cpf_cnpj = ep.cpf_cnpj
CROSS JOIN TotalGeral tg
ORDER BY es.valor_total DESC
LIMIT 20;
            """
            cursor.execute(query)
            resultados_top_20 = cursor.fetchall()
            
            return {
                "total_empresas": resultados_gerais[0][0],
                "total_pago": resultados_gerais[0][1],
                "total_contratos": resultados_gerais[0][2],
                "top_10_empresas": [
                    {
                        "empresa": r[0],
                        "valor_total": r[1]
                    }
                    for r in resultados_top_10
                ],
                "top_20_empresas": [
                    {
                        "rank": r[0],
                        "empresa": r[1],
                        "partidos": r[2],
                        "cnpj": r[3],
                        "valor_total": r[4],
                        "contratos": r[5],
                        "percentual": r[6]
                    }
                    for r in resultados_top_20
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas gerais: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas gerais")