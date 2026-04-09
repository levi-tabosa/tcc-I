from fastapi import APIRouter, HTTPException, Query
from datetime import date
import psycopg2
import logging
from functools import lru_cache

# Garanta que este import está correto para sua estrutura
import database.db as db

router = APIRouter(
    prefix="/senado",
    tags=["Senado"]
)

@router.get("/legislaturas", summary="Lista todas as legislaturas disponíveis na base")
@lru_cache(maxsize=1)
def get_legislaturas_senado():
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT primeira_legislatura, segunda_legislatura 
                FROM senado.mandato
            """
            cursor.execute(query)
            mandatos = cursor.fetchall()
            legis_set = set()
            for m in mandatos:
                if m[0] and str(m[0]).strip().isdigit() and int(str(m[0]).strip()) <= 57:
                    legis_set.add(int(str(m[0]).strip()))
                if m[1] and str(m[1]).strip().isdigit() and int(str(m[1]).strip()) <= 57:
                    legis_set.add(int(str(m[1]).strip()))
            
            return sorted(list(legis_set), reverse=True)
    except Exception as e:
        logging.error(f"Erro ao buscar legislaturas ativas senado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar legislaturas")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/{legislatura}/lista", summary="Lista todos os senadores ativos")
def get_lista_senadores(legislatura: int):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT ON (p.codigo)
                    p.codigo,
                    p.nome_parlamentar,
                    p.sigla_partido,
                    p.uf,
                    p.url_foto
                FROM senado.parlamentar p
                INNER JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
            """
            params = []
            if legislatura:
                query += " WHERE m.primeira_legislatura = %s OR m.segunda_legislatura = %s"
                params.extend([str(legislatura), str(legislatura)])
                
            query += " ORDER BY p.codigo, p.nome_parlamentar ASC"
            cursor.execute(query, tuple(params))
            
            resultados = cursor.fetchall()
            
            return {
                "senadores": [
                {
                    "codigo": r[0],
                    "nomeParlamentar": r[1],
                    "siglaPartido": r[2],
                    "uf": r[3],
                    "urlFoto": r[4]
                }
                for r in resultados
            ]
        }
    except Exception as e:
        logging.error(f"Erro ao buscar senadores: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senadores")
    finally:
        if conn:
            db.release_db_connection(conn)





