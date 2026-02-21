import requests
import psycopg2
import os
import sys
import logging
from datetime import datetime, date
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

try:
    import database.db as db
except ImportError:
    sys.path.append(os.getcwd())
    import database.db as db

load_dotenv()

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

def clear_votos_and_props(conn):
    try:
        with conn.cursor() as cursor:
            logging.info("Limpando seletivamente: votacoes_votos e votacoes_proposicoes...")
            cursor.execute("TRUNCATE TABLE votacoes_votos, votacoes_proposicoes CASCADE;")
            conn.commit()
            logging.info("Tabelas limpas.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao limpar: {e}")
        raise

def get_votacoes_periodo(data_inicio, data_fim):
    votacoes = []
    url = f"{BASE_URL}/votacoes"
    params = {"dataInicio": data_inicio, "dataFim": data_fim, "itens": 100, "ordem": "ASC", "ordenarPor": "dataHoraRegistro"}
    
    while url:
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code != 200:
                logging.error(f"Erro API ({r.status_code}) para {data_inicio} a {data_fim}: {r.text}")
                break
            data = r.json()
            votacoes.extend(data['dados'])
            
            next_link = next((l['href'] for l in data.get('links', []) if l['rel'] == 'next'), None)
            url = next_link
            params = None 
        except Exception as e:
            logging.error(f"Erro na requisição ({data_inicio}-{data_fim}): {e}")
            break
            
    return votacoes

def process_votacao(conn, vot_res):
    vot_id = vot_res['id']
    try:
        r = requests.get(f"{BASE_URL}/votacoes/{vot_id}", timeout=20)
        if r.status_code != 200: return
        det = r.json()['dados']
        
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO votacoes (id, uri, data, data_hora_registro, sigla_orgao, uri_orgao, descricao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET 
                    data_hora_registro = EXCLUDED.data_hora_registro,
                    descricao = EXCLUDED.descricao;
            """, (det['id'], det['uri'], det['data'], det['dataHoraRegistro'], 
                  det['siglaOrgao'], det['uriOrgao'], det['descricao']))

            for p in det.get('proposicoesAfetadas', []):
                pid = p.get('id')
                if pid:
                    cursor.execute("SELECT 1 FROM proposicoes WHERE id = %s", (pid,))
                    if cursor.fetchone():
                        cursor.execute("INSERT INTO votacoes_proposicoes (votacao_id, proposicao_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (det['id'], pid))

            v_url = f"{BASE_URL}/votacoes/{vot_id}/votos"
            while v_url:
                vr = requests.get(v_url, timeout=20)
                if vr.status_code != 200: break
                vd = vr.json()
                for v in vd['dados']:
                    dep_id = v.get('deputado', {}).get('id')
                    if dep_id:
                        cursor.execute("SELECT 1 FROM deputados WHERE id = %s", (dep_id,))
                        if cursor.fetchone():
                            cursor.execute("""
                                INSERT INTO votacoes_votos (votacao_id, deputado_id, tipo_voto, data_registro_voto)
                                VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;
                            """, (det['id'], dep_id, v.get('tipoVoto'), v.get('dataHoraVoto')))
                v_url = next((l['href'] for l in vd.get('links', []) if l['rel'] == 'next'), None)
            conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro no processamento {vot_id}: {e}")

def main():
    logging.info("Iniciando script de ingestão 2007-2025 (com chunking de 3 meses)...")
    conn = db.get_connect()
    if not conn: return
    
    try:
        clear_votos_and_props(conn)
        
        periodos = [
            ("-01-01", "-03-31"),
            ("-04-01", "-06-30"),
            ("-07-01", "-09-30"),
            ("-10-01", "-12-31")
        ]

        for ano in range(2007, 2026):
            logging.info(f"=== Sincronizando Ano: {ano} ===")
            for p_inicio, p_fim in periodos:
                inicio = f"{ano}{p_inicio}"
                fim = f"{ano}{p_fim}"
                
                # Evita datas futuras
                if datetime.strptime(inicio, "%Y-%m-%d").date() > date.today():
                    continue

                lista = get_votacoes_periodo(inicio, fim)
                logging.info(f"Período {inicio} a {fim}: {len(lista)} votações.")
                
                for i, v in enumerate(lista):
                    process_votacao(conn, v)
                    if (i + 1) % 50 == 0:
                        logging.info(f"Status {inicio}-{fim}: {i+1}/{len(lista)}")
                    
    except Exception as e:
        logging.error(f"ERRO FATAL: {e}")
    finally:
        conn.close()
        logging.info("Concluído.")

if __name__ == "__main__":
    main()
