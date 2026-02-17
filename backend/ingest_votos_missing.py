import os
import sys
import psycopg2
import requests
import logging
import time

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_env_vars():
    env_path = os.path.join(os.getcwd(), 'backend', '.env')
    vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    vars[key] = value
    return vars

def get_connect():
    env = get_env_vars()
    db_url = os.getenv("DATABASE_URL", env.get("DATABASE_URL"))
    if db_url:
        try:
            return psycopg2.connect(db_url)
        except:
            pass
    
    return psycopg2.connect(
        host=env.get("DB_HOST", "localhost"),
        port=env.get("DB_PORT", "5432"),
        database=env.get("DB_NAME", "camara_db"),
        user=env.get("DB_USER", "postgres"),
        password=env.get("DB_PASSWORD", "postgres")
    )

def ingest_missing():
    conn = get_connect()
    cur = conn.cursor()
    
    # 1. Buscar votações que não estão em votacoes_proposicoes
    # Podemos também buscar votações "falhas" ou "pendentes" em votacoes_status
    logging.info("Buscando votações sem vínculos de proposição (mais recentes primeiro)...")
    cur.execute("""
        SELECT v.id 
        FROM votacoes v
        LEFT JOIN votacoes_proposicoes vp ON v.id = vp.votacao_id
        WHERE vp.votacao_id IS NULL
        ORDER BY v.id DESC
        LIMIT 500
    """)
    votacoes_pendentes = [r[0] for r in cur.fetchall()]
    logging.info(f"Encontradas {len(votacoes_pendentes)} votações pendentes no lote.")

    for vid in votacoes_pendentes:
        try:
            logging.info(f"Processando votação {vid}...")
            # Detalhes da votação
            res = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{vid}")
            if res.status_code != 200:
                logging.error(f"Erro ao buscar detalhes da votação {vid}: {res.status_code}")
                continue
            
            data = res.json().get('dados', {})
            
            # Formatos possíveis de proposições vinculadas
            pids = set()
            
            # 1. proposicaoObjeto
            obj = data.get('proposicaoObjeto')
            if obj and obj.get('id'):
                pids.add(obj.get('id'))
            
            # 2. objetosPossiveis
            objs = data.get('objetosPossiveis', [])
            for o in objs:
                if o.get('id'):
                    pids.add(o.get('id'))
            
            # 3. proposicoesAfetadas
            afetadas = data.get('proposicoesAfetadas', [])
            for a in afetadas:
                if a.get('id'):
                    pids.add(a.get('id'))
            
            inserted_p = 0
            for pid in pids:
                # Verificar se a proposição existe na tabela proposicoes
                cur.execute("SELECT id FROM proposicoes WHERE id = %s", (pid,))
                if cur.fetchone():
                    cur.execute(
                        "INSERT INTO votacoes_proposicoes (votacao_id, proposicao_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (vid, pid)
                    )
                    inserted_p += 1
            
            if inserted_p > 0:
                logging.info(f"Vínculos criados: {inserted_p} proposições para {vid}.")

            # Buscar Votos
            res_votos = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{vid}/votos")
            inserted_v = 0
            if res_votos.status_code == 200:
                votos = res_votos.json().get('dados', [])
                if not votos:
                    logging.info(f"Votação {vid} não possui votos nominais (votos simbólicos ou administrativos).")
                for v in votos:
                    dep_data = v.get('deputado', {})
                    dep_id = dep_data.get('id') if dep_data else None
                    
                    if dep_id:
                        cur.execute(
                            """INSERT INTO votacoes_votos (votacao_id, deputado_id, tipo_voto, data_registro_voto) 
                               VALUES (%s, %s, %s, %s) 
                               ON CONFLICT DO NOTHING""",
                            (vid, dep_id, v.get('tipoVoto'), v.get('dataRegistroVoto'))
                        )
                        inserted_v += 1
            else:
                logging.warning(f"Não foi possível buscar votos para {vid} (Status {res_votos.status_code}).")
            
            if inserted_v > 0:
                logging.info(f"Votos inseridos: {inserted_v} para {vid}.")
            
            # Atualizar status para sucesso (mesmo que não tenha vínculo ou votos, pois já checamos)
            cur.execute(
                "INSERT INTO votacoes_status (votacao_id, status, checked_at) VALUES (%s, 'sucesso', NOW()) ON CONFLICT (votacao_id) DO UPDATE SET status = 'sucesso', checked_at = NOW()",
                (vid,)
            )
            
            conn.commit()
            logging.info(f"Votação {vid} finalizada com sucesso.")
            time.sleep(0.3)
            
        except Exception as e:
            logging.error(f"Erro fatal ao processar {vid}: {e}")
            conn.rollback()

    cur.close()
    conn.close()

    cur.close()
    conn.close()

if __name__ == "__main__":
    ingest_missing()