@router.get("/{legislatura}/estatisticas")
@lru_cache(maxsize=16)
def get_estatisticas_senado(legislatura: int):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query_total = "SELECT COUNT(DISTINCT codigo_parlamentar) FROM senado.mandato"
            params = []
            if legislatura:
                query_total += " WHERE primeira_legislatura = %s OR segunda_legislatura = %s"
                params.extend([str(legislatura), str(legislatura)])
            
            cursor.execute(query_total, tuple(params))
            row = cursor.fetchone()
            total_senadores = row[0] if row else 0

            query_gastos = """
                SELECT COALESCE(SUM(d.valor_reembolsado), 0) 
                FROM senado.despesa_ceaps d
                INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
                WHERE 1=1
            """
            params_gastos = []
            if legislatura:
                query_gastos += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_gastos.extend([str(legislatura), str(legislatura)])
            
            cursor.execute(query_gastos, tuple(params_gastos))
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
                WHERE 1=1
            """
            params_reg = []
            if legislatura:
                query_regiao += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_reg.extend([str(legislatura), str(legislatura)])
                
            query_regiao += " GROUP BY regiao ORDER BY quantidade DESC"
            cursor.execute(query_regiao, tuple(params_reg))
            regioes = cursor.fetchall()
            
            return {
                "total_senadores": total_senadores,
                "total_gastos": total_gastos,
                "total_regioes": len(regioes),
                "senadores_por_regiao": [
                    {"name": r[0], "value": int(r[1])}
                    for r in regioes
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/comparar")
def get_comparativo_senadores(legislatura: int, id1: int, id2: int):
    conn = None
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
                query_despesas += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_stat.extend([str(legislatura), str(legislatura)])
                
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
        if conn:
            db.release_db_connection(conn)
                

@router.get("/{legislatura}/{senador_codigo}", summary="Obtém o perfil detalhado de um senador")
def get_perfil_senador(legislatura: int, senador_codigo: int):    
    conn = None
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
            
            # 2. Buscar Resumo de Emendas (Optimized with CTE)
            query_emendas = """
                WITH senadores_nomes AS (
                    SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                    UNION
                    SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                )
                SELECT SUM(e.valor_pago) as total_emendas
                FROM portal.emendas e
                JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                WHERE s.id = %s
            """
            cursor.execute(query_emendas, (senador_codigo,))
            emendas_res_row = cursor.fetchone()
            total_emendas = float(emendas_res_row[0]) if emendas_res_row and emendas_res_row[0] else 0.0

            # 3. Legislaturas Ativas
            query_legis = """
                SELECT primeira_legislatura, segunda_legislatura
                FROM senado.mandato
                WHERE codigo_parlamentar = %s
            """
            cursor.execute(query_legis, (senador_codigo,))
            mandatos = cursor.fetchall()
            legis_set = set()
            for m in mandatos:
                if m[0] and str(m[0]).strip().isdigit() and int(str(m[0]).strip()) <= 57:
                    legis_set.add(int(str(m[0]).strip()))
                if m[1] and str(m[1]).strip().isdigit() and int(str(m[1]).strip()) <= 57:
                    legis_set.add(int(str(m[1]).strip()))
            legislaturas_ativas = sorted(list(legis_set), reverse=True)

            # Determinar Legislatura Exibida (Sempre forçamos uma real)
            if legislatura and legislatura in legislaturas_ativas:
                leg_exibida = legislatura
            elif legislaturas_ativas:
                leg_exibida = legislaturas_ativas[0]
            else:
                leg_exibida = 57

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
                    "total_emendas": total_emendas,
                    "legislaturas_ativas": legislaturas_ativas,
                    "legislatura_exibida": leg_exibida
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senador")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/{senador_codigo}/despesas", summary="Obtém o extrato de despesas de um senador")
def get_despesas_senador(legislatura: int, senador_codigo: int, pagina: int = 1):
    itens_per_page = 20
    offset = (pagina - 1) * itens_per_page
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar o total de despesas para paginação
            query_count = """SELECT COUNT(*) 
                FROM senado.despesa_ceaps d
                WHERE d.cod_senador = %s"""
            params_count = [senador_codigo]
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query_count += " AND CAST(d.ano AS INTEGER) BETWEEN %s AND %s"
                params_count.extend([start_year, end_year])
            
            cursor.execute(query_count, tuple(params_count))
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + itens_per_page - 1) // itens_per_page

            # 2. Buscar as despesas paginadas
            query_recente = """SELECT 
                    d.ano, 
                    d.mes, 
                    d.tipo_despesa, 
                    d.fornecedor, 
                    d.valor_reembolsado, 
                    d.data_despesa
                FROM senado.despesa_ceaps d
                WHERE d.cod_senador = %s 
            """
            params_rec = [senador_codigo]
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query_recente += " AND CAST(d.ano AS INTEGER) BETWEEN %s AND %s"
                params_rec.extend([start_year, end_year])
                
            query_recente += " ORDER BY d.data_despesa DESC LIMIT %s OFFSET %s"
            params_rec.extend([itens_per_page, offset])
            cursor.execute(query_recente, tuple(params_rec))
            resultado = cursor.fetchall()

            # 3. Buscar o resumo por categoria
            query_categorias = """
                SELECT 
                    d.tipo_despesa, 
                    SUM(d.valor_reembolsado) as total
                FROM senado.despesa_ceaps d
                WHERE d.cod_senador = %s
            """
            params_cat = [senador_codigo]
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query_categorias += " AND CAST(d.ano AS INTEGER) BETWEEN %s AND %s"
                params_cat.extend([start_year, end_year])
            
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
                ],
                "paginacao": {
                    "total": total_items,
                    "pagina": pagina,
                    "total_paginas": total_paginas,
                    "itens_por_pagina": itens_per_page
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar despesas do senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar despesas")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/{legislatura}/despesas/estatisticas")
@lru_cache(maxsize=16)
def get_despesas_estatisticas(legislatura: int):
    conn = None
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
            where_leg = ""
            join_mandato = ""
            if legislatura:
                where_leg = " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                join_mandato = " INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar"
                params.extend([str(legislatura), str(legislatura)])
            
            # 1. Total de Gastos
            query_total = f"SELECT COALESCE(SUM(d.valor_reembolsado), 0) FROM senado.despesa_ceaps d {join_mandato} WHERE 1=1 {where_leg}"
            cursor.execute(query_total, tuple(params))
            total_gastos = cursor.fetchone()[0] or 0

            # 2. Média por Senador
            query_media = f"""
                SELECT COALESCE(SUM(d.valor_reembolsado) / NULLIF(COUNT(DISTINCT d.cod_senador), 0), 0)
                FROM senado.despesa_ceaps d
                {join_mandato}
                WHERE 1=1 {where_leg}
            """
            cursor.execute(query_media, tuple(params))
            media_por_senador = cursor.fetchone()[0] or 0
            
            # 3. Gastos por Partido
            query_partidos = f"""
                SELECT 
                    p.sigla_partido,
                    SUM(d.valor_reembolsado) AS total_valor,
                    ROUND((SUM(d.valor_reembolsado) / NULLIF({total_gastos}, 0)) * 100, 2) AS percentual
                FROM senado.despesa_ceaps d
                JOIN senado.parlamentar p ON d.cod_senador = p.codigo
                {join_mandato}
                WHERE 1=1 {where_leg}
                GROUP BY p.sigla_partido
                ORDER BY total_valor DESC
            """
            cursor.execute(query_partidos, tuple(params))
            partidos = cursor.fetchall()
            
            # 4. Gastos por Categoria
            query_cat = f"""
                WITH ranking_categorias AS (
                    SELECT 
                        d.tipo_despesa, 
                        SUM(d.valor_reembolsado) AS valor,
                        ROW_NUMBER() OVER (ORDER BY SUM(d.valor_reembolsado) DESC) as rank
                    FROM senado.despesa_ceaps d
                    {join_mandato}
                    WHERE 1=1 {where_leg}
                    GROUP BY d.tipo_despesa
                )
                SELECT 
                    CASE WHEN rank <= 9 THEN tipo_despesa ELSE 'Outros' END AS categoria,
                    SUM(valor) AS total_valor
                FROM ranking_categorias
                GROUP BY 1
                ORDER BY total_valor DESC
            """
            cursor.execute(query_cat, tuple(params))
            categorias = cursor.fetchall()
            
            # 5. Top 10 Senadores
            query_top = f"""
                SELECT 
                    p.codigo, 
                    p.nome_parlamentar, 
                    p.sigla_partido, 
                    p.uf, 
                    p.url_foto,
                    SUM(d.valor_reembolsado) AS total_valor
                FROM senado.despesa_ceaps d
                JOIN senado.parlamentar p ON d.cod_senador = p.codigo
                {join_mandato}
                WHERE 1=1 {where_leg}
                GROUP BY p.codigo, p.nome_parlamentar, p.sigla_partido, p.uf, p.url_foto
                ORDER BY total_valor DESC
                LIMIT 10
            """
            cursor.execute(query_top, tuple(params))
            top_10 = cursor.fetchall()

            # 6. Evolução Mensal (últimos 12 meses registrados na legislatura ou total)
            query_evolucao = f"""
                SELECT 
                    EXTRACT(YEAR FROM d.data_despesa)::int AS ano,
                    EXTRACT(MONTH FROM d.data_despesa)::int AS mes,
                    SUM(d.valor_reembolsado) AS valor
                FROM senado.despesa_ceaps d
                {join_mandato}
                WHERE d.data_despesa IS NOT NULL {where_leg}
                GROUP BY 1, 2
                ORDER BY 1 DESC, 2 DESC
                LIMIT 12
            """
            cursor.execute(query_evolucao, tuple(params))
            gastos_mensais = cursor.fetchall()

            # 7. Total 12 meses (sempre global ou por legislatura?) 
            # Mantendo global para contexto, ou filtrando se legislatura ativa 
            query_12m = f"""
                SELECT COALESCE(SUM(d.valor_reembolsado), 0)
                FROM senado.despesa_ceaps d
                {join_mandato}
                WHERE d.data_despesa >= (CURRENT_DATE - INTERVAL '1 year') {where_leg}
            """
            cursor.execute(query_12m, tuple(params))
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
        logging.error(f"Erro ao buscar estatísticas de despesas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/materia/listar")
def get_materia_listar(
    legislatura: int,
    siglaTipo: str = Query(None),
    ano: int = Query(None),
    ementa: str = Query(None),
    senador: str = Query(None),
    pagina: int = 1
):
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina
    conn = None
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
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/emendas", summary="Busca uma lista de emendas parlamentares do Senado")
def get_lista_emendas(
    legislatura: int,
    nome_senador: str = Query(None),
    ano: int = Query(None),
    pagina: int = 1
):
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Total para paginação
            query_count = """
                WITH senadores_nomes AS (
                    SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                    UNION
                    SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                )
                SELECT COUNT(*)
                FROM portal.emendas e
                JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
            """
            
            # Adicionar filtro de legislatura se especificado
            where_conditions = []
            params_count = []
            
            if legislatura:
                query_count += """
                    JOIN senado.mandato m ON s.id = m.codigo_parlamentar
                """
                where_conditions.append("(m.primeira_legislatura = %s OR m.segunda_legislatura = %s)")
                params_count.extend([str(legislatura), str(legislatura)])
            
            if nome_senador:
                where_conditions.append("""s.id IN (
                    SELECT codigo FROM senado.parlamentar 
                    WHERE nome_completo ILIKE %s OR nome_parlamentar ILIKE %s
                )""")
                params_count.extend([f"%{nome_senador}%", f"%{nome_senador}%"])
            
            if ano:
                where_conditions.append("e.ano = %s")
                params_count.append(ano)
            
            if where_conditions:
                query_count += " WHERE " + " AND ".join(where_conditions)
            
            cursor.execute(query_count, tuple(params_count))
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + itens_por_pagina - 1) // itens_por_pagina

            # 2. Dados paginados
            query = """
                WITH senadores_nomes AS (
                    SELECT codigo as id, lower(nome_parlamentar) as nome, nome_parlamentar as nome_senador FROM senado.parlamentar
                    UNION
                    SELECT codigo as id, lower(nome_completo) as nome, nome_parlamentar as nome_senador FROM senado.parlamentar
                )
                SELECT 
                    s.nome_senador as senador,
                    e.codigo_emenda as codigo,
                    e.ano,
                    e.tipo_emenda as tipo,
                    e.valor_pago,
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
            """
            
            # Adicionar JOIN e filtros
            where_conditions_data = []
            params = []
            
            if legislatura:
                query += """
                    JOIN senado.mandato m ON s.id = m.codigo_parlamentar
                """
                where_conditions_data.append("(m.primeira_legislatura = %s OR m.segunda_legislatura = %s)")
                params.extend([str(legislatura), str(legislatura)])
            
            if nome_senador:
                where_conditions_data.append("s.nome_senador ILIKE %s")
                params.append(f"%{nome_senador}%")
            
            if ano:
                where_conditions_data.append("e.ano = %s")
                params.append(ano)
            
            if where_conditions_data:
                query += " WHERE " + " AND ".join(where_conditions_data)
                
            query += " ORDER BY e.ano DESC, e.valor_pago DESC LIMIT %s OFFSET %s"
            params.extend([itens_por_pagina, offset])

            cursor.execute(query, tuple(params))
            res = cursor.fetchall()

            return {
                "emendas": [
                    {
                        "senador": r[0],
                        "codigo": r[1],
                        "ano": r[2],
                        "tipo": r[3],
                        "valorPago": float(r[4]),
                        "funcao": r[5],
                        "localidade": r[6]
                    }
                    for r in res
                ],
                "paginacao": {
                    "total": total_items,
                    "pagina": pagina,
                    "total_paginas": total_paginas,
                    "itens_por_pagina": itens_por_pagina
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar emendas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/emendas/resumo", summary="Obtém resumo das emendas do Senado")
@lru_cache(maxsize=32)
def get_resumo_emendas(legislatura: int):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Totais Gerais (Optimized with CTE)
            if legislatura:
                query_totais = """
                    WITH senadores_nomes AS (
                        SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                        UNION
                        SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                    )
                    SELECT 
                        COUNT(DISTINCT s.id) as total_senadores,
                        COUNT(DISTINCT e.localidade_gasto) as total_municipios,
                        COUNT(DISTINCT e.funcao) as total_areas,
                        COALESCE(SUM(e.valor_pago), 0) as valor_total
                    FROM portal.emendas e
                    JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                    WHERE CAST(e.ano AS INTEGER) BETWEEN %s AND %s
                """
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                cursor.execute(query_totais, (start_year, end_year))
            else:
                query_totais = """
                    WITH senadores_nomes AS (
                        SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                        UNION
                        SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                    )
                    SELECT 
                        COUNT(DISTINCT s.id) as total_senadores,
                        COUNT(DISTINCT e.localidade_gasto) as total_municipios,
                        COUNT(DISTINCT e.funcao) as total_areas,
                        COALESCE(SUM(e.valor_pago), 0) as valor_total
                    FROM portal.emendas e
                    JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                """
                cursor.execute(query_totais)
            
            totais_row = cursor.fetchone()
            valor_total_global_totais = float(totais_row[3]) if totais_row[3] else 1.0
            
            # 2. Distribuição por Área (Optimized with CTE)
            if legislatura:
                query_areas = """
                    WITH senadores_nomes AS (
                        SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                        UNION
                        SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                    )
                    SELECT e.funcao, SUM(e.valor_pago) as valor_total
                    FROM portal.emendas e
                    JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                    WHERE CAST(e.ano AS INTEGER) BETWEEN %s AND %s
                    GROUP BY e.funcao
                    ORDER BY valor_total DESC
                """
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                cursor.execute(query_areas, (start_year, end_year))
            else:
                query_areas = """
                    WITH senadores_nomes AS (
                        SELECT lower(nome_completo) as nome FROM senado.parlamentar
                        UNION
                        SELECT lower(nome_parlamentar) as nome FROM senado.parlamentar
                    )
                    SELECT e.funcao, SUM(e.valor_pago) as valor_total
                    FROM portal.emendas e
                    JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                    GROUP BY e.funcao
                    ORDER BY valor_total DESC
                """
                cursor.execute(query_areas)
            
            areas_raw = cursor.fetchall()
            valor_total_global = sum(float(r[1]) for r in areas_raw) if areas_raw else 1.0

            areas_formatadas = [
                {
                    "nome": r[0] if r[0] else "Outros",
                    "valor": float(r[1]),
                    "percentual": round((float(r[1]) / valor_total_global) * 100, 1)
                }
                for r in areas_raw
            ]

            # 3. Top 10 Senadores (Optimized with CTE)
            if legislatura:
                query_top = """
                    WITH senadores_nomes AS (
                        SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                        UNION
                        SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                    )
                    SELECT 
                        p.codigo, p.nome_parlamentar, p.sigla_partido, p.uf, p.url_foto,
                        SUM(e.valor_pago) as total_valor
                    FROM portal.emendas e
                    JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                    JOIN senado.parlamentar p ON s.id = p.codigo
                    WHERE CAST(e.ano AS INTEGER) BETWEEN %s AND %s
                    GROUP BY p.codigo, p.nome_parlamentar, p.sigla_partido, p.uf, p.url_foto
                    ORDER BY total_valor DESC
                    LIMIT 10
                """
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                cursor.execute(query_top, (start_year, end_year))
            else:
                query_top = """
                    WITH senadores_nomes AS (
                        SELECT codigo as id, lower(nome_completo) as nome FROM senado.parlamentar
                        UNION
                        SELECT codigo as id, lower(nome_parlamentar) as nome FROM senado.parlamentar
                    )
                    SELECT 
                        p.codigo, p.nome_parlamentar, p.sigla_partido, p.uf, p.url_foto,
                        SUM(e.valor_pago) as total_valor
                    FROM portal.emendas e
                    JOIN senadores_nomes s ON lower(e.nome_autor) = s.nome
                    JOIN senado.parlamentar p ON s.id = p.codigo
                    GROUP BY p.codigo, p.nome_parlamentar, p.sigla_partido, p.uf, p.url_foto
                    ORDER BY total_valor DESC
                    LIMIT 10
                """
                cursor.execute(query_top)
            
            top_senadores = cursor.fetchall()

            return {
                "totais": {
                    "senadores": totais_row[0],
                    "municipios": totais_row[1],
                    "areas": totais_row[2],
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
                        "foto": r[4] if r[4] and str(r[4]).strip() else "/placeholder-user.svg"
                    }
                    for r in top_senadores
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar resumo emendas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/materia/votacao", summary="Obtém o histórico de votações de um projeto legislativo")
def get_votacao_materia(legislatura: int, codigo_materia: int):
    conn = None
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
            """
            params = [codigo_materia]
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query += " AND m.ano BETWEEN %s AND %s"
                params.extend([start_year, end_year])

            query += " ORDER BY m.ano DESC, m.sigla, m.numero, p.nome_parlamentar"
            cursor.execute(query, tuple(params))
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
        if conn:
            db.release_db_connection(conn)

