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



@router.get("/proposicoes")
def listar_proposicoes_deputados(
    siglaTipo: str = Query(None), 
    ano: int = Query(None), 
    ementa: str = Query(None), 
    deputado: str = Query(None),
    pagina: int = 1
):
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    
    itens_por_pagina = 15
    offset = (pagina - 1) * itens_por_pagina
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT ON (p.id)
                    p.id, 
                    p.sigla_tipo, 
                    p.numero, 
                    p.ano, 
                    p.ementa, 
                    p.data_apresentacao
                FROM proposicoes p
            """
            params = []
            
            # JOIN com tabelas de votação quando filtrar por deputado
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
                
            # DISTINCT ON requirement: ORDER BY must start with the DISTINCT expression
            query += " ORDER BY p.id DESC LIMIT %s OFFSET %s"
            params.extend([itens_por_pagina, offset])

            
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            
            return [
                {
                    "id": r[0],
                    "siglaTipo": r[1],
                    "numero": r[2],
                    "ano": r[3],
                    "ementa": r[4],
                    "dataApresentacao": r[5].isoformat() if hasattr(r[5], 'isoformat') else str(r[5]) if r[5] else None,
                    "autor_principal": "Desconhecido" # Metadata unavailable due to missing table
                }
                for r in resultados
            ]
    except Exception as e:
        logging.error(f"Erro ao buscar proposições: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar proposições")
    finally:
        conn.close()


@router.get("/proposicoes/{proposicao_id}/votos")
def listar_votos_por_proposicao(proposicao_id: int):

    conn =  db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")

    try:
        with conn.cursor() as cursor:
            query =  """
                SELECT 
                    v.id AS votacao_id,
                    v.data,
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

            cursor.execute(query, (proposicao_id,))
            resultados = cursor.fetchall()

            votacoes_dict = {}

            for row in resultados:
                vot_id = row[0]
                data_votacao = row[1]
                descricao = row[2]
                dep_id = row[3]
                nome_dep = row[4]
                voto = row[5]

                if vot_id not in votacoes_dict:
                    votacoes_dict[vot_id] = {
                        "id_votacao": vot_id,
                        "data": data_votacao.isoformat() if hasattr(data_votacao, 'isoformat') else str(data_votacao),
                        "descricao": descricao,
                        "total_votos": 0,
                        "lista_votos": []
                    }
                
                # Adiciona o voto do deputado na lista desta votação
                votacoes_dict[vot_id]["lista_votos"].append({
                    "deputado_id": dep_id,
                    "nome": nome_dep,
                    "voto": voto
                })
                votacoes_dict[vot_id]["total_votos"] += 1

            # Transformar o dicionário em uma lista para o JSON
            resposta_final = {
                "proposicao_id": proposicao_id,
                "historico_votacoes": list(votacoes_dict.values())
            }

            return resposta_final

    except Exception as e:
        logging.error(f"Erro ao buscar votos da proposição {proposicao_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar votos da proposição")
    finally:
        conn.close()


