#!/bin/bash
set -e

# Este script automatiza a criação de múltiplos bancos de dados e a importação de arquivos SQL.
# Ele percorre todos os arquivos .sql dentro da pasta /docker-entrypoint-initdb.d/sql-auto/

SQL_DIR="/docker-entrypoint-initdb.d/sql-auto"

if [ -d "$SQL_DIR" ]; then
    echo "Iniciando automação de importação SQL..."
    for f in "$SQL_DIR"/*.sql; do
        [ -e "$f" ] || continue
        
        # Extrai o nome do arquivo sem a extensão e adiciona _db
        FILENAME=$(basename "$f" .sql)
        DB_NAME="${FILENAME}_db"
        
        echo "Processando arquivo: $f"
        echo "Criando banco de dados: $DB_NAME"
        
        # Cria o banco de dados se ele não existir
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
            SELECT 'CREATE DATABASE $DB_NAME'
            WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec
EOSQL

        echo "Importando dados para $DB_NAME..."
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" < "$f"
        
        echo "Finalizado: $DB_NAME pronto."
    done
else
    echo "Pasta $SQL_DIR não encontrada. Pulando automação."
fi
