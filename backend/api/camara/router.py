from fastapi import APIRouter, HTTPException, Query
from datetime import date
import psycopg2
import logging
from functools import lru_cache

# Garanta que este import está correto para sua estrutura
import database.db as db

router = APIRouter(
    prefix="/camara",
    tags=["Câmara"]
)


@router.get("/legislaturas", summary="Lista todas as legislaturas disponíveis na base")
@lru_cache(maxsize=1)
def get_legislaturas_camara():
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT legislatura_id
                FROM camara.deputados_mandatos
                WHERE legislatura_id <= 57
                ORDER BY legislatura_id DESC
            """
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Erro ao buscar legislaturas ativas camara: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar legislaturas")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/emendas", summary="Busca uma lista de emendas parlamentares")
def get_lista_emendas(
    nome_deputado: str = Query(None),
    ano: int = Query(None),
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
            # 1. Total para paginação
            query_count = """
                WITH parlamentares_nomes AS (
                    SELECT d.id, lower(d.nome_civil) as nome 
                    FROM camara.deputados d
                    UNION
                    SELECT m.deputado_id as id, lower(m.nome_eleitoral) as nome 
                    FROM camara.deputados_mandatos m
                )
                SELECT COUNT(*)
                FROM portal.emendas e
                JOIN parlamentares_nomes p ON lower(e.autor) = p.nome
            """
            
            # Adicionar filtro de legislatura se especificado
            where_conditions = []
            params_count = []
            
            if legislatura:
                query_count += """
                    JOIN camara.deputados_mandatos m ON p.id = m.deputado_id
                """
                where_conditions.append("m.legislatura_id = %s")
                params_count.append(legislatura)
            
            if nome_deputado:
                where_conditions.append("""p.id IN (
                    SELECT id FROM camara.deputados WHERE nome_civil ILIKE %s
                )""")
                params_count.append(f"%{nome_deputado}%")
            
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
                WITH parlamentares_nomes AS (
                    SELECT d.id, lower(d.nome_civil) as nome, d.nome_civil 
                    FROM camara.deputados d
                    UNION
                    SELECT m.deputado_id as id, lower(m.nome_eleitoral) as nome, m.nome_eleitoral as nome_civil 
                    FROM camara.deputados_mandatos m
                )
                SELECT 
                    p.nome_civil as deputado,
                    e.codigo_emenda as codigo,
                    e.ano,
                    e.tipo_emenda as tipo,
                    e.valor_pago,
                    e.funcao,
                    e.localidade_gasto as localidade,
                    p.id as deputado_id
                FROM portal.emendas e
                JOIN parlamentares_nomes p ON lower(e.autor) = p.nome
            """
            
            # Adicionar JOIN e filtros
            where_conditions_data = []
            params = []
            
            if legislatura:
                query += """
                    JOIN camara.deputados_mandatos m ON p.id = m.deputado_id
                """
                where_conditions_data.append("m.legislatura_id = %s")
                params.append(legislatura)
            
            if nome_deputado:
                where_conditions_data.append("p.nome_civil ILIKE %s")
                params.append(f"%{nome_deputado}%")
            
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
                        "deputado": r[0],
                        "codigo": r[1],
                        "ano": r[2],
                        "tipo": r[3],
                        "valorPago": float(r[4]),
                        "funcao": r[5],
                        "localidade": r[6],
                        "deputadoId": r[7]
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