@router.get("/")
def listar_todos_deputados():

    """Lista todos os deputados com informações básicas"""
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indisponível: Erro de conexão com o banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT DISTINCT ON (d.id)
                    d.id, 
                    d.nome_civil,
                    m.sigla_partido,
                    m.sigla_uf
                FROM deputados d
                INNER JOIN deputados_mandatos m ON d.id = m.deputado_id
                WHERE m.sigla_uf IS NOT NULL
                ORDER BY d.id, m.id DESC
            """
            cursor.execute(query)
            deputados = cursor.fetchall()
            
            resultado = [
                {
                    "id": dep[0],
                    "nome_civil": dep[1],
                    "sigla_partido": dep[2] if dep[2] else "S/P",
                    "uf": dep[3]
                }
                for dep in deputados
            ]
            
            return resultado

    except psycopg2.Error as e:
        logging.error(f"Erro ao listar deputados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao listar deputados.")
    finally:
        if conn: conn.close()


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


@router.get("/comparar")
def comparar_deputados(id1: int, id2: int, ano: int = None):
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indispónivel")
    
    if id1 == id2:
        raise HTTPException(status_code=400, detail="Escolha dois deputados diferentes para comparar.")

    try:
        with conn.cursor() as cursor:
            # 1. Buscar Perfis
            query_perfil = """
                SELECT DISTINCT ON (d.id)
                    d.id, 
                    d.nome_civil, 
                    m.sigla_partido, 
                    m.sigla_uf, 
                    d.email,
                    d.data_nascimento,
                    d.escolaridade,
                    d.uf_nascimento
                FROM deputados d
                LEFT JOIN deputados_mandatos m ON d.id = m.deputado_id
                WHERE d.id IN (%s, %s)
                ORDER BY d.id, m.id DESC
            """
            cursor.execute(query_perfil, (id1, id2))
            perfis = cursor.fetchall()

            if len(perfis) < 2:
                raise HTTPException(status_code=404, detail="Um ou ambos os deputados não foram encontrados.")
            
            comparacao = {}
            for p in perfis:
                data_nasc = p[5]
                comparacao[p[0]] = {
                    "id": p[0],
                    "nome_civil": p[1],
                    "sigla_partido": p[2],
                    "sigla_uf": p[3],
                    "email": p[4],
                    "data_nascimento": data_nasc.isoformat() if isinstance(data_nasc, date) else None,
                    "escolaridade": p[6],
                    "uf_nascimento": p[7],
                    "foto": f"https://www.camara.leg.br/internet/deputado/bandep/{p[0]}.jpg",
                    "total_gasto": 0.0,
                    "qtd_despesas": 0,
                    "maior_categoria": {"nome": "-", "valor": 0.0},
                    "despesas": [],
                    "categorias": []
                }
            
            # 2. Buscar Despesas (Categorias e Total)
            query_stats = """
                SELECT 
                    m.deputado_id, 
                    d.tipo_despesa, 
                    SUM(d.valor_documento) as total,
                    COUNT(d.id) as qtd
                FROM deputados_despesas d
                JOIN deputados_mandatos m ON d.mandato_id = m.id
                WHERE m.deputado_id IN (%s, %s)
            """
            params = [id1, id2]
            if ano:
                query_stats += " AND d.ano = %s"
                params.append(ano)
            query_stats += " GROUP BY m.deputado_id, d.tipo_despesa"

            cursor.execute(query_stats, tuple(params))
            stats = cursor.fetchall() 

            for linha in stats:
                dep_id, cat, valor, qtd = linha
                valor = float(valor)
                if dep_id in comparacao:
                    comparacao[dep_id]["total_gasto"] += valor
                    comparacao[dep_id]["qtd_despesas"] += qtd
                    comparacao[dep_id]["categorias"].append({"categoria": cat, "valor": valor})

                    if valor > comparacao[dep_id]["maior_categoria"]["valor"]:
                        comparacao[dep_id]["maior_categoria"] = {
                            "nome": cat.replace("_", " ").title() if cat else "-",
                            "valor": valor
                        }

            # 3. Buscar Últimas Despesas (Top 10 para cada um)
            for dep_id in [id1, id2]:
                query_recent = """
                    SELECT d.ano, d.mes, d.tipo_despesa, d.valor_documento, d.url_documento
                    FROM deputados_despesas d
                    JOIN deputados_mandatos m ON d.mandato_id = m.id
                    WHERE m.deputado_id = %s
                    ORDER BY d.ano DESC, d.mes DESC
                    LIMIT 10
                """
                cursor.execute(query_recent, (dep_id,))
                recentes = cursor.fetchall()
                comparacao[dep_id]["despesas"] = [
                    {"ano": r[0], "mes": r[1], "tipo_despesa": r[2], "valor": float(r[3]), "url_documento": r[4]}
                    for r in recentes
                ]
            
            resultado_final = [comparacao[id1], comparacao[id2]]
            for item in resultado_final:
                item["total_gasto"] = round(item["total_gasto"], 2)
                item["maior_categoria"]["valor"] = round(item["maior_categoria"]["valor"], 2)

            return resultado_final
            
    except psycopg2.Error as e:
        logging.error(f"Erro ao comparar deputados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao comparar deputados.")
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
            logging.info(f"Buscando despesas para deputado {deputado_id}")
            # Query otimizada com Window Function
            # Traz as despesas limitadas a 50, mas o total_geral considera TODAS as despesas do mandato
            query = """
                SELECT 
                    desp.ano, 
                    desp.mes, 
                    desp.tipo_despesa, 
                    desp.valor_documento, 
                    desp.url_documento,
                    SUM(desp.valor_documento) OVER() as total_geral
                FROM deputados_despesas AS desp
                JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
                ORDER BY desp.ano DESC, desp.mes DESC
                LIMIT 50;
            """
            cursor.execute(query, (deputado_id,))
            resultados = cursor.fetchall()
            logging.info(f"Encontradas {len(resultados)} despesas")

            # Se houver resultados, o total está na coluna 5 (índice 5) da primeira linha
            total_despesas = resultados[0][5] if resultados else 0.0
            
            resultado_formatado = [
                {
                    "ano": r[0],
                    "mes": r[1],
                    "tipo_despesa": r[2],
                    "valor": r[3],
                    "url_documento": r[4]
                }
                for r in resultados
            ]
            
            return {
                "despesas": resultado_formatado,
                "total_despesas": float(total_despesas)
            }

    except psycopg2.Error as e:
        logging.error(f"Erro na query de despesas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as despesas do deputado.")
    finally:
        if conn: conn.close()        
        



@router.get("/estatisticas/categorias")
def estatisticas_categorias():
    conn = db.get_connect()
    if not conn:
        raise HTTPException(status_code=503, detail="Serviço indisponível: Erro de conexão com o banco de dados.")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT tipo_despesa, SUM(valor_documento)
                FROM deputados_despesas
                WHERE ano >= 2023
                GROUP BY tipo_despesa
                ORDER BY 2 DESC
                """
            )
            resultados = cursor.fetchall()
            
            dados_formatados = []
            total_outros = 0.0
            
            LIMITE_TOP = 9
            
            for i, row in enumerate(resultados):
                nome_categoria = row[0]
                valor = float(row[1])
                
                nome_bonito = nome_categoria.title().replace("_", " ")
                
                if i < LIMITE_TOP:
                    dados_formatados.append({
                        "categoria": nome_bonito, 
                        "valor": valor
                    })
                else:
                    total_outros += valor
            
            # Adicionar "Outros" após o loop, se houver
            if total_outros > 0:
                dados_formatados.append({
                    "categoria": "Outros", 
                    "valor": total_outros
                })
            
            return dados_formatados
                
    except psycopg2.Error as e:
        logging.error(f"Erro na query de estatísticas por categorias: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as estatísticas por categorias.")
    finally:
        conn.close()
         
 
