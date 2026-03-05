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

def _execute_query(query: str, params: tuple = None, fetch_one: bool = False):
    """Auxiliar para executar queries e retornar resultados como dicionário."""
    conn = db.get_connect_camara()
    if not conn:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            
            # Se for uma query que não retorna nada (INSERT/UPDATE), retorna None
            if cursor.description is None:
                conn.commit()
                return None
                
            columns = [desc[0] for desc in cursor.description]
            if fetch_one:
                row = cursor.fetchone()
                return dict(zip(columns, row)) if row else None
            
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Erro na base de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a requisição")
    finally:
        conn.close()


@router.get("/emendas", summary="Busca uma lista de emendas parlamentares")
def get_lista_emendas(
    nome_deputado: str = Query(None),
    ano: int = Query(None),
    pagina: int = 1
):
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina

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
        JOIN public.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
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

    resultados = _execute_query(query, tuple(params))
    
    # Garantir conversão para float
    for r in resultados:
        r["valorEmpenhado"] = float(r["valorEmpenhado"]) if r["valorEmpenhado"] else 0.0
        r["valorLiquidado"] = float(r["valorLiquidado"]) if r["valorLiquidado"] else 0.0
        r["valorPago"] = float(r["valorPago"]) if r["valorPago"] else 0.0
        
    return resultados

@router.get("/emendas/resumo", summary="Obtém resumo das emendas")
def get_resumo_emendas():
    # 1. Totais Gerais
    totais = _execute_query("""
        SELECT 
            COUNT(DISTINCT nome_autor) as total_deputados,
            COUNT(DISTINCT localidade_gasto) as total_municipios,
            COUNT(DISTINCT funcao) as total_areas
        FROM portal.emendas
    """, fetch_one=True)
    
    # 2. Distribuição por Área
    areas_raw = _execute_query("""
        SELECT funcao, SUM(valor_pago) as valor_total
        FROM portal.emendas
        GROUP BY funcao
        ORDER BY valor_total DESC
    """)
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
    top_deputados = _execute_query("""
        SELECT 
            d.id, d.nome_civil, m.sigla_partido, m.sigla_uf,
            SUM(e.valor_pago) as total_valor
        FROM portal.emendas e
        JOIN public.deputados d ON lower(e.nome_autor) = lower(d.nome_civil)
        LEFT JOIN (
            SELECT DISTINCT ON (deputado_id) deputado_id, sigla_partido, sigla_uf
            FROM public.deputados_mandatos
            ORDER BY deputado_id, id DESC
        ) m ON d.id = m.deputado_id
        GROUP BY d.id, d.nome_civil, m.sigla_partido, m.sigla_uf
        ORDER BY total_valor DESC
        LIMIT 10
    """)

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

