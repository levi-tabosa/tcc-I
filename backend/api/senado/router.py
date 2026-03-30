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

@router.get("/lista", summary="Lista todos os senadores ativos")
def get_lista_senadores(legislatura: int = Query(None)):
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





@router.get("/estatisticas")
@lru_cache(maxsize=16)
def get_estatisticas_senado(legislatura: int = Query(None)):
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

            query_gastos = "SELECT COALESCE(SUM(valor_reembolsado), 0) FROM senado.despesa_ceaps"
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
                query_regiao += " WHERE m.primeira_legislatura = %s OR m.segunda_legislatura = %s"
                params_reg.extend([str(legislatura), str(legislatura)])
                
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
        if conn:
            db.release_db_connection(conn)


@router.get("/comparar")
def get_comparativo_senadores(id1: int, id2: int, ano: int = None, legislatura: int = Query(None)):
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
        if conn:
            db.release_db_connection(conn)
                
@router.get("/comissoes", summary="Lista todas as comissões do Senado com membros")
def get_comissoes_senado(legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                 SELECT
                    c.codigo,
                    c.sigla,
                    c.nome,
                    'Comissão' AS tipo,
                    COUNT(DISTINCT mc.codigo_parlamentar) AS total_membros
                FROM senado.comissao c
                LEFT JOIN senado.membro_comissao mc ON c.codigo = mc.codigo_comissao
            """
            params = []
            if legislatura:
                query += """
                    INNER JOIN senado.mandato m ON mc.codigo_parlamentar = m.codigo_parlamentar
                    WHERE m.primeira_legislatura = %s OR m.segunda_legislatura = %s
                """
                params.extend([str(legislatura), str(legislatura)])
            
            query += " GROUP BY c.codigo, c.sigla, c.nome ORDER BY c.nome"
            cursor.execute(query, tuple(params))
            comissoes_raw = cursor.fetchall()
            
            comissoes = []
            for row in comissoes_raw:
                cod_comissao = row[0]

                query_membros = f"""
                    SELECT
                        p.nome_parlamentar,
                        p.sigla_partido,
                        p.uf,
                        mc.tipo_vaga AS cargo,
                        p.codigo,
                        p.url_foto
                    FROM senado.membro_comissao mc
                    JOIN senado.parlamentar p ON mc.codigo_parlamentar = p.codigo
                    {"INNER" if legislatura else "LEFT"} JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
                    WHERE mc.codigo_comissao = %s
                    {"AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)" if legislatura else ""}
                    ORDER BY mc.tipo_vaga NULLS LAST, p.nome_parlamentar
                """
                params_m = [cod_comissao]
                if legislatura:
                    params_m.extend([str(legislatura), str(legislatura)])
                cursor.execute(query_membros, tuple(params_m))
                membros_raw = cursor.fetchall()

                query_partidos = f"""
                    SELECT p.sigla_partido, COUNT(*) AS qtd
                    FROM senado.membro_comissao mc
                    JOIN senado.parlamentar p ON mc.codigo_parlamentar = p.codigo
                    {"INNER" if legislatura else "LEFT"} JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
                    WHERE mc.codigo_comissao = %s AND p.sigla_partido IS NOT NULL
                    {"AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)" if legislatura else ""}
                    GROUP BY p.sigla_partido
                    ORDER BY qtd DESC
                    LIMIT 4
                """
                params_p = [cod_comissao]
                if legislatura:
                    params_p.extend([str(legislatura), str(legislatura)])
                cursor.execute(query_partidos, tuple(params_p))
                partidos_raw = cursor.fetchall()

                presidente = next((m[0] for m in membros_raw if m[3] and "presidente" in m[3].lower()), None)
                
                comissoes.append({
                    "id": row[0],
                    "sigla": row[1],
                    "nome": row[2],
                    "tipo": row[3],
                    "total_membros": row[4],
                    "presidente": presidente,
                    "partidos_destaque": [p[0] for p in partidos_raw],
                    "membros": [
                        {
                            "nome": mb[0],
                            "partido": mb[1] or "S/P",
                            "uf": mb[2] or "BR",
                            "cargo": mb[3],
                            "id": mb[4],
                            "foto": mb[5]
                        }
                        for mb in membros_raw
                    ]
                })
            return {
                "total": len(comissoes),
                "comissoes": comissoes
            }

    except Exception as e:
        logging.error(f"Erro ao buscar comissões do senado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar comissões")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/{senador_codigo}", summary="Obtém o perfil detalhado de um senador")
def get_perfil_senador(senador_codigo: int, legislatura: int = Query(None)):    
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
                    "legislaturas_ativas": legislaturas_ativas
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar senador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar senador")
    finally:
        if conn:
            db.release_db_connection(conn)


@router.get("/{senador_codigo}/despesas", summary="Obtém o extrato de despesas de um senador")
def get_despesas_senador(senador_codigo: int, legislatura: int = Query(None), pagina: int = 1):
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
                INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
                WHERE d.cod_senador = %s"""
            params_count = [senador_codigo]
            if legislatura:
                query_count += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_count.extend([str(legislatura), str(legislatura)])
            
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
                INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
                WHERE d.cod_senador = %s 
            """
            params_rec = [senador_codigo]
            if legislatura:
                query_recente += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_rec.extend([str(legislatura), str(legislatura)])
                
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
                INNER JOIN senado.mandato m ON d.cod_senador = m.codigo_parlamentar
                WHERE d.cod_senador = %s
            """
            params_cat = [senador_codigo]
            if legislatura:
                query_categorias += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params_cat.extend([str(legislatura), str(legislatura)])
            
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

@router.get("/despesas/estatisticas")
@lru_cache(maxsize=16)
def get_despesas_estatisticas(legislatura: int = Query(None)):
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
            if legislatura:
                query += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params.extend([str(legislatura), str(legislatura)])
            
            cursor.execute(query, tuple(params))
            res_total = cursor.fetchone()
            total_gastos = res_total[0] if res_total else 0

            query_media = """SELECT 
    COALESCE(SUM(valor_reembolsado) / NULLIF(COUNT(DISTINCT cod_senador), 0), 0) AS media_por_senador
FROM senado.despesa_ceaps;
"""
            cursor.execute(query_media)
            res_media = cursor.fetchone()
            media_por_senador = res_media[0] if res_media else 0
            
            query_partidos = """WITH total_geral AS (
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
            cursor.execute(query_partidos)
            partidos = cursor.fetchall()
            
            query_cat = """WITH ranking_categorias AS (
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
ORDER BY (CASE WHEN SUM(valor) > 0 THEN 0 ELSE 1 END), total_valor DESC;
"""
            cursor.execute(query_cat)
            categorias = cursor.fetchall()
            
            query_top = """SELECT 
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
            cursor.execute(query_top)
            top_10 = cursor.fetchall()

            # Evolução Mensal
            query_evolucao = """SELECT 
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
            cursor.execute(query_evolucao)
            gastos_mensais = cursor.fetchall()

            query_12m = """SELECT 
    COALESCE(SUM(valor_reembolsado), 0) AS total_geral
FROM senado.despesa_ceaps
WHERE data_despesa >= (CURRENT_DATE - INTERVAL '1 year');
"""
            cursor.execute(query_12m)
            res_total_12 = cursor.fetchone()
            total_12_meses = res_total_12[0] if res_total_12 else 0
            
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


@router.get("/emendas", summary="Busca uma lista de emendas parlamentares do Senado")
def get_lista_emendas(
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
                SELECT COUNT(*)
                FROM portal.emendas e
                JOIN senado.parlamentar s 
                   ON (lower(e.nome_autor) = lower(s.nome_completo) 
                       OR lower(e.nome_autor) = lower(s.nome_parlamentar))
                WHERE e.autor_tipo = 'SENADOR'
            """
            params_count = []
            if nome_senador:
                query_count += " AND s.nome_parlamentar ILIKE %s"
                params_count.append(f"%{nome_senador}%")
            if ano:
                query_count += " AND e.ano = %s"
                params_count.append(ano)
            
            cursor.execute(query_count, tuple(params_count))
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + itens_por_pagina - 1) // itens_por_pagina

            # 2. Dados paginados (Seleção Seletiva)
            query = """
                SELECT 
                    s.nome_parlamentar as senador,
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
                WHERE e.autor_tipo = 'SENADOR'
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


@router.get("/emendas/resumo", summary="Obtém resumo das emendas do Senado")
@lru_cache(maxsize=8)
def get_resumo_emendas():
    conn = None
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
        if conn:
            db.release_db_connection(conn)


@router.get("/materia/votacao", summary="Obtém o histórico de votações de um projeto legislativo")
def get_votacao_materia(codigo_materia: int):
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
        if conn:
            db.release_db_connection(conn)


@router.get("/estatisticas", summary="Obtém estatísticas gerais dos senadores")
@lru_cache(maxsize=4)
def get_estatisticas_gerais(legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """SELECT COUNT(DISTINCT p.codigo) AS total_senadores
FROM senado.parlamentar p
INNER JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
WHERE 1=1"""
            params = []
            if legislatura:
                query += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params.extend([str(legislatura), str(legislatura)])

            cursor.execute(query, tuple(params))
            total_senadores = cursor.fetchone()[0]

            query_regioes_count = """SELECT COUNT(DISTINCT
    CASE
        WHEN p.uf IN ('AC','AP','AM','PA','RO','RR','TO') THEN 'Norte'
        WHEN p.uf IN ('AL','BA','CE','MA','PB','PE','PI','RN','SE') THEN 'Nordeste'
        WHEN p.uf IN ('DF','GO','MT','MS') THEN 'Centro-Oeste'
        WHEN p.uf IN ('ES','MG','RJ','SP') THEN 'Sudeste'
        WHEN p.uf IN ('PR','RS','SC') THEN 'Sul'
    END
) AS total_regioes
FROM senado.parlamentar p
INNER JOIN senado.mandato m ON p.codigo = m.codigo_parlamentar
WHERE p.uf IS NOT NULL"""
            params = []
            if legislatura:
                query_regioes_count += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params.extend([str(legislatura), str(legislatura)])
            cursor.execute(query_regioes_count, tuple(params))
            total_regioes = cursor.fetchone()[0]

            query_regioes = """SELECT 
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
WHERE p.uf IS NOT NULL"""
            params = []
            if legislatura:
                query_regioes += " AND (m.primeira_legislatura = %s OR m.segunda_legislatura = %s)"
                params.extend([str(legislatura), str(legislatura)])
                
            query_regioes += " GROUP BY regiao ORDER BY quantidade DESC;"
            cursor.execute(query_regioes, tuple(params))
            regioes = cursor.fetchall()
            
            return {
                "total_senadores": total_senadores,
                "total_regioes": total_regioes,
                "senadores_por_regiao": [
                    {
                        "name": r[0],
                        "value": r[1]
                    }
                    for r in regioes
                ]
            }
            
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas gerais do senado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas gerais")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/{senador_codigo}/emendas/lista", summary="Obtém a lista de emendas parlamentares de um senador")
def get_emendas_lista_senador(senador_codigo: int, pagina: int = 1):
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
            cursor.execute(query_count, (senador_codigo,))
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
                ORDER BY e.ano DESC, e.valor_pago DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (senador_codigo, itens_per_page, offset))
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
#     finally:
#         if conn:
#             db.release_db_connection(conn)