@router.get("/estatisticas/geral")
def estatisticas_geral():    
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
            
            # 3. Gastos por Estado do Mandato (UF representada)
            cursor.execute("""
                SELECT m.sigla_uf, SUM(desp.valor_documento) as total
                FROM deputados_mandatos m
                JOIN deputados_despesas desp ON m.id = desp.mandato_id
                WHERE m.sigla_uf IS NOT NULL
                GROUP BY m.sigla_uf
                ORDER BY total DESC;
            """)
            gastos_estado = [{"estado": r[0], "valor": float(r[1])} for r in cursor.fetchall()]

            cursor.execute(
                """
                SELECT m.sigla_partido, SUM(desp.valor_documento) as total
                FROM deputados_mandatos m
                JOIN deputados_despesas desp ON m.id = desp.mandato_id
                WHERE m.sigla_partido IS NOT NULL
                GROUP BY m.sigla_partido
                ORDER BY total DESC;
            """
            )

            gastos_partido =[{"partido": r[0], "valor": float(r[1])} for r in cursor.fetchall()]
    

            # 4. Quantidade de Deputados por Região
            cursor.execute("""
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
                ORDER BY quantidade DESC;
            """)
            
            deputados_regiao = [
                {"name": r[0], "value": int(r[1])} 
                for r in cursor.fetchall()
            ]

    
            cursor.execute("""
                SELECT SUM(valor_documento) 
                FROM deputados_despesas
                WHERE TO_DATE(CAST(ano AS TEXT) || '-' || CAST(mes AS TEXT), 'YYYY-MM') >= (CURRENT_DATE - INTERVAL '1 year');
            """)
            total_12_meses = cursor.fetchone()[0] or 0
                
            cursor.execute("SELECT SUM(valor_documento) from deputados_despesas WHERE ano >= 2023")
            total_geral = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(DISTINCT deputado_id) from deputados_mandatos")
            total_deputados = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(DISTINCT cnpj_cpf_fornecedor) FROM deputados_despesas")
            total_empresas_contratadas = cursor.fetchone()[0] or 0

            return{
                "total_gastos_12_meses": float(total_12_meses),
                "total_gastos": float(total_geral),
                "total_deputados": total_deputados,
                "total_empresas_contratadas": total_empresas_contratadas,
                "gastos_por_categoria": gastos_categoria,
                "gastos_por_mes": gastos_mensais,
                "gastos_por_estado": gastos_estado,
                "gastos_por_partido": gastos_partido,
                "deputados_por_regiao": deputados_regiao
            }
         
    except psycopg2.Error as e:
        logging.error(f"Erro na query de estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as estatísticas.")
    finally:
        conn.close()
    


@router.get("/empresas/estatisticas")
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
        
        
@router.get("/empresas/ranking")
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