@router.get("/proposicoes", summary="Busca uma lista de projetos legislativos")
def get_lista_proposicoes(
    siglaTipo: str = Query(None), 
    ano: int = Query(None), 
    ementa: str = Query(None), 
    deputado: str = Query(None),
    pagina: int = 1
):
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina
    
    query = """
        SELECT DISTINCT ON (p.id)
            p.id, 
            p.sigla_tipo as "siglaTipo", 
            p.numero, 
            p.ano, 
            p.ementa, 
            p.data_apresentacao as "dataApresentacao"
        FROM proposicoes p
    """
    params = []
    
    if deputado:
        query += """
            INNER JOIN votacoes_proposicoes vp ON p.id = vp.proposicao_id
            INNER JOIN votacoes_votos vv ON vp.votacao_id = vv.votacao_id
            INNER JOIN deputados d ON vv.deputado_id = d.id
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
        
    query += " ORDER BY p.id DESC LIMIT %s OFFSET %s"
    params.extend([itens_por_pagina, offset])

    resultados = _execute_query(query, tuple(params))
    
    for r in resultados:
        if r["dataApresentacao"]:
            r["dataApresentacao"] = r["dataApresentacao"].isoformat() if hasattr(r["dataApresentacao"], 'isoformat') else str(r["dataApresentacao"])
        r["autor_principal"] = "Desconhecido"
        
    return resultados


@router.get("/proposicoes/{proposicao_id}/votos", summary="Obtém o histórico de votos de um projeto legislativo")
def get_votos_proposicao(proposicao_id: int):
    query = """
        SELECT 
            v.id AS votacao_id,
            v.data as data_votacao,
            v.descricao,
            d.id AS deputado_id,
            d.nome_civil,
            vv.tipo_voto AS voto
        FROM votacoes_proposicoes vp
        INNER JOIN votacoes v ON vp.votacao_id = v.id
        INNER JOIN votacoes_votos vv ON v.id = vv.votacao_id
        INNER JOIN deputados d ON vv.deputado_id = d.id
        WHERE vp.proposicao_id = %s
        ORDER BY v.data DESC, d.nome_civil ASC
    """
    resultados = _execute_query(query, (proposicao_id,))
    
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


@router.get("/lista", summary="Lista todos os deputados ativos")
def get_todos_deputados():
    query = """
        SELECT DISTINCT ON (d.id)
            d.id, 
            d.nome_civil,
            m.sigla_partido,
            m.sigla_uf as uf
        FROM deputados d
        INNER JOIN deputados_mandatos m ON d.id = m.deputado_id
        WHERE m.sigla_uf IS NOT NULL
        ORDER BY d.id, m.id DESC
    """
    resultados = _execute_query(query)
    for r in resultados:
        if not r["sigla_partido"]: r["sigla_partido"] = "S/P"
    return resultados


@router.get("/estatisticas", summary="Obtém estatísticas gerais dos deputados")
def get_estatisticas_gerais():
    # 1. Total de Deputados
    total_deputados = _execute_query("SELECT COUNT(DISTINCT deputado_id) as total from deputados_mandatos", fetch_one=True)["total"] or 0

    # 2. Distribuição por Região
    deputados_regiao_raw = _execute_query("""
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
        FROM deputados_mandatos m
        WHERE m.sigla_uf IS NOT NULL
        GROUP BY regiao
        ORDER BY quantidade DESC
    """)
    deputados_regiao = [{"name": r["regiao"], "value": int(r["quantidade"])} for r in deputados_regiao_raw]

    return {
        "total_deputados": int(total_deputados),
        "deputados_por_regiao": deputados_regiao
    }



@router.get("/comparar", summary="Compara perfil e gastos entre dois deputados")
def get_comparativo_deputados(id1: int, id2: int, ano: int = None):
    if id1 == id2:
        raise HTTPException(status_code=400, detail="Escolha dois deputados diferentes para comparar.")

    # 1. Buscar Perfis
    query_perfil = """
        SELECT DISTINCT ON (d.id)
            d.id, d.nome_civil, m.sigla_partido, m.sigla_uf, 
            d.email, d.data_nascimento, d.escolaridade, d.uf_nascimento
        FROM deputados d
        LEFT JOIN deputados_mandatos m ON d.id = m.deputado_id
        WHERE d.id IN (%s, %s)
        ORDER BY d.id, m.id DESC
    """
    perfis_raw = _execute_query(query_perfil, (id1, id2))
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
        FROM deputados_despesas d
        JOIN deputados_mandatos m ON d.mandato_id = m.id
        WHERE m.deputado_id IN (%s, %s)
    """
    params = [id1, id2]
    if ano:
        query_stats += " AND d.ano = %s"
        params.append(ano)
    query_stats += " GROUP BY m.deputado_id, d.tipo_despesa"

    stats = _execute_query(query_stats, tuple(params))
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
        recentes = _execute_query("""
            SELECT d.ano, d.mes, d.tipo_despesa, d.valor_documento as valor, d.url_documento
            FROM deputados_despesas d
            JOIN deputados_mandatos m ON d.mandato_id = m.id
            WHERE m.deputado_id = %s
            ORDER BY d.ano DESC, d.mes DESC
            LIMIT 10
        """, (dep_id,))
        for r in recentes: r["valor"] = float(r["valor"])
        comparacao[dep_id]["despesas"] = recentes
    
    return [comparacao[id1], comparacao[id2]]

