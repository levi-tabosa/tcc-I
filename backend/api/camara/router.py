from fastapi import APIRouter, HTTPException, Query
from datetime import date
import psycopg2
import logging

# Garanta que este import está correto para sua estrutura
import database.db as db

router = APIRouter(
    prefix="/camara",
    tags=["Câmara"]
)


@router.get("/emendas", summary="Busca uma lista de emendas parlamentares")
def get_lista_emendas(
    nome_deputado: str = Query(None),
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
                    d.nome_civil as deputado,
                    e.codigo_emenda as codigo,
                    e.ano,
                    e.tipo_emenda as tipo,
                    e.valor_empenhado as "valorEmpenhado",
                    e.valor_liquidado as "valorLiquidado",
                    e.valor_pago as "valorPago",
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN camara.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
                WHERE 1=1
            """
            params = []
            if nome_deputado:
                query += " AND d.nome_civil ILIKE %s"
                params.append(f"%{nome_deputado}%")
            if ano:
                query += " AND e.ano = %s"
                params.append(ano)
                
            query += " ORDER BY e.ano DESC, e.valor_pago DESC LIMIT %s OFFSET %s"
            params.extend([itens_por_pagina, offset])

            cursor.execute(query, tuple(params))
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Garantir conversão para float
            for r in resultados:
                r["valorEmpenhado"] = float(r["valorEmpenhado"]) if r["valorEmpenhado"] else 0.0
                r["valorLiquidado"] = float(r["valorLiquidado"]) if r["valorLiquidado"] else 0.0
                r["valorPago"] = float(r["valorPago"]) if r["valorPago"] else 0.0
                
            return resultados
    except Exception as e:
        logging.error(f"Erro ao buscar emendas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/emendas/resumo", summary="Obtém resumo das emendas")
def get_resumo_emendas():
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Totais Gerais
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT nome_autor) as total_deputados,
                    COUNT(DISTINCT localidade_gasto) as total_municipios,
                    COUNT(DISTINCT funcao) as total_areas
                FROM portal.emendas
            """)
            row = cursor.fetchone()
            totais = {"total_deputados": row[0], "total_municipios": row[1], "total_areas": row[2]}
            
            # 2. Distribuição por Área
            cursor.execute("""
                SELECT funcao, SUM(valor_pago) as valor_total
                FROM portal.emendas
                GROUP BY funcao
                ORDER BY valor_total DESC
            """)
            areas_raw = [{"funcao": r[0], "valor_total": r[1]} for r in cursor.fetchall()]
            valor_total_global = sum(float(r["valor_total"]) for r in areas_raw) if areas_raw else 1
            
            areas_formatadas = [
                {
                    "nome": r["funcao"] if r["funcao"] else "Outros",
                    "valor": float(r["valor_total"]),
                    "percentual": round((float(r["valor_total"]) / valor_total_global) * 100, 1)
                }
                for r in areas_raw
            ]
            
            # 3. Top 10 Deputados
            cursor.execute("""
                SELECT 
                    d.id, d.nome_civil, m.sigla_partido, m.sigla_uf,
                    SUM(e.valor_pago) as total_valor
                FROM portal.emendas e
                JOIN camara.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
                LEFT JOIN (
                    SELECT DISTINCT ON (deputado_id) deputado_id, sigla_partido, sigla_uf
                    FROM camara.deputados_mandatos
                    ORDER BY deputado_id, id DESC
                ) m ON d.id = m.deputado_id
                GROUP BY d.id, d.nome_civil, m.sigla_partido, m.sigla_uf
                ORDER BY total_valor DESC
                LIMIT 10
            """)
            top_deputados = [
                {
                    "id": r[0], "nome_civil": r[1], "sigla_partido": r[2], 
                    "sigla_uf": r[3], "total_valor": r[4]
                } 
                for r in cursor.fetchall()
            ]

            return {
                "totais": {
                    "deputados": totais["total_deputados"],
                    "municipios": totais["total_municipios"],
                    "areas": totais["total_areas"],
                    "valor_total": valor_total_global
                },
                "areas": areas_formatadas,
                "ranking": [
                    {
                        "id": r["id"],
                        "nome": r["nome_civil"],
                        "partido": r["sigla_partido"] if r["sigla_partido"] else "S/P",
                        "estado": r["sigla_uf"] if r["sigla_uf"] else "BR",
                        "emendasTotal": float(r["total_valor"]),
                        "foto": f"https://www.camara.leg.br/internet/deputado/bandep/{r['id']}.jpg"
                    }
                    for r in top_deputados
                ]
            }
    except Exception as e:
        logging.error(f"Erro ao obter resumo de emendas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar resumo de emendas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

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
    
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
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
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            for r in resultados:
                if r["dataApresentacao"]:
                    r["dataApresentacao"] = r["dataApresentacao"].isoformat() if hasattr(r["dataApresentacao"], 'isoformat') else str(r["dataApresentacao"])
                r["autor_principal"] = "Desconhecido"
                
            return resultados
    except Exception as e:
        logging.error(f"Erro ao buscar proposições: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar proposições")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/proposicoes/{proposicao_id}/votos", summary="Obtém o histórico de votos de um projeto legislativo")
def get_votos_proposicao(proposicao_id: int):
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
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            votacoes_dict = {}
            for row in resultados:
                vot_id = row["votacao_id"]
                if vot_id not in votacoes_dict:
                    votacoes_dict[vot_id] = {
                        "id_votacao": vot_id,
                        "data": row["data_votacao"].isoformat() if hasattr(row["data_votacao"], 'isoformat') else str(row["data_votacao"]),
                        "descricao": row["descricao"],
                        "total_votos": 0,
                        "lista_votos": []
                    }
                
                votacoes_dict[vot_id]["lista_votos"].append({
                    "deputado_id": row["deputado_id"],
                    "nome": row["nome_civil"],
                    "voto": row["voto"]
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
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/lista", summary="Lista todos os deputados ativos")
def get_todos_deputados(legislatura: int = Query(None)):
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
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]

            for r in resultados:
                if not r["sigla_partido"]: r["sigla_partido"] = "S/P"
            return resultados
    except Exception as e:
        logging.error(f"Erro ao buscar lista de deputados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar lista de deputados")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/estatisticas", summary="Obtém estatísticas gerais dos deputados")
def get_estatisticas_gerais(legislatura: int = Query(None)):
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
        if 'conn' in locals() and conn:
            conn.close()



@router.get("/comparar", summary="Compara perfil e gastos entre dois deputados")
def get_comparativo_deputados(id1: int, id2: int, ano: int = None, legislatura: int = Query(None)):
    if id1 == id2:
        raise HTTPException(status_code=400, detail="Escolha dois deputados diferentes para comparar.")

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
            columns = [desc[0] for desc in cursor.description]
            perfis_raw = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            if len(perfis_raw) < 2:
                raise HTTPException(status_code=404, detail="Um ou ambos os deputados não foram encontrados.")
            
            comparacao = {}
            for p in perfis_raw:
                pid = p["id"]
                comparacao[pid] = {
                    **p,
                    "data_nascimento": p["data_nascimento"].isoformat() if isinstance(p["data_nascimento"], date) else None,
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
            columns_stats = [desc[0] for desc in cursor.description]
            stats = [dict(zip(columns_stats, row)) for row in cursor.fetchall()]

            for s in stats:
                dep_id, valor = s["deputado_id"], float(s["total"])
                if dep_id in comparacao:
                    comparacao[dep_id]["total_gasto"] += valor
                    comparacao[dep_id]["qtd_despesas"] += s["qtd"]
                    comparacao[dep_id]["categorias"].append({"categoria": s["tipo_despesa"], "valor": valor})

                    if valor > comparacao[dep_id]["maior_categoria"]["valor"]:
                        comparacao[dep_id]["maior_categoria"] = {
                            "nome": s["tipo_despesa"].replace("_", " ").title() if s["tipo_despesa"] else "-",
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
                columns_rec = [desc[0] for desc in cursor.description]
                recentes = [dict(zip(columns_rec, row)) for row in cursor.fetchall()]
                
                for r in recentes: r["valor"] = float(r["valor"])
                comparacao[dep_id]["despesas"] = recentes
            
            return [comparacao[id1], comparacao[id2]]
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erro ao comparar deputados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar comparação")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/{deputado_id}", summary="Obtém os detalhes do perfil e despesas do deputado pelo ID")
def get_perfil_deputado(deputado_id: int, legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar Perfil (Mandato mais recente da legislatura se especificada)
            query_perfil = """
                SELECT d.id, d.nome_civil, d.cpf, d.sexo, d.email, d.data_nascimento, 
                       d.escolaridade, d.uf_nascimento, d.municipio_nascimento, 
                       m.sigla_partido
                FROM camara.deputados d
                LEFT JOIN camara.deputados_mandatos m ON d.id = m.deputado_id
                WHERE d.id = %s
            """
            params_perfil = [deputado_id]
            if legislatura:
                query_perfil += " AND m.legislatura_id = %s"
                params_perfil.append(legislatura)
            
            query_perfil += " ORDER BY m.id DESC LIMIT 1"
            cursor.execute(query_perfil, tuple(params_perfil))
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Deputado com ID {deputado_id} não encontrado na legislatura {legislatura}")
            
            res = dict(zip(columns, row))
            
            if res["data_nascimento"] and isinstance(res["data_nascimento"], date):
                res["data_nascimento"] = res["data_nascimento"].isoformat()
            
            res["foto"] = f"https://www.camara.leg.br/internet/deputado/bandep/{res['id']}.jpg"

            # 2. Buscar as 50 despesas mais recentes
            query_recente = """
                SELECT 
                    desp.ano, desp.mes, desp.tipo_despesa, 
                    desp.valor_documento as valor, desp.url_documento
                FROM camara.deputados_despesas AS desp
                JOIN camara.deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
            """
            params_recente = [deputado_id]
            if legislatura:
                query_recente += " AND mand.legislatura_id = %s"
                params_recente.append(legislatura)
            
            query_recente += " ORDER BY desp.ano DESC, desp.mes DESC LIMIT 50"
            cursor.execute(query_recente, tuple(params_recente))
            col_desp = [desc[0] for desc in cursor.description]
            despesas = [dict(zip(col_desp, r)) for r in cursor.fetchall()]
            for d in despesas: d["valor"] = float(d["valor"])

            # 3. Resumo por categoria
            query_categorias = """
                SELECT desp.tipo_despesa as categoria, SUM(desp.valor_documento) as valor
                FROM camara.deputados_despesas AS desp
                JOIN camara.deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
            """
            params_cat = [deputado_id]
            if legislatura:
                query_categorias += " AND mand.legislatura_id = %s"
                params_cat.append(legislatura)
            
            query_categorias += " GROUP BY desp.tipo_despesa ORDER BY valor DESC"
            cursor.execute(query_categorias, tuple(params_cat))
            col_cat = [desc[0] for desc in cursor.description]
            categorias = [dict(zip(col_cat, r)) for r in cursor.fetchall()]
            total_despesas = sum(float(c["valor"]) for c in categorias)
            for c in categorias: c["valor"] = float(c["valor"])

            # 4. Buscar Resumo de Emendas
            query_emendas_resumo = """
                SELECT SUM(e.valor_pago) as total_emendas
                FROM portal.emendas e
                JOIN camara.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
                WHERE d.id = %s
            """
            cursor.execute(query_emendas_resumo, (deputado_id,))
            row_emendas = cursor.fetchone()
            total_emendas = float(row_emendas[0]) if row_emendas and row_emendas[0] else 0.0

            return {
                **res,
                "despesas": despesas,
                "total_despesas": total_despesas,
                "categorias": categorias,
                "total_emendas": total_emendas
            }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erro ao buscar perfil do deputado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar perfil")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/{deputado_id}/despesas", summary="Obtém a lista de despesas de um deputado")
def get_despesas_deputado(deputado_id: int, legislatura: int = Query(None)):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Buscar as 50 despesas mais recentes
            query_recente = """
                SELECT 
                    desp.ano, desp.mes, desp.tipo_despesa, 
                    desp.valor_documento as valor, desp.url_documento
                FROM camara.deputados_despesas AS desp
                JOIN camara.deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
            """
            params_recente = [deputado_id]
            if legislatura:
                query_recente += " AND mand.legislatura_id = %s"
                params_recente.append(legislatura)
                
            query_recente += " ORDER BY desp.ano DESC, desp.mes DESC LIMIT 50"
            cursor.execute(query_recente, tuple(params_recente))
            col_desp = [desc[0] for desc in cursor.description]
            despesas = [dict(zip(col_desp, r)) for r in cursor.fetchall()]
            for d in despesas: d["valor"] = float(d["valor"])

            # 2. Resumo por categoria
            query_categorias = """
                SELECT desp.tipo_despesa as categoria, SUM(desp.valor_documento) as valor
                FROM camara.deputados_despesas AS desp
                JOIN camara.deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
            """
            params_cat = [deputado_id]
            if legislatura:
                query_categorias += " AND mand.legislatura_id = %s"
                params_cat.append(legislatura)
                
            query_categorias += " GROUP BY desp.tipo_despesa ORDER BY valor DESC"
            cursor.execute(query_categorias, tuple(params_cat))
            col_cat = [desc[0] for desc in cursor.description]
            categorias = [dict(zip(col_cat, r)) for r in cursor.fetchall()]
            total_despesas = sum(float(c["valor"]) for c in categorias)
            for c in categorias: c["valor"] = float(c["valor"])

            return {
                "despesas": despesas,
                "total_despesas": total_despesas,
                "categorias": categorias
            }
    except Exception as e:
        logging.error(f"Erro ao buscar despesas do deputado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar despesas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/{deputado_id}/emendas", summary="Obtém a lista de emendas parlamentares de um deputado")
def get_emendas_deputado(deputado_id: int):
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
                    e.valor_empenhado as "valorEmpenhado",
                    e.valor_liquidado as "valorLiquidado",
                    e.valor_pago as "valorPago",
                    e.funcao,
                    e.localidade_gasto as localidade
                FROM portal.emendas e
                JOIN camara.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
                WHERE d.id = %s
                ORDER BY e.ano DESC, e.valor_pago DESC
            """
            cursor.execute(query, (deputado_id,))
            columns = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            for r in resultados:
                r["valorEmpenhado"] = float(r["valorEmpenhado"]) if r["valorEmpenhado"] else 0.0
                r["valorLiquidado"] = float(r["valorLiquidado"]) if r["valorLiquidado"] else 0.0
                r["valorPago"] = float(r["valorPago"]) if r["valorPago"] else 0.0
                
            return resultados
    except Exception as e:
        logging.error(f"Erro ao buscar emendas do deputado: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar emendas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/despesas/estatisticas", summary="Obtém o panorama geral de gastos da Câmara")
def get_estatisticas_despesas(legislatura: int = Query(None)):    
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Gastos por Categoria (com formatação Top 9 + Outros)
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
            resultados_categoria = [{"categoria": r[0], "valor": r[1]} for r in cursor.fetchall()]
            
            gastos_categoria = []
            total_outros = 0.0
            LIMITE_TOP = 9
            
            for i, row in enumerate(resultados_categoria):
                nome_formatado = row["categoria"].title().replace("_", " ") if row["categoria"] else "Outros"
                valor = float(row["valor"])
                
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
                SELECT SUM(valor_documento) as total
                FROM camara.deputados_despesas
                WHERE TO_DATE(CAST(ano AS TEXT) || '-' || CAST(mes AS TEXT), 'YYYY-MM') >= (CURRENT_DATE - INTERVAL '1 year')
            """)
            total_12_meses = cursor.fetchone()[0] or 0

            query_total_geral = "SELECT SUM(valor_documento) as total FROM camara.deputados_despesas desp"
            params_total = []
            if legislatura:
                query_total_geral = """
                    SELECT SUM(desp.valor_documento) as total 
                    FROM camara.deputados_despesas desp
                    JOIN camara.deputados_mandatos m ON desp.mandato_id = m.id
                    WHERE m.legislatura_id = %s
                """
                params_total.append(legislatura)
            
            cursor.execute(query_total_geral, tuple(params_total))
            total_geral = cursor.fetchone()[0] or 0
            
            query_total_fornecedores = "SELECT COUNT(DISTINCT cnpj_cpf_fornecedor) as total FROM camara.deputados_despesas desp"
            params_forn = []
            if legislatura:
                query_total_fornecedores = """
                    SELECT COUNT(DISTINCT desp.cnpj_cpf_fornecedor) as total 
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
            gastos_deputados = [
                {
                    "deputado_id": r[0], "nome_civil": r[1], "sigla_partido": r[2],
                    "estado": r[3], "total_gasto": float(r[4])
                } 
                for r in cursor.fetchall()
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
        if 'conn' in locals() and conn:
            conn.close()

@router.get("/empresas/estatisticas", summary="Obtém as estatísticas e ranking das empresas contratadas")
def get_estatisticas_empresas(limit: int = 20):
    try:
        conn = db.get_db_connection()
        if not conn:
            raise HTTPException(status_code=503, detail="Banco de dados indisponível")
        
        with conn.cursor() as cursor:
            # 1. Estatísticas Gerais
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT cnpj_cpf_fornecedor) as total_empresas,
                    COALESCE(SUM(valor_documento), 0) as total_pago,
                    COUNT(*) as total_contratos
                FROM camara.deputados_despesas
                WHERE LENGTH(cnpj_cpf_fornecedor) > 11
            """)
            res_stats = cursor.fetchone()
            stats = {
                "total_empresas": res_stats[0],
                "total_pago": res_stats[1],
                "total_contratos": res_stats[2]
            }
            
            total_geral_empresas = float(stats["total_pago"]) if stats["total_pago"] else 1.0

            # 2. Ranking de Empresas
            cursor.execute("""
            WITH top_fornecedores AS (
                SELECT 
                    cnpj_cpf_fornecedor,
                    MAX(nome_fornecedor) as nome,
                    SUM(valor_documento) as total_valor,
                    COUNT(*) as qtd_contratos
                FROM camara.deputados_despesas
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
            """, (limit,))
            resultados_ranking = [
                {
                    "cnpj": r[0], "nome": r[1], "total_valor": r[2], 
                    "qtd_contratos": r[3], "principais_partidos": r[4]
                }
                for r in cursor.fetchall()
            ]
            
            ranking_formatado = []
            for i, row in enumerate(resultados_ranking):
                nome_bruto = row["nome"]
                nome_limpo = nome_bruto.split("-")[0].strip().title() if nome_bruto else "Não Informado"
                valor_empresa = float(row["total_valor"]) 
                percentual = (valor_empresa / total_geral_empresas) * 100
                                 
                ranking_formatado.append({
                    "rank": i + 1,
                    "cnpj": row["cnpj"],
                    "nome": nome_limpo,
                    "valor_total": valor_empresa,
                    "contratos": int(row["qtd_contratos"]),
                    "principais_partidos": row["principais_partidos"] if row["principais_partidos"] else "N/A",
                    "percentual": round(percentual, 2)
                })

            return {
                "geral": {
                    "total_empresas": stats["total_empresas"] or 0,
                    "total_pago": float(stats["total_pago"]) if stats["total_pago"] else 0,
                    "total_contratos": stats["total_contratos"] or 0
                },
                "ranking": ranking_formatado
            }
    except Exception as e:
        logging.error(f"Erro ao buscar estatísticas de empresas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar estatísticas de empresas")
    finally:
        if 'conn' in locals() and conn:
            conn.close()





