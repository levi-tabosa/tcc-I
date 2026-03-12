#!/bin/bash
set -e

# Script para criar o schema 'portal' e importar os dados nos bancos de dados existentes.
# Assume que o arquivo portal_data.sql foi montado em /tmp/portal_data.sql

PORTAL_DIR="/docker-entrypoint-initdb.d/portal-auto"

if [ ! -d "$PORTAL_DIR" ]; then
    echo "Aviso: Pasta $PORTAL_DIR não encontrada. Pulando importação do portal."
    exit 0
fi

# Lista de bancos de dados para importar os dados do portal
DATABASES=("camara_db")

for f in "$PORTAL_DIR"/*.sql; do
    [ -e "$f" ] || continue
    
    echo "Processando arquivo de portal: $f"
    
    for DB_NAME in "${DATABASES[@]}"; do
        echo "Configurando schema 'portal' no banco: $DB_NAME"
        
        # Cria o schema portal se não existir
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
            CREATE SCHEMA IF NOT EXISTS portal;
EOSQL

        echo "Importando dados do portal ($f) para $DB_NAME..."
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" --set search_path=portal < "$f"
    done
done

echo "Todos os arquivos do portal foram processados."
