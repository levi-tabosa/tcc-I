#!/bin/bash
set -e

# Script para configurar o banco fiscaliza_db com os schemas camara, senado e portal
# e importar os respectivos arquivos SQL.

SQL_DIR="/docker-entrypoint-initdb.d/sql-auto"
DB_NAME="$POSTGRES_DB"

echo "Iniciando a configuração do banco: $DB_NAME"

# 1. Cria os schemas
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS camara;
    CREATE SCHEMA IF NOT EXISTS senado;
    CREATE SCHEMA IF NOT EXISTS portal;
EOSQL

# 2. Importa os arquivos SQL para os respectivos schemas
# Nota: Assumimos que os nomes dos arquivos na pasta sql-auto são camara.sql, senado.sql e portal_data.sql

# Importando CAMARA
if [ -f "$SQL_DIR/camara.sql" ]; then
    echo "Importando CAMARA para o schema 'camara' (ajustando public -> camara)..."
    sed 's/public\./camara./g' "$SQL_DIR/camara.sql" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" --set search_path=camara
else
    echo "Aviso: camara.sql não encontrado."
fi

# Importando SENADO
if [ -f "$SQL_DIR/senado.sql" ]; then
    echo "Importando SENADO para o schema 'senado' (ajustando public -> senado)..."
    sed 's/public\./senado./g' "$SQL_DIR/senado.sql" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" --set search_path=senado
else
    echo "Aviso: senado.sql não encontrado."
fi

# Importando PORTAL
if [ -f "$SQL_DIR/portal_data.sql" ]; then
    echo "Importando PORTAL para o schema 'portal'..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" --set search_path=portal < "$SQL_DIR/portal_data.sql"
else
    echo "Aviso: portal_data.sql não encontrado."
fi

echo "Configuração do fiscaliza_db concluída com sucesso."