@router.get("/{deputado_id}", summary="Obtém os detalhes do perfil e despesas do deputado pelo ID")
def get_perfil_deputado(deputado_id: int):
    # 1. Buscar Perfil
    query_perfil = """
        SELECT d.id, d.nome_civil, d.cpf, d.sexo, d.email, d.data_nascimento, 
               d.escolaridade, d.uf_nascimento, d.municipio_nascimento, 
               m.sigla_partido
        FROM deputados d
        LEFT JOIN deputados_mandatos m ON d.id = m.deputado_id
        WHERE d.id = %s
        ORDER BY m.id DESC
        LIMIT 1
    """
    res = _execute_query(query_perfil, (deputado_id,), fetch_one=True)
    if not res:
        raise HTTPException(status_code=404, detail=f"Deputado com ID {deputado_id} não encontrado")
    
    if res["data_nascimento"] and isinstance(res["data_nascimento"], date):
        res["data_nascimento"] = res["data_nascimento"].isoformat()
    
    res["foto"] = f"https://www.camara.leg.br/internet/deputado/bandep/{res['id']}.jpg"

    # 2. Buscar as 50 despesas mais recentes
    query_recente = """
        SELECT 
            desp.ano, desp.mes, desp.tipo_despesa, 
            desp.valor_documento as valor, desp.url_documento
        FROM deputados_despesas AS desp
        JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
        WHERE mand.deputado_id = %s
        ORDER BY desp.ano DESC, desp.mes DESC
        LIMIT 50
    """
    despesas = _execute_query(query_recente, (deputado_id,))
    for d in despesas: d["valor"] = float(d["valor"])

    # 3. Resumo por categoria
    query_categorias = """
        SELECT desp.tipo_despesa as categoria, SUM(desp.valor_documento) as valor
        FROM deputados_despesas AS desp
        JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
        WHERE mand.deputado_id = %s
        GROUP BY desp.tipo_despesa
        ORDER BY valor DESC
    """
    categorias = _execute_query(query_categorias, (deputado_id,))
    total_despesas = sum(float(c["valor"]) for c in categorias)
    for c in categorias: c["valor"] = float(c["valor"])

    # 4. Consolidar Resposta
    return {
        **res,
        "despesas": despesas,
        "total_despesas": total_despesas,
        "categorias": categorias
    }
        

@router.get("/{deputado_id}/despesas", summary="Obtém a lista de despesas de um deputado")
def get_despesas_deputado(deputado_id: int):
    # 1. Buscar as 50 despesas mais recentes
    query_recente = """
        SELECT 
            desp.ano, desp.mes, desp.tipo_despesa, 
            desp.valor_documento as valor, desp.url_documento
        FROM deputados_despesas AS desp
        JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
        WHERE mand.deputado_id = %s
        ORDER BY desp.ano DESC, desp.mes DESC
        LIMIT 50
    """
    despesas = _execute_query(query_recente, (deputado_id,))
    for d in despesas: d["valor"] = float(d["valor"])

    # 2. Resumo por categoria
    query_categorias = """
        SELECT desp.tipo_despesa as categoria, SUM(desp.valor_documento) as valor
        FROM deputados_despesas AS desp
        JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
        WHERE mand.deputado_id = %s
        GROUP BY desp.tipo_despesa
        ORDER BY valor DESC
    """
    categorias = _execute_query(query_categorias, (deputado_id,))
    total_despesas = sum(float(c["valor"]) for c in categorias)
    for c in categorias: c["valor"] = float(c["valor"])

    return {
        "despesas": despesas,
        "total_despesas": total_despesas,
        "categorias": categorias
    }
        