@router.get("/emendas/resumo", summary="Obtém resumo das emendas")
@lru_cache(maxsize=32)
def get_resumo_emendas(legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # Base query components
            leg_join = ""
            leg_where = ""
            leg_params = []
            
            if legislatura:
                leg_join = "JOIN camara.deputados_mandatos m ON p.id = m.deputado_id"
                leg_where = "WHERE m.legislatura_id = %s"
                leg_params = [legislatura]
            
            # 1. Totais Gerais
            query_totais = f"""
                WITH parlamentares_nomes AS (
                    SELECT id FROM camara.deputados
                    UNION
                    SELECT deputado_id as id FROM camara.deputados_mandatos
                ),
                deputados_emendas AS (
                    SELECT e.id, e.valor_pago, e.localidade_gasto, e.funcao, p.id as deputado_id
                    FROM portal.emendas e
                    JOIN (
                        SELECT id, lower(nome_civil) as nome FROM camara.deputados
                        UNION
                        SELECT deputado_id as id, lower(nome_eleitoral) as nome FROM camara.deputados_mandatos
                    ) p ON lower(e.autor) = p.nome
                    {leg_join}
                    {leg_where}
                )
                SELECT 
                    COUNT(DISTINCT deputado_id) as total_deputados,
                    COUNT(DISTINCT localidade_gasto) as total_municipios,
                    COUNT(DISTINCT funcao) as total_areas,
                    COALESCE(SUM(valor_pago), 0) as valor_total
                FROM deputados_emendas
            """
            cursor.execute(query_totais, tuple(leg_params))
            totais_row = cursor.fetchone()
            valor_total_global = float(totais_row[3]) if totais_row[3] else 1.0
            
            # 2. Distribuição por Área
            query_areas = f"""
                WITH deputados_emendas AS (
                    SELECT e.valor_pago, e.funcao, p.id as deputado_id
                    FROM portal.emendas e
                    JOIN (
                        SELECT id, lower(nome_civil) as nome FROM camara.deputados
                        UNION
                        SELECT deputado_id as id, lower(nome_eleitoral) as nome FROM camara.deputados_mandatos
                    ) p ON lower(e.autor) = p.nome
                    {leg_join}
                    {leg_where}
                )
                SELECT funcao, SUM(valor_pago) as valor_total
                FROM deputados_emendas
                GROUP BY funcao
                ORDER BY valor_total DESC
            """
            cursor.execute(query_areas, tuple(leg_params))
            areas_raw = cursor.fetchall()
            
            areas_formatadas = [
                {
                    "nome": r[0] if r[0] else "Outros",
                    "valor": float(r[1]),
                    "percentual": round((float(r[1]) / (valor_total_global or 1)) * 100, 1)
                }
                for r in areas_raw
            ]
            
            # 3. Top 10 Deputados
            query_top = f"""
                WITH deputados_emendas AS (
                    SELECT e.valor_pago, p.id as deputado_id
                    FROM portal.emendas e
                    JOIN (
                        SELECT id, lower(nome_civil) as nome FROM camara.deputados
                        UNION
                        SELECT deputado_id as id, lower(nome_eleitoral) as nome FROM camara.deputados_mandatos
                    ) p ON lower(e.autor) = p.nome
                    {leg_join}
                    {leg_where}
                )
                SELECT 
                    d.id, d.nome_civil, m.sigla_partido, m.sigla_uf,
                    SUM(de.valor_pago) as total_valor
                FROM deputados_emendas de
                JOIN camara.deputados d ON de.deputado_id = d.id
                LEFT JOIN (
                    SELECT DISTINCT ON (deputado_id) deputado_id, sigla_partido, sigla_uf
                    FROM camara.deputados_mandatos
                    ORDER BY deputado_id, id DESC
                ) m ON d.id = m.deputado_id
                GROUP BY d.id, d.nome_civil, m.sigla_partido, m.sigla_uf
                ORDER BY total_valor DESC
                LIMIT 10
            """
            cursor.execute(query_top, tuple(leg_params))
            top_deputados = cursor.fetchall()

            return {
                "totais": {
                    "deputados": totais_row[0],
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
                        "emendasTotal": float(r[4]),
                        "foto": f"https://www.camara.leg.br/internet/deputado/bandep/{r[0]}.jpg"
                    }
                    for r in top_deputados
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao obter resumo de emendas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar resumo de emendas")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/proposicoes", summary="Busca uma lista de projetos legislativos")
def get_lista_proposicoes(
    siglaTipo: str = Query(None), 
    ano: int = Query(None), 
    ementa: str = Query(None), 
    deputado: str = Query(None),
    legislatura: int = Query(None),
    limite: int = Query(15),
    pagina: int = 1
):
    offset = (pagina - 1) * limite
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Total para paginação
            query_count = """
                SELECT COUNT(DISTINCT p.id)
                FROM camara.proposicoes p
            """
            if deputado:
                query_count += """
                    INNER JOIN camara.votacoes_proposicoes vp ON p.id = vp.proposicao_id
                    INNER JOIN camara.votacoes_votos vv ON vp.votacao_id = vv.votacao_id
                    INNER JOIN camara.deputados d ON vv.deputado_id = d.id
                """
            query_count += " WHERE 1=1"
            params_count = []
            if siglaTipo:
                query_count += " AND p.sigla_tipo = %s"
                params_count.append(siglaTipo)
            if ano:
                query_count += " AND p.ano = %s"
                params_count.append(ano)
            if ementa:
                query_count += " AND p.ementa ILIKE %s"
                params_count.append(f"%{ementa}%")
            if deputado:
                query_count += " AND d.nome_civil ILIKE %s"
                params_count.append(f"%{deputado}%")
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query_count += " AND p.ano BETWEEN %s AND %s"
                params_count.extend([start_year, end_year])
            
            cursor.execute(query_count, tuple(params_count))
            total_items = cursor.fetchone()[0]
            total_paginas = (total_items + limite - 1) // limite

            # 2. Dados paginados
            query = """
                SELECT DISTINCT ON (p.id)
                    p.id, 
                    p.sigla_tipo as "siglaTipo", 
                    p.numero, 
                    p.ano, 
                    p.ementa, 
                    p.data_apresentacao as "dataApresentacao"
                FROM camara.proposicoes p
            """
            params = []
            
            if deputado:
                query += """
                    INNER JOIN camara.votacoes_proposicoes vp ON p.id = vp.proposicao_id
                    INNER JOIN camara.votacoes_votos vv ON vp.votacao_id = vv.votacao_id
                    INNER JOIN camara.deputados d ON vv.deputado_id = d.id
                """
            
            query += " WHERE 1=1"
            
            if siglaTipo:
                query += " AND p.sigla_tipo = %s"
                params.append(siglaTipo)
            if ano:
                query += " AND p.ano = %s"
                params.append(ano)
            if ementa:
                query += " AND p.ementa ILIKE %s"
                params.append(f"%{ementa}%")
            if deputado:
                query += " AND d.nome_civil ILIKE %s"
                params.append(f"%{deputado}%")
            if legislatura:
                start_year = 2023 - (57 - legislatura) * 4
                end_year = start_year + 3
                query += " AND p.ano BETWEEN %s AND %s"
                params.extend([start_year, end_year])
                
            query += " ORDER BY p.id DESC LIMIT %s OFFSET %s"
            params.extend([limite, offset])

            cursor.execute(query, tuple(params))
            res = cursor.fetchall()
            
            return {
                "proposicoes": [
                    {
                        "id": r[0],
                        "siglaTipo": r[1],
                        "numero": r[2],
                        "ano": r[3],
                        "ementa": r[4],
                        "dataApresentacao": r[5].isoformat() if hasattr(r[5], 'isoformat') else str(r[5]) if r[5] else None,
                        "autor_principal": "Desconhecido"
                    }
                    for r in res
                ],
                "paginacao": {
                    "total": total_items,
                    "pagina": pagina,
                    "total_paginas": total_paginas,
                    "itens_por_pagina": limite
                }
            }
    except Exception as e:
        logging.error(f"Erro ao buscar proposições: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar proposições")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/proposicoes/{proposicao_id}/votos", summary="Obtém o histórico de votos de um projeto legislativo")
def get_votos_proposicao(proposicao_id: int):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    v.id AS votacao_id,
                    v.data as data_votacao,
                    v.descricao,
                    d.id AS deputado_id,
                    d.nome_civil,
                    vv.tipo_voto AS voto
                FROM camara.votacoes_proposicoes vp
                INNER JOIN camara.votacoes v ON vp.votacao_id = v.id
                INNER JOIN camara.votacoes_votos vv ON v.id = vv.votacao_id
                INNER JOIN camara.deputados d ON vv.deputado_id = d.id
                WHERE vp.proposicao_id = %s AND vv.tipo_voto != 'Artigo 17'
                ORDER BY v.data DESC, d.nome_civil ASC
            """
            cursor.execute(query, (proposicao_id,))
            resultados = cursor.fetchall()
            
            votacoes_dict = {}
            for r in resultados:
                vot_id = r[0]
                if vot_id not in votacoes_dict:
                    votacoes_dict[vot_id] = {
                        "id_votacao": vot_id,
                        "data": r[1].isoformat() if hasattr(r[1], 'isoformat') else str(r[1]) if r[1] else None,
                        "descricao": r[2],
                        "total_votos": 0,
                        "lista_votos": []
                    }
                
                votacoes_dict[vot_id]["lista_votos"].append({
                    "deputado_id": r[3],
                    "nome": r[4],
                    "voto": r[5]
                })
                votacoes_dict[vot_id]["total_votos"] += 1

            return {
                "proposicao_id": proposicao_id,
                "historico_votacoes": list(votacoes_dict.values())
            }
    except Exception as e:
        logging.error(f"Erro ao buscar votos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar votos")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/lista", summary="Lista todos os deputados ativos")
@lru_cache(maxsize=16)
def get_todos_deputados(legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT ON (d.id)
                    d.id, 
                    d.nome_civil,
                    m.sigla_partido,
                    m.sigla_uf as uf
                FROM camara.deputados d
                INNER JOIN camara.deputados_mandatos m ON d.id = m.deputado_id
                WHERE m.sigla_uf IS NOT NULL
            """
            params = []
            if legislatura:
                query += " AND m.legislatura_id = %s"
                params.append(legislatura)
                
            query += " ORDER BY d.id, m.id DESC"
            cursor.execute(query, tuple(params))
            res = cursor.fetchall()

            return [
                {
                    "id": r[0],
                    "nome_civil": r[1],
                    "sigla_partido": r[2] if r[2] else "S/P",
                    "uf": r[3]
                }
                for r in res
            ]
    except Exception as e:
        logging.error(f"Erro ao buscar lista de deputados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar lista de deputados")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/estatisticas", summary="Obtém estatísticas gerais dos deputados")
@lru_cache(maxsize=8)
def get_estatisticas_gerais(legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Total de Deputados
            query_total = "SELECT COUNT(DISTINCT deputado_id) as total from camara.deputados_mandatos"
            params = []
            if legislatura:
                query_total += " WHERE legislatura_id = %s"
                params.append(legislatura)
            
            cursor.execute(query_total, tuple(params))
            total_deputados = cursor.fetchone()[0] or 0

            # 2. Distribuição por Região
            query_regiao = """
                SELECT 
                    CASE
                        WHEN m.sigla_uf IN ('AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO') THEN 'Norte'
                        WHEN m.sigla_uf IN ('AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE') THEN 'Nordeste'
                        WHEN m.sigla_uf IN ('DF', 'GO', 'MT', 'MS') THEN 'Centro-Oeste'
                        WHEN m.sigla_uf IN ('ES', 'MG', 'RJ', 'SP') THEN 'Sudeste'
                        WHEN m.sigla_uf IN ('PR', 'RS', 'SC') THEN 'Sul'
                        ELSE 'Outros'
                    END AS regiao,
                    COUNT(DISTINCT m.deputado_id) as quantidade
                FROM camara.deputados_mandatos m
                WHERE m.sigla_uf IS NOT NULL
            """
            if legislatura:
                query_regiao += " AND m.legislatura_id = %s"
            
            query_regiao += " GROUP BY regiao ORDER BY quantidade DESC"
            
            cursor.execute(query_regiao, (legislatura,) if legislatura else ())
            deputados_regiao = [{"name": r[0], "value": int(r[1])} for r in cursor.fetchall()]

            return {
                "total_deputados": int(total_deputados),
                "deputados_por_regiao": deputados_regiao
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas gerais: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas")
    finally:
        if conn:
            db.release_db_connection(conn)



@router.get("/comparar", summary="Compara perfil e gastos entre dois deputados")
def get_comparativo_deputados(id1: int, id2: int, ano: int = None, legislatura: int = Query(None)):
    if id1 == id2:
        raise HTTPException(status_code=400, detail="Escolha dois deputados diferentes para comparar.")

    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar Perfis
            query_perfil = """
                SELECT DISTINCT ON (d.id)
                    d.id, d.nome_civil, m.sigla_partido, m.sigla_uf, 
                    d.email, d.data_nascimento, d.escolaridade, d.uf_nascimento
                FROM camara.deputados d
                LEFT JOIN camara.deputados_mandatos m ON d.id = m.deputado_id
                WHERE d.id IN (%s, %s)
                ORDER BY d.id, m.id DESC
            """
            cursor.execute(query_perfil, (id1, id2))
            perfis_raw = cursor.fetchall()
            
            if len(perfis_raw) < 2:
                raise HTTPException(status_code=404, detail="Um ou ambos os deputados não foram encontrados.")
            
            comparacao = {}
            for r in perfis_raw:
                pid = r[0]
                comparacao[pid] = {
                    "id": pid,
                    "nome_civil": r[1],
                    "sigla_partido": r[2],
                    "sigla_uf": r[3],
                    "email": r[4],
                    "data_nascimento": r[5].isoformat() if isinstance(r[5], date) else None,
                    "escolaridade": r[6],
                    "uf_nascimento": r[7],
                    "foto": f"https://www.camara.leg.br/internet/deputado/bandep/{pid}.jpg",
                    "total_gasto": 0.0,
                    "qtd_despesas": 0,
                    "maior_categoria": {"nome": "-", "valor": 0.0},
                    "despesas": [],
                    "categorias": []
                }
            
            # 2. Buscar Despesas
            query_stats = """
                SELECT 
                    m.deputado_id, d.tipo_despesa, 
                    SUM(d.valor_documento) as total, COUNT(d.id) as qtd
                FROM camara.deputados_despesas d
                JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
                WHERE m.deputado_id IN (%s, %s)
            """
            params = [id1, id2]
            if ano:
                query_stats += " AND d.ano = %s"
                params.append(ano)
            if legislatura:
                query_stats += " AND m.legislatura_id = %s"
                params.append(legislatura)
                
            query_stats += " GROUP BY m.deputado_id, d.tipo_despesa"

            cursor.execute(query_stats, tuple(params))
            stats = cursor.fetchall()

            for s in stats:
                dep_id, valor = s[0], float(s[2])
                if dep_id in comparacao:
                    comparacao[dep_id]["total_gasto"] += valor
                    comparacao[dep_id]["qtd_despesas"] += s[3]
                    comparacao[dep_id]["categorias"].append({"categoria": s[1], "valor": valor})

                    if valor > comparacao[dep_id]["maior_categoria"]["valor"]:
                        comparacao[dep_id]["maior_categoria"] = {
                            "nome": s[1].replace("_", " ").title() if s[1] else "-",
                            "valor": valor
                        }

            # 3. Buscar Últimas Despesas (Top 10)
            for dep_id in [id1, id2]:
                cursor.execute("""
                    SELECT d.ano, d.mes, d.tipo_despesa, d.valor_documento as valor, d.url_documento
                    FROM camara.deputados_despesas d
                    JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
                    WHERE m.deputado_id = %s
                    ORDER BY d.ano DESC, d.mes DESC
                    LIMIT 10
                """, (dep_id,))
                recentes = cursor.fetchall()
                
                comparacao[dep_id]["despesas"] = [
                    {
                        "ano": r[0],
                        "mes": r[1],
                        "tipo_despesa": r[2],
                        "valor": float(r[3]),
                        "url_documento": r[4]
                    }
                    for r in recentes
                ]
            
            return [comparacao[id1], comparacao[id2]]
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erro ao comparar deputados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar comparação")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/{deputado_id}", summary="Obtém os detalhes do perfil e despesas do deputado pelo ID")
def get_perfil_deputado(deputado_id: int, legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar Perfil (Resiliente a legislatura inexistente)
            query_perfil = """
                SELECT d.id, d.nome_civil, d.cpf, d.sexo, d.email, d.data_nascimento, 
                       d.escolaridade, d.uf_nascimento, d.municipio_nascimento, 
                       m.sigla_partido, m.sigla_uf, m.legislatura_id
                FROM camara.deputados d
                LEFT JOIN camara.deputados_mandatos m ON d.id = m.deputado_id
                WHERE d.id = %s
            """
            params_perfil = [deputado_id]
            
            if legislatura:
                # Ordena para colocar a legislatura pedida no topo (se existir), senão a mais recente
                query_perfil += " ORDER BY (m.legislatura_id = %s) DESC NULLS LAST, m.id DESC LIMIT 1"
                params_perfil.append(legislatura)
            else:
                query_perfil += " ORDER BY m.id DESC LIMIT 1"
            
            cursor.execute(query_perfil, tuple(params_perfil))
            row = cursor.fetchone()
            
            if not row:
                # Verifica se o ID pelo menos existe na tabela base
                cursor.execute("SELECT id FROM camara.deputados WHERE id = %s", (deputado_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"Deputado com ID {deputado_id} não encontrado")
                else:
                    # Existe mas sem mandatos registrados? (Raro)
                    raise HTTPException(status_code=404, detail=f"Deputado com ID {deputado_id} não possui mandatos registrados")

            # A legislatura efetivamente encontrada (pode ser diferente da pedida)
            # Se legislatura for 0, tratamos como 'Todas', então leg_efetiva fica None para não filtrar despesas
            leg_efetiva = row[11] if legislatura else None
            
            res = {
                "id": row[0],
                "nome_civil": row[1],
                "cpf": row[2],
                "sexo": row[3],
                "email": row[4],
                "data_nascimento": row[5].isoformat() if isinstance(row[5], date) else None,
                "escolaridade": row[6],
                "uf_nascimento": row[7],
                "municipio_nascimento": row[8],
                "sigla_partido": row[9] if row[9] else "S/P",
                "sigla_uf": row[10],
                "foto": f"https://www.camara.leg.br/internet/deputado/bandep/{row[0]}.jpg",
                "legislatura_exibida": leg_efetiva
            }

            # 2. Buscar as 50 despesas mais recentes (Usando a legislatura efetiva)
            query_recente = """
                SELECT 
                    desp.ano, desp.mes, desp.tipo_despesa, 
                    desp.valor_documento as valor, desp.url_documento
                FROM camara.deputados_despesas AS desp
                JOIN camara.deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
            """
            params_recente = [deputado_id]
            if leg_efetiva:
                query_recente += " AND mand.legislatura_id = %s"
                params_recente.append(leg_efetiva)
            
            query_recente += " ORDER BY desp.ano DESC, desp.mes DESC LIMIT 50"
            cursor.execute(query_recente, tuple(params_recente))
            despesas_raw = cursor.fetchall()
            despesas = [
                {
                    "ano": r[0],
                    "mes": r[1],
                    "tipo_despesa": r[2],
                    "valor": float(r[3]),
                    "url_documento": r[4]
                }
                for r in despesas_raw
            ]

            # 3. Resumo por categoria (Usando a legislatura efetiva)
            query_categorias = """
                SELECT desp.tipo_despesa as categoria, SUM(desp.valor_documento) as valor
                FROM camara.deputados_despesas AS desp
                JOIN camara.deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
            """
            params_cat = [deputado_id]
            if leg_efetiva:
                query_categorias += " AND mand.legislatura_id = %s"
                params_cat.append(leg_efetiva)
            
            query_categorias += " GROUP BY desp.tipo_despesa ORDER BY valor DESC"
            cursor.execute(query_categorias, tuple(params_cat))
            categorias_raw = cursor.fetchall()
            categorias = [{"categoria": r[0], "valor": float(r[1])} for r in categorias_raw]
            total_despesas = sum(c["valor"] for c in categorias)

            # 4. Buscar Resumo de Emendas (Não depende de legislatura do mandato)
            query_emendas_resumo = """
                WITH parlamentares_nomes AS (
                    SELECT id, lower(nome_civil) as nome FROM camara.deputados
                    UNION
                    SELECT deputado_id as id, lower(nome_eleitoral) as nome FROM camara.deputados_mandatos
                )
                SELECT SUM(e.valor_pago) as total_emendas
                FROM portal.emendas e
                JOIN parlamentares_nomes p ON lower(e.autor) = p.nome
                WHERE p.id = %s
            """
            cursor.execute(query_emendas_resumo, (deputado_id,))
            row_emendas = cursor.fetchone()
            total_emendas = float(row_emendas[0]) if row_emendas and row_emendas[0] else 0.0

            # 5. Legislaturas Ativas
            query_legis = """
                SELECT DISTINCT legislatura_id
                FROM camara.deputados_mandatos
                WHERE deputado_id = %s AND legislatura_id <= 57
                ORDER BY legislatura_id DESC
            """
            cursor.execute(query_legis, (deputado_id,))
            legislaturas_ativas = [row[0] for row in cursor.fetchall()]

            return {
                **res,
                "despesas": despesas,
                "total_despesas": total_despesas,
                "categorias": categorias,
                "total_emendas": total_emendas,
                "legislaturas_ativas": legislaturas_ativas
            }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erro ao buscar perfil do deputado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar perfil")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/{deputado_id}/emendas", summary="Obtém a lista de emendas parlamentares de um deputado")
def get_emendas_deputado(deputado_id: int):
    conn = None
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
                    e.valor_pago,
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN camara.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
                WHERE d.id = %s
                ORDER BY e.ano DESC, e.valor_pago DESC
            """
            cursor.execute(query, (deputado_id,))
            res = cursor.fetchall()
            
            return [
                {
                    "codigo": r[0],
                    "ano": r[1],
                    "tipo": r[2],
                    "valorPago": float(r[3]),
                    "funcao": r[4],
                    "localidade": r[5]
                }
                for r in res
            ]
    except Exception as e:
        logging.error(f"Erro ao buscar emendas do deputado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/despesas/estatisticas", summary="Obtém o panorama geral de gastos da Câmara")
@lru_cache(maxsize=4)
def get_estatisticas_despesas(legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Gastos por Categoria
            query_cat = """
                SELECT d.tipo_despesa as categoria, SUM(d.valor_documento) as valor
                FROM camara.deputados_despesas d
                JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
                WHERE 1=1
            """
            params = []
            if legislatura:
                query_cat += " AND m.legislatura_id = %s"
                params.append(legislatura)
            
            query_cat += " GROUP BY d.tipo_despesa ORDER BY valor DESC"
            cursor.execute(query_cat, tuple(params))
            resultados_categoria = cursor.fetchall()
            
            gastos_categoria = []
            total_outros = 0.0
            LIMITE_TOP = 9
            
            for i, r in enumerate(resultados_categoria):
                nome_formatado = r[0].title().replace("_", " ") if r[0] else "Outros"
                valor = float(r[1])
                
                if i < LIMITE_TOP:
                    gastos_categoria.append({"categoria": nome_formatado, "valor": valor})
                else:
                    total_outros += valor
            
            if total_outros > 0:
                gastos_categoria.append({"categoria": "Outros", "valor": total_outros})

            # 2. Evolução Mensal
            query_mensal = """
                SELECT d.ano, d.mes, SUM(d.valor_documento) as valor
                FROM camara.deputados_despesas d
                JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
                WHERE 1=1
            """
            params_mensal = []
            if legislatura:
                query_mensal += " AND m.legislatura_id = %s"
                params_mensal.append(legislatura)
                
            query_mensal += " GROUP BY d.ano, d.mes ORDER BY d.ano DESC, d.mes DESC LIMIT 12"
            cursor.execute(query_mensal, tuple(params_mensal))
            gastos_mensais = [{"ano": r[0], "mes": r[1], "valor": float(r[2])} for r in cursor.fetchall()]
            
            # 3. Gastos por Estado
            query_estado = """
                SELECT m.sigla_uf as estado, SUM(desp.valor_documento) as valor
                FROM camara.deputados_mandatos m
                JOIN camara.deputados_despesas desp ON m.id = desp.mandato_id
                WHERE m.sigla_uf IS NOT NULL
            """
            params_est = []
            if legislatura:
                query_estado += " AND m.legislatura_id = %s"
                params_est.append(legislatura)
            
            query_estado += " GROUP BY m.sigla_uf ORDER BY valor DESC"
            cursor.execute(query_estado, tuple(params_est))
            gastos_estado = [{"estado": r[0], "valor": float(r[1])} for r in cursor.fetchall()]

            # 4. Gastos por Partido
            query_partido = """
                SELECT m.sigla_partido as partido, SUM(desp.valor_documento) as valor
                FROM camara.deputados_mandatos m
                JOIN camara.deputados_despesas desp ON m.id = desp.mandato_id
                WHERE m.sigla_partido IS NOT NULL
            """
            params_part = []
            if legislatura:
                query_partido += " AND m.legislatura_id = %s"
                params_part.append(legislatura)
                
            query_partido += " GROUP BY m.sigla_partido ORDER BY valor DESC"
            cursor.execute(query_partido, tuple(params_part))
            gastos_partido = [{"partido": r[0], "valor": float(r[1])} for r in cursor.fetchall()]

            # 5. Totais
            cursor.execute("""
                SELECT SUM(valor_documento)
                FROM camara.deputados_despesas
                WHERE TO_DATE(CAST(ano AS TEXT) || '-' || CAST(mes AS TEXT), 'YYYY-MM') >= (CURRENT_DATE - INTERVAL '1 year')
            """)
            total_12_row = cursor.fetchone()
            total_12_meses = total_12_row[0] or 0

            query_total_geral = "SELECT SUM(valor_documento) FROM camara.deputados_despesas desp"
            params_total = []
            if legislatura:
                query_total_geral = """
                    SELECT SUM(desp.valor_documento)
                    FROM camara.deputados_despesas desp
                    JOIN camara.deputados_mandatos m ON desp.mandato_id = m.id
                    WHERE m.legislatura_id = %s
                """
                params_total.append(legislatura)
            
            cursor.execute(query_total_geral, tuple(params_total))
            total_geral = cursor.fetchone()[0] or 0
            
            query_total_fornecedores = "SELECT COUNT(DISTINCT cnpj_cpf_fornecedor) FROM camara.deputados_despesas desp"
            params_forn = []
            if legislatura:
                query_total_fornecedores = """
                    SELECT COUNT(DISTINCT desp.cnpj_cpf_fornecedor)
                    FROM camara.deputados_despesas desp
                    JOIN camara.deputados_mandatos m ON desp.mandato_id = m.id
                    WHERE m.legislatura_id = %s
                """
                params_forn.append(legislatura)
                
            cursor.execute(query_total_fornecedores, tuple(params_forn))
            total_empresas = cursor.fetchone()[0] or 0

            query_gastos_dep = """
            SELECT 
                d.id AS deputado_id,
                d.nome_civil,
                m.sigla_partido,
                m.sigla_uf AS estado,
                SUM(desp.valor_documento) AS total_gasto
            FROM camara.deputados_despesas desp
            JOIN camara.deputados_mandatos m ON desp.mandato_id = m.id
            JOIN camara.deputados d ON m.deputado_id = d.id
            WHERE 1=1
            """
            params_dep = []
            if legislatura:
                query_gastos_dep += " AND m.legislatura_id = %s"
                params_dep.append(legislatura)
            
            query_gastos_dep += """
            GROUP BY d.id, d.nome_civil, m.sigla_partido, m.sigla_uf
            ORDER BY total_gasto DESC
            LIMIT 10;
            """
            cursor.execute(query_gastos_dep, tuple(params_dep))
            gastos_dep_raw = cursor.fetchall()
            
            gastos_deputados = [
                {
                    "deputado_id": r[0], "nome_civil": r[1], "sigla_partido": r[2],
                    "estado": r[3], "total_gasto": float(r[4])
                } 
                for r in gastos_dep_raw
            ]

            return {
                "total_gastos_12_meses": float(total_12_meses),
                "total_12_meses": float(total_12_meses),
                "total_gastos": float(total_geral),
                "total_empresas_contratadas": int(total_empresas),
                "gastos_por_categoria": gastos_categoria,
                "gastos_por_mes": gastos_mensais,
                "gastos_por_estado": gastos_estado,
                "gastos_por_partido": gastos_partido,
                "gastos_deputados": gastos_deputados
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas de despesas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas de despesas")
    finally:
        if conn:
            db.release_db_connection(conn)

@router.get("/empresas/estatisticas", summary="Obtém as estatísticas e ranking das empresas contratadas")
@lru_cache(maxsize=4)
def get_estatisticas_empresas(limit: int = 20, legislatura: int = Query(None)):
    conn = None
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Estatísticas Gerais
            # 1. Estatísticas Gerais
            query_gerais = """
                SELECT 
                    COUNT(DISTINCT d.cnpj_cpf_fornecedor) as total_empresas,
                    SUM(d.valor_documento) as total_pago,
                    COUNT(*) as total_contratos
                FROM camara.deputados_despesas d
                JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
                WHERE LENGTH(d.cnpj_cpf_fornecedor) > 11
            """
            params_geral = []
            if legislatura:
                query_gerais += " AND m.legislatura_id = %s"
                params_geral.append(legislatura)
            
            cursor.execute(query_gerais, tuple(params_geral))
            res_stats = cursor.fetchone()
            total_geral_empresas = float(res_stats[1]) if res_stats[1] else 1.0

            # 2. Ranking de Empresas
            query_top = """
            WITH top_fornecedores AS (
                SELECT 
                    d.cnpj_cpf_fornecedor,
                    MAX(d.nome_fornecedor) as nome,
                    SUM(d.valor_documento) as total_valor,
                    COUNT(*) as qtd_contratos
                FROM camara.deputados_despesas d
                JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
                WHERE LENGTH(d.cnpj_cpf_fornecedor) > 11
            """
            if legislatura:
                query_top += " AND m.legislatura_id = %s"
            
            query_top += """
                GROUP BY d.cnpj_cpf_fornecedor
            ),
            partidos_pagadores AS (
                SELECT 
                    d.cnpj_cpf_fornecedor,
                    m.sigla_partido,
                    SUM(d.valor_documento) as valor
                FROM camara.deputados_despesas d
                JOIN camara.deputados_mandatos m ON d.mandato_id = m.id
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
            ORDER BY tf.total_valor DESC
            LIMIT %s
            """
            
            params_ranking = []
            if legislatura:
                params_ranking.append(legislatura)
            params_ranking.append(limit)
            
            cursor.execute(query_top, tuple(params_ranking))
            res_ranking = cursor.fetchall()
            
            ranking_formatado = []
            for i, r in enumerate(res_ranking):
                nome_bruto = r[1]
                nome_limpo = nome_bruto.split("-")[0].strip().title() if nome_bruto else "Não Informado"
                valor_empresa = float(r[2]) 
                percentual = (valor_empresa / total_geral_empresas) * 100
                                 
                ranking_formatado.append({
                    "rank": i + 1,
                    "cnpj": r[0],
                    "nome": nome_limpo,
                    "valor_total": valor_empresa,
                    "contratos": int(r[3]),
                    "principais_partidos": r[4] if r[4] else "N/A",
                    "percentual": round(percentual, 2)
                })

            return {
                "geral": {
                    "total_empresas": res_stats[0],
                    "total_pago": float(res_stats[1]) if res_stats[1] else 0.0,
                    "total_contratos": res_stats[2]
                },
                "ranking": ranking_formatado
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas de empresas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas de empresas")
    finally:
        if conn:
            db.release_db_connection(conn)





