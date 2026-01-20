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
            query = """
                SELECT 
                    desp.ano, 
                    desp.mes, 
                    desp.tipo_despesa, 
                    desp.valor_documento, 
                    desp.url_documento
                FROM deputados_despesas AS desp
                JOIN deputados_mandatos AS mand ON desp.mandato_id = mand.id
                WHERE mand.deputado_id = %s
                ORDER BY desp.ano DESC, desp.mes DESC
                LIMIT 50;
            """
            cursor.execute(query, (deputado_id,))
            despesas = cursor.fetchall()
            logging.info(f"Encontradas {len(despesas)} despesas")

            
            resultado_formatado = [
                {
                    "ano": d[0],
                    "mes": d[1],
                    "tipo_despesa": d[2],
                    "valor": d[3],
                    "url_documento": d[4]
                }
                for d in despesas
            ]
            
            return {"despesas": resultado_formatado}

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
    