@router.get("/{legislatura}/{senador_codigo}/emendas/lista", summary="Obtém a lista de emendas parlamentares de um senador")
def get_emendas_lista_senador(legislatura: int, senador_codigo: int, pagina: int = 1):
    itens_per_page = 15
    offset = (pagina - 1) * itens_per_page
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Total para paginação
            query_count = """
                SELECT COUNT(*)
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                   ON (lower(e.nome_autor) = lower(s.nome_completo) 
                       OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                WHERE s.codigo = %s
            """
            params_count = [senador_codigo]
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query_count += " AND e.ano BETWEEN %s AND %s"
                params_count.extend([start_year, end_year])

            cursor.execute(query_count, tuple(params_count))
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + itens_per_page - 1) // itens_per_page

            # 2. Dados paginados (Seleção Seletiva)
            query = """
                SELECT 
                    e.codigo_emenda as codigo,
                    e.ano,
                    e.tipo_emenda as tipo,
                    e.valor_pago,
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                  ON (lower(e.nome_autor) = lower(s.nome_completo) 
                      OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                WHERE s.codigo = %s
            """
            params = [senador_codigo]
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query += " AND e.ano BETWEEN %s AND %s"
                params.extend([start_year, end_year])

            query += " ORDER BY e.ano DESC, e.valor_pago DESC LIMIT %s OFFSET %s"
            params.extend([itens_per_page, offset])
            cursor.execute(query, tuple(params))
            res = cursor.fetchall()
            
            return {
                "emendas": [
                    {
                        "codigo": r[0],
                        "ano": r[1],
                        "tipo": r[2],
                        "valorPago": float(r[3]),
                        "funcao": r[4],
                        "localidade": r[5]
                    }
                    for r in res
                ],
                "paginacao": {
                    "total": total_items,
                    "pagina": pagina,
                    "total_paginas": total_paginas,
                    "itens_por_pagina": itens_per_page
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar emendas do senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{legislatura}/empresas/estatisticas", summary="Obtém estatísticas gerais das empresas")
@lru_cache(maxsize=4)
def get_estatisticas_empresas(legislatura: int):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query_gerais = """
               SELECT
                    COUNT(DISTINCT d.cpf_cnpj) as total_empresas,
                    SUM(d.valor_reembolsado) as total_pago,
                    COUNT(*) as total_contratos
                FROM senado.despesa_ceaps d
                LEFT JOIN senado.parlamentar p ON d.cod_senador = p.codigo
                JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
                WHERE 1=1
            """
            params_gerais = []
            if legislatura:
                query_gerais += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_gerais.extend([str(legislatura), str(legislatura)])
            
            cursor.execute(query_gerais, tuple(params_gerais))
            row_gerais = cursor.fetchone()

            query_top_10 = """
                SELECT
                    d.fornecedor as empresa,
                    SUM(d.valor_reembolsado) as valor_total
                FROM senado.despesa_ceaps d
                LEFT JOIN senado.parlamentar p ON d.cod_senador = p.codigo
                JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
                WHERE 1=1
            """
            params_top10 = []
            if legislatura:
                query_top_10 += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_top10.extend([str(legislatura), str(legislatura)])
            
            query_top_10 += " GROUP BY d.fornecedor ORDER BY valor_total DESC LIMIT 10"
            cursor.execute(query_top_10, tuple(params_top10))
            res_top_10 = cursor.fetchall()
            
            query_top_20 = """
WITH EmpresaStats AS (
    SELECT
        d.fornecedor,
        d.cpf_cnpj,
        SUM(d.valor_reembolsado) as valor_total,
        COUNT(*) as contratos
    FROM senado.despesa_ceaps d
    LEFT JOIN senado.parlamentar p ON d.cod_senador = p.codigo
    JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
    WHERE 1=1
"""
            if legislatura:
                query_top_20 += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
            
            query_top_20 += """
    GROUP BY d.fornecedor, d.cpf_cnpj
),
TotalGeral AS (
    SELECT SUM(d.valor_reembolsado) as soma_total FROM senado.despesa_ceaps d
    LEFT JOIN senado.parlamentar p ON d.cod_senador = p.codigo
    JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
    WHERE 1=1
"""
            if legislatura:
                query_top_20 += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                
            query_top_20 += """
),
EmpresaPartidos AS (
    SELECT
        d.fornecedor,
        d.cpf_cnpj,
        STRING_AGG(DISTINCT p.sigla_partido, ', ') as partidos
    FROM senado.despesa_ceaps d
    LEFT JOIN senado.parlamentar p ON d.cod_senador = p.codigo
    JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
    WHERE 1=1
"""
            if legislatura:
                query_top_20 += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"

            query_top_20 += """
    GROUP BY d.fornecedor, d.cpf_cnpj
)
SELECT
    ROW_NUMBER() OVER (ORDER BY es.valor_total DESC) as rank,
    es.fornecedor as empresa,
    COALESCE(ep.partidos, 'N/A') as partidos,
    es.cpf_cnpj as cnpj,
    es.valor_total,
    es.contratos,
    ROUND((es.valor_total / NULLIF(tg.soma_total, 0)) * 100, 2) as percentual
FROM EmpresaStats es
JOIN EmpresaPartidos ep ON es.fornecedor = ep.fornecedor AND es.cpf_cnpj = ep.cpf_cnpj
CROSS JOIN TotalGeral tg
ORDER BY es.valor_total DESC
LIMIT 20;
"""
            params_top20 = []
            if legislatura:
                params_top20.extend([str(legislatura), str(legislatura), str(legislatura), str(legislatura), str(legislatura), str(legislatura)])
            
            cursor.execute(query_top_20, tuple(params_top20))
            res_top_20 = cursor.fetchall()
            
            return {
                "total_empresas": row_gerais[0],
                "total_pago": float(row_gerais[1] or 0),
                "total_contratos": row_gerais[2],
                "top_10_empresas": [
                    {
                        "empresa": r[0],
                        "valor_total": float(r[1])
                    }
                    for r in res_top_10
                ],
                "top_20_empresas": [
                    {
                        "rank": r[0],
                        "empresa": r[1],
                        "partidos": r[2],
                        "cnpj": r[3],
                        "valor_total": float(r[4]),
                        "contratos": r[5],
                        "percentual": float(r[6])
                    }
                    for r in res_top_20
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas de empresas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        if conn:
            db.release_db_connection(conn)