@router.get("/despesas/estatisticas", summary="Obtém o panorama geral de gastos da Câmara")
def get_estatisticas_despesas():    
    # 1. Gastos por Categoria (com formatação Top 9 + Outros)
    resultados_categoria = _execute_query("""
        SELECT tipo_despesa as categoria, SUM(valor_documento) as valor
        FROM deputados_despesas
        GROUP BY tipo_despesa
        ORDER BY valor DESC
    """)
    
    gastos_categoria = []
    total_outros = 0.0
    LIMITE_TOP = 9
    
    for i, row in enumerate(resultados_categoria):
        nome_formatado = row["categoria"].title().replace("_", " ")
        valor = float(row["valor"])
        
        if i < LIMITE_TOP:
            gastos_categoria.append({"categoria": nome_formatado, "valor": valor})
        else:
            total_outros += valor
    
    if total_outros > 0:
        gastos_categoria.append({"categoria": "Outros", "valor": total_outros})

    # 2. Evolução Mensal
    gastos_mensais = _execute_query("""
        SELECT ano, mes, SUM(valor_documento) as valor
        FROM deputados_despesas
        GROUP BY ano, mes
        ORDER BY ano DESC, mes DESC
        LIMIT 12
    """)
    for g in gastos_mensais: g["valor"] = float(g["valor"])
    
    # 3. Gastos por Estado
    gastos_estado = _execute_query("""
        SELECT m.sigla_uf as estado, SUM(desp.valor_documento) as valor
        FROM deputados_mandatos m
        JOIN deputados_despesas desp ON m.id = desp.mandato_id
        WHERE m.sigla_uf IS NOT NULL
        GROUP BY m.sigla_uf
        ORDER BY valor DESC
    """)
    for g in gastos_estado: g["valor"] = float(g["valor"])

    # 4. Gastos por Partido
    gastos_partido = _execute_query("""
        SELECT m.sigla_partido as partido, SUM(desp.valor_documento) as valor
        FROM deputados_mandatos m
        JOIN deputados_despesas desp ON m.id = desp.mandato_id
        WHERE m.sigla_partido IS NOT NULL
        GROUP BY m.sigla_partido
        ORDER BY valor DESC
    """)
    for g in gastos_partido: g["valor"] = float(g["valor"])

    # 5. Totais
    total_12_meses = _execute_query("""
        SELECT SUM(valor_documento) as total
        FROM deputados_despesas
        WHERE TO_DATE(CAST(ano AS TEXT) || '-' || CAST(mes AS TEXT), 'YYYY-MM') >= (CURRENT_DATE - INTERVAL '1 year')
    """, fetch_one=True)["total"] or 0

    total_geral = _execute_query("SELECT SUM(valor_documento) as total from deputados_despesas", fetch_one=True)["total"] or 0
    total_empresas = _execute_query("SELECT COUNT(DISTINCT cnpj_cpf_fornecedor) as total FROM deputados_despesas", fetch_one=True)["total"] or 0

    query = """
    SELECT 
        d.id AS deputado_id,
        d.nome_civil,
        m.sigla_partido,
        m.sigla_uf AS estado,
        SUM(desp.valor_documento) AS total_gasto
    FROM public.deputados_despesas desp
    JOIN public.deputados_mandatos m ON desp.mandato_id = m.id
    JOIN public.deputados d ON m.deputado_id = d.id
    GROUP BY d.id, d.nome_civil, m.sigla_partido, m.sigla_uf
    ORDER BY total_gasto DESC
    LIMIT 10;
    """
    gastos_deputados = _execute_query(query)
    for g in gastos_deputados: g["total_gasto"] = float(g["total_gasto"])

    return {
        "total_gastos_12_meses": float(total_12_meses),
        "total_gastos": float(total_geral),
        "total_empresas_contratadas": int(total_empresas),
        "gastos_por_categoria": gastos_categoria,
        "gastos_por_mes": gastos_mensais,
        "gastos_por_estado": gastos_estado,
        "gastos_por_partido": gastos_partido,
        "gastos_deputados": gastos_deputados
    }
    


@router.get("/empresas/estatisticas", summary="Obtém as estatísticas e ranking das empresas contratadas")
def get_estatisticas_empresas(limit: int = 20):
    # 1. Estatísticas Gerais
    stats = _execute_query("""
        SELECT 
            COUNT(DISTINCT cnpj_cpf_fornecedor) as total_empresas,
            COALESCE(SUM(valor_documento), 0) as total_pago,
            COUNT(*) as total_contratos
        FROM deputados_despesas
        WHERE LENGTH(cnpj_cpf_fornecedor) > 11
    """, fetch_one=True)
    
    total_geral_empresas = float(stats["total_pago"]) if stats["total_pago"] else 1.0

    # 2. Ranking de Empresas
    query_ranking = """
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
    ORDER BY tf.total_valor DESC
    """
    resultados_ranking = _execute_query(query_ranking, (limit,))
    
    ranking_formatado = []
    for i, row in enumerate(resultados_ranking):
        nome_bruto = row["nome"]
        nome_limpo = nome_bruto.split("-")[0].strip().title() if nome_bruto else "Não Informado"
        valor_empresa = float(row["total_valor"]) 
        percentual = (valor_empresa / total_geral_empresas) * 100
                         
        ranking_formatado.append({
            "rank": i + 1,
            "cnpj": row["cnpj_cpf_fornecedor"],
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





