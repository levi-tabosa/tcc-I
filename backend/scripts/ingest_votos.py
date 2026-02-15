import os
import requests
import psycopg2
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/camara_db")
        )
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco: {e}")
        return None

def get_votacoes_pendentes(year=None, limit=500):
    """Busca votações que ainda não foram processadas e não estão marcadas como concluídas."""
    conn = get_db_connection()
    if not conn: return []
    
    try:
        with conn.cursor() as cursor:
            # Seleciona votações que não estão na tabela de status ou estão marcadas como 'erro' ou 'vazio' (para re-tentar se necessário)
            # Mas aqui focamos nas que NUNCA foram checadas.
            query = """
                SELECT v.id, v.descricao, v.data
                FROM votacoes v
                LEFT JOIN votacoes_status vs ON v.id = vs.votacao_id
                WHERE vs.votacao_id IS NULL
            """
            params = []
            if year:
                query += " AND EXTRACT(YEAR FROM v.data) = %s"
                params.append(year)
            
            # Prioriza Plenário e Comissões se quiser, mas aqui vamos por data
            query += " ORDER BY v.data DESC LIMIT %s"
            params.append(limit)
            
            logging.info(f"Buscando até {limit} votações pendentes para o ano: {year if year else 'Todos'}")
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
    except Exception as e:
        logging.error(f"Erro ao buscar votações: {e}")
        return []
    finally:
        conn.close()

def update_status(votacao_id, status):
    conn = get_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO votacoes_status (votacao_id, status, checked_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (votacao_id) DO UPDATE SET status = EXCLUDED.status, checked_at = EXCLUDED.checked_at
            """, (votacao_id, status, datetime.now()))
        conn.commit()
    except Exception as e:
        logging.error(f"Erro ao atualizar status: {e}")
    finally:
        conn.close()

def ingest_votos_for_votacao(votacao_id):
    url = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{votacao_id}/votos"
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            update_status(votacao_id, '404')
            return 0
        response.raise_for_status()
        votos = response.json().get('dados', [])
        
        if not votos:
            update_status(votacao_id, 'vazio')
            return 0
            
        conn = get_db_connection()
        count = 0
        with conn.cursor() as cursor:
            for v in votos:
                deputado = v.get('deputado_') or v.get('deputado', {})
                deputado_id = deputado.get('id')
                tipo_voto = v.get('tipoVoto')
                data_registro = v.get('dataRegistroVoto')
                
                if not deputado_id: continue
                
                cursor.execute("""
                    INSERT INTO votacoes_votos (votacao_id, deputado_id, tipo_voto, data_registro_voto, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (votacao_id, deputado_id) DO NOTHING
                """, (votacao_id, deputado_id, tipo_voto, data_registro, datetime.now()))
                if cursor.rowcount > 0:
                    count += 1
        conn.commit()
        conn.close()
        
        update_status(votacao_id, 'sucesso' if count > 0 else 'vazio')
        return count
    except Exception as e:
        logging.error(f"Erro ao processar votação {votacao_id}: {e}")
        update_status(votacao_id, 'erro')
        return 0

def main():
    # Processar anos de 2025 a 2008
    years = range(2025, 2007, -1)
    
    total_novos_votos = 0
    for year in years:
        logging.info(f"--- Iniciando processamento do ano {year} ---")
        while True:
            votacoes = get_votacoes_pendentes(year, limit=100)
            if not votacoes:
                logging.info(f"Todas as votações de {year} já foram processadas ou não existem.")
                break
                
            logging.info(f"Processando lote de {len(votacoes)} votações em {year}...")
            
            batch_votos = 0
            for v_id, desc, data in votacoes:
                votos_count = ingest_votos_for_votacao(v_id)
                if votos_count > 0:
                    batch_votos += votos_count
            
            total_novos_votos += batch_votos
            logging.info(f"Lote concluído. Votos adicionais: {batch_votos}. Total acumulado: {total_novos_votos}")
            
            # Pequena pausa ou limite para não sobrecarregar a API no loop massivo
            # Se batch_votos for 0 em muitas votações, o loop continua rápido.

    logging.info(f"Ingestão massiva concluída. Total de novos votos: {total_novos_votos}")

if __name__ == "__main__":
    main()
